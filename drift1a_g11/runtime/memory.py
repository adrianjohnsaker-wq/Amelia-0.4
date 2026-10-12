"""Pure deterministic ports and explicit DRIFT-1A adaptations. Python 3.8+."""
import copy
import math


def clip(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def norm(d):
    total = sum(d.values())
    return {k: v / total for k, v in d.items()} if total > 0 else {}


def entropy(d):
    return -sum(p * math.log2(p) for p in d.values() if p > 0)


class CommitmentMemory:
    """Numeric port of CommitmentMemoryEngine; label exceptions optional.

    Legacy defaults reproduce TS. DRIFT passes label_exceptions=False, deliberately
    removing zone-1->crystal preference and zone-0->9 capture exclusion.
    """
    def __init__(self, label_exceptions=True):
        self.states = {}
        self.label_exceptions = label_exceptions

    def save(self, key, state):
        state = copy.deepcopy(state)
        traces = state['traces']
        if not traces:
            return
        latest = traces[-1]
        dist = norm(latest.get('exitDistribution', {}))
        ranked = sorted(dist.items(), key=lambda p: -p[1])
        dominant, strength = ranked[0] if ranked else (None, 0)
        second = ranked[1][1] if len(ranked) > 1 else 0
        if self.label_exceptions and state['sourceZone'] == 'zone-1-flux':
            if dist.get('zone-0-crystal', 0) > 0:
                dominant, strength = 'zone-0-crystal', dist['zone-0-crystal']
        rivals = {k: max(0, strength - p) for k, p in ranked if k != dominant}
        strengths = [norm(t.get('exitDistribution', {})).get(dominant, 0) for t in traces[-4:]]
        narrowing = clip(.5 + (strengths[-1] - strengths[0]) * 2) if dominant and len(traces) >= 2 else 0
        ent = entropy(dist)
        avg = sum(rivals.values()) / len(rivals) if rivals else 0
        foreclosure = clip(max(0, strength - second) * 1.8 + avg * 1.2 + (1 - ent / 2.2) * .8)
        confidence = (clip(foreclosure * .45 + latest.get('selfLoopDepth', 0) * .20
                           + latest.get('gammaOccupancy', 0) * .20
                           + clip((latest.get('btl', 0) - 30) / 20) * .15)
                      if dominant and len(traces) >= 2 else foreclosure * .5)
        f = dict(zone=state['sourceZone'], dominantExit=dominant, dominantStrength=strength,
                 secondStrength=second, localEntropy=ent, narrowingConfidence=narrowing,
                 rivalSuppression=rivals, foreclosureStrength=foreclosure, commitmentConfidence=confidence)
        if self.label_exceptions and f['zone'] == 'zone-0-flux' and dominant == 'zone-9-flux':
            return
        if foreclosure < .18 or confidence < .55:
            return
        state.update(foreclosure=f, active=True, decay=1.0)
        self.states[key] = state

    def bias(self, key, zone, step):
        s = self.states.get(key)
        if not s or not s.get('active') or s['sourceZone'] != zone or not s.get('foreclosure'):
            return None
        f = s['foreclosure']
        decay = .9985 ** max(0, step - s['savedAtStep']) * (s.get('decay') or 1.0)
        if decay < .08 or s['confidence'] < .55 or f['foreclosureStrength'] < .18 or not f['dominantExit']:
            return None
        return dict(preferredExit=f['dominantExit'], boost=min(.22, (.08 + f['commitmentConfidence'] * .14) * decay),
                    rivalPenalties={k: min(.28, p * (.65 + f['foreclosureStrength']) * decay)
                                    for k, p in f['rivalSuppression'].items()}, confidence=s['confidence'],
                    foreclosureStrength=f['foreclosureStrength'], commitmentConfidence=f['commitmentConfidence'],
                    narrowingConfidence=f['narrowingConfidence'], shouldApply=True, decay=decay)

    @staticmethod
    def apply(scores, bias):
        out = dict(scores)
        if bias:
            k = bias['preferredExit']
            if k in out:
                out[k] *= 1 + bias['boost']
            for k, p in bias['rivalPenalties'].items():
                if k in out:
                    out[k] *= max(.01, 1 - p)
        return out


class LegacyRetention:
    """Exact TS behavior for regression only; NOT used in DRIFT dynamics."""
    def __init__(self):
        self.states = {}
        self.last = {}

    def apply(self, zone, raw, depth, delta=1):
        raw, depth = clip(raw), clip(depth)
        alive = raw >= .08
        if zone != 'zone-2-flux':
            self.last = dict(zone=zone, retentionFloorActive=False, priorPeakSelfLoop=0,
                             rawSelfLoopProb=raw, retainedSelfLoopProb=raw, retentionWindowAge=0,
                             decayMode='inactive', thresholdCrossed=False, sufficientlyAlive=alive, floorApplied=False)
            return raw
        prev = self.states.get(zone, dict(priorPeakSelfLoop=0, retentionFloorActive=False, retentionWindowAge=0))
        peak = max(prev['priorPeakSelfLoop'], depth)
        crossed = peak >= .35
        active = prev['retentionFloorActive'] or crossed
        age = prev['retentionWindowAge']
        retained, mode = raw, 'inactive'
        if not active:
            age = 0
        else:
            age += delta
            if age <= 500 and alive:
                retained, mode = max(.4, raw * .985), 'slow_floor'
            else:
                active, age, retained, mode = False, 0, raw * .9, 'fast_release'
        retained = clip(retained)
        state = dict(zone=zone, priorPeakSelfLoop=peak, retentionFloorActive=active,
                     retainedSelfLoopProb=retained, rawSelfLoopProb=raw, retentionWindowAge=age, decayMode=mode)
        self.states[zone] = state
        self.last = dict(state, thresholdCrossed=crossed, sufficientlyAlive=alive, floorApplied=mode == 'slow_floor')
        return retained


class ProcessFieldMemory:
    """Exact arithmetic/update-order port of substrate/ProcessFieldMemory.ts.

    Camel-case state keys are retained for audit and differential testing.
    Domain interpretations of signals are declared by the caller, not this port.
    """
    KEYS = ('selfLoopMomentum', 'corridorPressure', 'ringBias', 'latentReadiness',
            'compressionDebt', 'releaseDebt', 'prevSelfLoopDepth', 'prevRingSignal', 'prevCorridorSignal')

    def __init__(self, state=None):
        self.state = {k: (state or {}).get(k, 0.0) for k in self.KEYS}

    def update(self, x):
        s = self.state
        sl, ring, corridor = x['selfLoopDepth'], x['ringSignal'], x['corridorSignal']
        s['selfLoopMomentum'] = clip(.90 * s['selfLoopMomentum'] + .10 * (sl - s['prevSelfLoopDepth']), -1, 1)
        drive = .45 * clip(sl) + .35 * clip(corridor) + .20 * max(0, s['latentReadiness'])
        s['corridorPressure'] = clip(.92 * s['corridorPressure'] + .08 * drive)
        s['ringBias'] = clip(.95 * s['ringBias'] + .05 * clip(ring))
        drive = (.35 * max(0, s['selfLoopMomentum']) + .30 * s['corridorPressure']
                 + .20 * s['compressionDebt'] + .15 * clip(x['latentSignal']))
        s['latentReadiness'] = clip(.90 * s['latentReadiness'] + .10 * drive)
        if x['compressionActive'] and not x['transitionSuccess']:
            s['compressionDebt'] = clip(s['compressionDebt'] + .03)
        elif x['transitionSuccess']:
            s['compressionDebt'] = clip(s['compressionDebt'] * .70)
        else:
            s['compressionDebt'] = clip(s['compressionDebt'] * .98)
        if x['releaseSignal'] > .25 and not x['transitionSuccess'] and s['corridorPressure'] < .40:
            s['releaseDebt'] = clip(s['releaseDebt'] + .03)
        elif x['transitionSuccess']:
            s['releaseDebt'] = clip(s['releaseDebt'] * .65)
        else:
            s['releaseDebt'] = clip(s['releaseDebt'] * .98)
        s.update(prevSelfLoopDepth=clip(sl), prevRingSignal=clip(ring), prevCorridorSignal=clip(corridor))
        return self.modulation()

    def modulation(self):
        s = self.state
        label = 'indeterminate'
        if s['ringBias'] > .55 and s['corridorPressure'] < .35:
            label = 'oscillatory'
        elif s['selfLoopMomentum'] > .10 and s['compressionDebt'] > .20:
            label = 'transition-ready' if s['corridorPressure'] > .45 and s['latentReadiness'] > .35 else 'compressing'
        elif s['corridorPressure'] > .45 and s['latentReadiness'] > .25:
            label = 'corridor-seeking'
        elif s['ringBias'] > .45 and (s['releaseDebt'] > .20 or s['compressionDebt'] > .20):
            label = 'brittle-return'
        elif s['releaseDebt'] > .30:
            label = 'release-building'
        return dict(thresholdShift=clip(.40 * max(0, s['selfLoopMomentum']) + .35 * s['corridorPressure'] + .25 * s['compressionDebt']),
                    corridorAvailability=clip(.45 * s['corridorPressure'] + .35 * s['latentReadiness'] - .30 * s['ringBias']),
                    persistenceFactor=clip(.50 * max(0, s['selfLoopMomentum']) + .30 * s['compressionDebt'] + .20 * s['corridorPressure']),
                    releaseVolatility=clip(.55 * s['releaseDebt'] + .20 * s['latentReadiness'] - .25 * s['ringBias']),
                    fieldStateLabel=label)
