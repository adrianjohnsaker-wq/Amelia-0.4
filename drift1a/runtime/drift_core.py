"""DRIFT-1A engineering candidate v0.1. Standard library; no network, clock or RNG.

A new, registered-in-waiting composition, NOT a claim of autonomous intelligence.
The canonical modules are immutable inputs. Each tick is one legal D1 passage;
no episodic ingress is added and terminal components remain closed.
"""
import copy
import hashlib
import json
import math
import os
import sys
from collections import Counter
from memory import CommitmentMemory, ProcessFieldMemory, entropy, norm

CANONICAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'canonical')
if CANONICAL_DIR not in sys.path:
    sys.path.insert(0, CANONICAL_DIR)
import NumogramDynamics as D
import amelia_core

VERSION = 'DRIFT-1A-G1-0.1.0'
DEFAULTS = dict(window=32, phase_min_events=4, pre_lock_depth=.35, near_lock_depth=.65,
                max_phase_entropy=.85, retention_floor=.40, retention_steps=500,
                retention_min_raw=.08, governor_gain=2.0, gt00='include')


def canonical_json(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def digest(x):
    return hashlib.sha256(canonical_json(x).encode('ascii')).hexdigest()


def verify_canonical():
    r = amelia_core.check(CANONICAL_DIR)
    if not r['ok']:
        raise ValueError('canonical source integrity failure')
    return r


def edge_id(e):
    return canonical_json(e)


def edge_order(e):
    return (e[0], {'syzygy': 0, 'current': 1, 'gate': 2}[e[2]], e[1], e[3])


def canonical_edges():
    verify_canonical()
    return sorted([e.as_list() for e in D.canonical_graph().edges], key=edge_order)


def keyed_uniform(input_hex, tick, operation='transition', stream='DRIFT-1A'):
    """53-bit [0,1) SHA256 variate; no arm, graph or mutable draw counter in key.

    input_hex may be synthetic or externally verified beacon randomness. This
    function does NOT verify signatures or establish future-release eligibility.
    """
    if not isinstance(input_hex, str) or len(input_hex) != 64:
        raise ValueError('input must be a 32-byte hex string')
    try:
        raw = bytes.fromhex(input_hex)
    except ValueError:
        raise ValueError('invalid randomness hex')
    if len(raw) != 32 or type(tick) is not int or tick < 0:
        raise ValueError('invalid random input or tick')
    key = canonical_json([VERSION, stream, tick, operation]).encode('ascii')
    n = int.from_bytes(hashlib.sha256(key + b'\0' + raw).digest()[:8], 'big') >> 11
    return n / float(1 << 53)


def sample(probs, u):
    if not isinstance(u, (int, float)) or isinstance(u, bool) or not math.isfinite(u) or not 0 <= u < 1:
        raise ValueError('u must be finite in [0,1)')
    if not probs or any(not math.isfinite(p) or p < 0 for p in probs) or abs(sum(probs) - 1) > 1e-12:
        raise ValueError('invalid probability distribution')
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if p > 0 and u < acc:
            return i
    return max(i for i, p in enumerate(probs) if p > 0)


def degree_signature(edges):
    return dict(in_degree=sorted(Counter((e[2], e[1]) for e in edges).items()),
                out_degree=sorted(Counter((e[2], e[0]) for e in edges).items()),
                self_loops=sorted(edge_id(e) for e in edges if e[0] == e[1]))


def rewire(edges, seed='DRIFT-1A-G1-20261011', swaps=100):
    """Frozen directed typed double-edge swaps. Preserve all original self-loops,
    typed in/out degrees, source edge labels and weights; reject parallel edges
    of the same type. Does not preserve SCCs or reciprocal syzygy pairing.
    """
    out = copy.deepcopy(edges)
    baseline = degree_signature(out)
    done = 0
    for attempt in range(20000):
        if done == swaps:
            break
        h = hashlib.sha256((seed + ':' + str(attempt)).encode()).digest()
        i, j = int.from_bytes(h[:4], 'big') % len(out), int.from_bytes(h[4:8], 'big') % len(out)
        a, b = out[i], out[j]
        if i == j or a[2] != b[2] or a[0] == a[1] or b[0] == b[1] or a[0] == b[0] or a[1] == b[1]:
            continue
        if a[0] == b[1] or b[0] == a[1]:
            continue
        occupied = {(e[0], e[1], e[2]) for k, e in enumerate(out) if k not in (i, j)}
        if (a[0], b[1], a[2]) in occupied or (b[0], a[1], b[2]) in occupied:
            continue
        a[1], b[1] = b[1], a[1]
        done += 1
    if done != swaps or degree_signature(out) != baseline or sorted(out) == sorted(edges):
        raise ValueError('failed to construct distinct degree-matched graph')
    return sorted(out, key=edge_order)


def empty_history():
    return dict(field=ProcessFieldMemory().state, observations={str(z): [] for z in range(10)},
                traces={str(z): [] for z in range(10)}, commitment={}, retention={}, updates=0)


def validate_graph(edges):
    if not isinstance(edges, list) or not edges:
        raise ValueError('empty graph')
    seen = set()
    for e in edges:
        if (not isinstance(e, list) or len(e) != 6 or type(e[0]) is not int or type(e[1]) is not int
                or e[0] not in range(10) or e[1] not in range(10) or e[2] not in ('current', 'gate', 'syzygy')
                or not isinstance(e[3], str) or type(e[5]) is not bool):
            raise ValueError('invalid typed edge')
        k = (e[0], e[1], e[2])
        if k in seen:
            raise ValueError('duplicate same-type edge')
        seen.add(k)
    if {e[0] for e in edges} != set(range(10)):
        raise ValueError('all ten zones must have legal exits')


class Substrate:
    def __init__(self, edges=None, start=1, config=None):
        if type(start) is not int or start not in range(10):
            raise ValueError('invalid start')
        self.edges = sorted(copy.deepcopy(edges if edges is not None else canonical_edges()), key=edge_order)
        validate_graph(self.edges)
        self.config = dict(DEFAULTS)
        if config:
            if set(config) - set(DEFAULTS):
                raise ValueError('unknown configuration field')
            self.config.update(config)
        for k in ('window', 'phase_min_events', 'retention_steps'):
            if type(self.config[k]) is not int or self.config[k] <= 0:
                raise ValueError('invalid integer config')
        for k in ('pre_lock_depth', 'near_lock_depth', 'max_phase_entropy', 'retention_floor', 'retention_min_raw'):
            if not math.isfinite(self.config[k]) or not 0 <= self.config[k] <= 1:
                raise ValueError('invalid probability config')
        if not math.isfinite(self.config['governor_gain']) or self.config['governor_gain'] < 0:
            raise ValueError('invalid Governor gain')
        if self.config['gt00'] not in ('include', 'exclude'):
            raise ValueError('invalid Gt-00 policy')
        self.P = dict(zone=start, tick=0)
        self.H = empty_history()

    def reset_memory(self):
        self.H = empty_history()

    def snapshot(self):
        body = dict(version=VERSION, edges=self.edges, config=self.config, P=self.P, H=self.H)
        return copy.deepcopy(dict(body, digest=digest(body)))

    @classmethod
    def restore(cls, snapshot):
        d = copy.deepcopy(snapshot)
        want = d.pop('digest', None)
        if set(d) != {'version', 'edges', 'config', 'P', 'H'} or d['version'] != VERSION or digest(d) != want:
            raise ValueError('checkpoint digest/version/schema mismatch')
        s = cls(d['edges'], d['P']['zone'], d['config'])
        if type(d['P']['tick']) is not int or d['P']['tick'] < 0 or set(d['H']) != set(empty_history()):
            raise ValueError('invalid checkpoint state')
        if set(d['H']['field']) != set(ProcessFieldMemory.KEYS):
            raise ValueError('invalid field schema')
        for name in ('observations', 'traces'):
            if set(d['H'][name]) != {str(z) for z in range(10)}:
                raise ValueError('invalid history schema')
        s.P, s.H = d['P'], d['H']
        return s

    def _row(self, zone):
        row = [e for e in self.edges if e[0] == zone and not (e[5] and self.config['gt00'] == 'exclude')]
        if not row:
            raise ValueError('no legal candidates: halt, never invent a hold edge')
        return row

    def _signals(self, src, dst):
        """New graph-generic operationalization, NOT canonical CCRU semantics.
        Loop fraction: source-local last W completed events including hypothetical
        candidate. Corridor: normalized concentration of observed source exits.
        Ring: return to a destination already in that source's recent history.
        Latent: novel destination. Release: departure. Success: departure from an
        empirical >=.35 loop episode. This internal objective is a design choice.
        """
        past = self.H['observations'][str(src)]
        obs = (past + [dst])[-self.config['window']:]
        sl = sum(x == src for x in obs) / len(obs)
        k = len({e[1] for e in self._row(src)})
        h = entropy(norm(dict(Counter(obs)))) / math.log2(k) if k > 1 else 0
        compressed = sl >= self.config['pre_lock_depth']
        previous_sl = sum(x == src for x in past) / len(past) if past else 0
        return dict(step=self.P['tick'], currentZone='zone-%d-flux' % src, selfLoopDepth=sl,
                    ringSignal=float(dst in past), corridorSignal=1 - h,
                    latentSignal=float(dst not in past), releaseSignal=float(dst != src),
                    transitionSuccess=bool(dst != src and previous_sl >= self.config['pre_lock_depth']),
                    compressionActive=compressed)

    def distribution(self):
        """Read-only evaluation of all legal candidates from the SAME prior H.
        Governor simulates field update in isolated copies; no candidate writes
        live state or consumes a random draw. Cost=predicted compression+release
        debt. Weight multiplier=1/(1+gain*cost). No target zone or relay input.
        """
        src, tick = self.P['zone'], self.P['tick']
        row = self._row(src)
        base = [2.0 if e[2] == 'current' else 1.0 for e in row]
        base = [p / sum(base) for p in base]
        zones = {}
        for e, p in zip(row, base):
            label = 'zone-%d-flux' % e[1]
            zones[label] = zones.get(label, 0) + p
        cm = CommitmentMemory(label_exceptions=False)
        cm.states = self.H['commitment']
        label = 'zone-%d-flux' % src
        bias = cm.bias(label, label, tick)
        zone_adjusted = CommitmentMemory.apply(zones, bias)
        commitment = [p * zone_adjusted['zone-%d-flux' % e[1]] / zones['zone-%d-flux' % e[1]]
                      for e, p in zip(row, base)]
        audits, weights = [], []
        for e, w in zip(row, commitment):
            f = ProcessFieldMemory(copy.deepcopy(self.H['field']))
            signals = self._signals(src, e[1])
            f.update(signals)
            cost = f.state['compressionDebt'] + f.state['releaseDebt']
            factor = 1 / (1 + self.config['governor_gain'] * cost)
            weights.append(w * factor)
            audits.append(dict(edge=e, decision='ADMIT', reason='legal; finite predicted debt',
                               predicted_field=f.state, cost=cost, multiplier=factor))
        probs = [w / sum(weights) for w in weights]
        pre_retention = list(probs)
        retained = self.H['retention'].get(str(src), {})
        active = retained.get('activation_tick', -1) <= tick < retained.get('expiry_tick', -1)
        self_indices = [i for i, e in enumerate(row) if e[1] == src]
        raw = sum(probs[i] for i in self_indices)
        applied = bool(active and self_indices and raw >= self.config['retention_min_raw']
                       and raw < self.config['retention_floor'])
        if applied:
            floor = self.config['retention_floor']
            probs = [p * floor / raw if i in self_indices else p * (1 - floor) / (1 - raw)
                     for i, p in enumerate(probs)]
        return dict(candidates=row, base=base, probabilities=probs, pre_retention=pre_retention,
                    commitment_bias=bias, governor=audits,
                    retention=dict(active=active, floor_applied=applied, raw=raw,
                                   final=sum(probs[i] for i in self_indices)))

    def advance(self, u, reset=False):
        # Validate randomness before a reset/mutation; failure is transactional.
        if not isinstance(u, (int, float)) or isinstance(u, bool) or not math.isfinite(u) or not 0 <= u < 1:
            raise ValueError('invalid variate')
        if reset:
            self.reset_memory()
        pre = self.snapshot()
        read = self.distribution()
        i = sample(read['probabilities'], u)
        e = read['candidates'][i]
        src, dst, tick = e[0], e[1], self.P['tick']
        signals = self._signals(src, dst)
        f = ProcessFieldMemory(self.H['field'])
        f.update(signals)
        self.H['field'] = f.state
        obs = self.H['observations'][str(src)]
        obs.append(dst)
        del obs[:-self.config['window']]
        # Source-local empirical distribution with a single D1 prior pseudocount.
        dist = {}
        for edge, p in zip(read['candidates'], read['base']):
            label = 'zone-%d-flux' % edge[1]
            dist[label] = dist.get(label, 0) + p
        for z in obs:
            label = 'zone-%d-flux' % z
            dist[label] = dist.get(label, 0) + 1
        dist = norm(dist)
        h = entropy(dist) / math.log2(len(dist)) if len(dist) > 1 else 0
        sl = signals['selfLoopDepth']
        phase = 'neutral'
        if len(obs) >= self.config['phase_min_events'] and h <= self.config['max_phase_entropy']:
            if sl >= self.config['near_lock_depth']:
                phase = 'near_lock'
            elif sl >= self.config['pre_lock_depth']:
                phase = 'pre_lock'
        trace = dict(step=tick, currentZone='zone-%d-flux' % src, exitDistribution=dist,
                     selfLoopDepth=sl, gammaOccupancy=0.0, btl=0.0)
        traces = self.H['traces'][str(src)]
        traces.append(trace)
        del traces[:-4]
        if phase != 'neutral':
            cm = CommitmentMemory(label_exceptions=False)
            cm.states = self.H['commitment']
            label = 'zone-%d-flux' % src
            cm.save(label, dict(runId='lineage', sourceZone=label, confidence=1.0,
                                savedAtStep=tick + 1, candidateExit=None, traces=traces))
            self.H['commitment'] = cm.states
        # Rising threshold qualification after completed events, never stale peak.
        if any(x[1] == src for x in read['candidates']):
            state = self.H['retention'].setdefault(str(src), dict(above=False, activation_tick=-1, expiry_tick=-1))
            above = sl >= self.config['pre_lock_depth']
            if above and not state['above'] and tick + 1 >= state['expiry_tick']:
                state.update(activation_tick=tick + 1, expiry_tick=tick + 1 + self.config['retention_steps'])
            state['above'] = above
        self.H['updates'] += 1
        self.P = dict(zone=dst, tick=tick + 1)
        return dict(tick=tick, u=u, reset=reset, selected_edge=e, phase_after_event=phase,
                    memory_read_digest=digest(pre['H']), pre_state_digest=pre['digest'],
                    selection=read, post_state_digest=self.snapshot()['digest'])
