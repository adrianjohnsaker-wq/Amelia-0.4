"""G1.1 embodiment wrapper. The accepted G1 selector is byte-for-byte unchanged."""
import copy
import math
from collections import Counter
from drift_core import Substrate, canonical_edges, digest, keyed_uniform
from memory import CommitmentMemory

VERSION = 'DRIFT-1A-G1.1-0.1.0'
BOUNDARY = (0, 3, 6, 9)
EPISODE_CAP = 1260
POLICY = dict(version=VERSION, boundary=list(BOUNDARY), episode_cap=EPISODE_CAP,
              ingress='uniform-ten-zones-at-tick-start', initial_entry='uniform',
              ticks='one-legal-move-per-arm', memory='carry-CG-reset-M-before-choice',
              clock='global-tick', outcome='post-move-boundary-Warp-or-Plex')


def variates(value, tick):
    return {op: keyed_uniform(value, tick, operation=op, stream=VERSION)
            for op in ('ingress', 'transition')}


def proposal(u):
    if type(u) not in (int, float) or not math.isfinite(u) or not 0 <= u < 1:
        raise ValueError('invalid uniform variate')
    return int(10 * u)


class EpisodicSubstrate:
    def __init__(self, edges=None):
        # Placeholder zone is never sampled: tick zero always performs ingress.
        self.core = Substrate(edges if edges is not None else canonical_edges(), 0)
        self.episode = dict(index=-1, length=0, pending_entry=True)

    @property
    def P(self):
        return self.core.P

    @property
    def edges(self):
        return self.core.edges

    def snapshot(self):
        d = dict(version=VERSION, policy=POLICY, core=self.core.snapshot(), episode=self.episode)
        return copy.deepcopy(dict(d, digest=digest(d)))

    @classmethod
    def restore(cls, snapshot):
        d = copy.deepcopy(snapshot)
        claimed = d.pop('digest', None)
        if (set(d) != {'version', 'policy', 'core', 'episode'} or d['version'] != VERSION
                or d['policy'] != POLICY or digest(d) != claimed):
            raise ValueError('G1.1 snapshot schema/version/digest mismatch')
        s = cls(d['core']['edges'])
        s.core = Substrate.restore(d['core'])
        ep = d['episode']
        if (set(ep) != {'index', 'length', 'pending_entry'} or type(ep['index']) is not int
                or type(ep['length']) is not int or type(ep['pending_entry']) is not bool
                or ep['index'] < -1 or not 0 <= ep['length'] <= EPISODE_CAP):
            raise ValueError('invalid episode state')
        s.episode = ep
        return s

    def advance(self, u, ingress_u, reset=False):
        zone = proposal(ingress_u)
        proposal(u)  # validate both before any mutation
        prior = self.snapshot()['digest']
        entered = self.episode['pending_entry']
        ingress = None
        if entered:
            ingress = dict(kind='embodiment-entry', zone=zone, tick=self.P['tick'])
            self.core.P['zone'] = zone
            self.episode = dict(index=self.episode['index'] + 1, length=0, pending_entry=False)
        # Core resets M's complete H before reading it, and updates H only after selection.
        event = self.core.advance(u, reset=reset)
        self.episode['length'] += 1
        dst = event['selected_edge'][1]
        end = 'boundary' if dst in BOUNDARY else ('cap' if self.episode['length'] == EPISODE_CAP else None)
        self.episode['pending_entry'] = end is not None
        sel = event['selection']
        zones = {}
        for e, p in zip(sel['candidates'], sel['base']):
            label = 'zone-%d-flux' % e[1]
            zones[label] = zones.get(label, 0) + p
        adjusted = CommitmentMemory.apply(zones, sel['commitment_bias'])
        committed = [p * adjusted['zone-%d-flux' % e[1]] / zones['zone-%d-flux' % e[1]]
                     for e, p in zip(sel['candidates'], sel['base'])]
        # Count observable stage changes above the registered numerical tolerance.
        changed = lambda a, b: any(abs(x-y) > 1e-12 for x,y in zip(a,b))
        event['effects'] = dict(commitment_changed=changed(committed, sel['base']),
                               governor_changed=changed(sel['pre_retention'], committed),
                               retention_changed=changed(sel['probabilities'], sel['pre_retention']))
        event['embodiment'] = dict(ingress_u=ingress_u, proposed_entry=zone, entry=ingress,
            episode=self.episode['index'], length=self.episode['length'], end=end,
            outcome=('Warp' if dst in (3,6) else 'Plex') if end == 'boundary' else None)
        event['pre_embodiment_digest'] = prior
        event['post_embodiment_digest'] = self.snapshot()['digest']
        return event


def episode_metrics(events):
    """Only completed boundary episodes enter the Warp/Plex denominator."""
    completed, route, effects = [], [], {str(z): dict(choices=0, commitment_changed=0,
        governor_changed=0, retention_changed=0, commitment_active=0, retention_active=0) for z in range(10)}
    for e in events:
        b = e['embodiment']
        if b['entry'] is not None:
            route = [b['entry']['zone']]
        route.append(e['selected_edge'][1])
        x = effects[str(e['selected_edge'][0])]
        x['choices'] += 1
        for k,v in e['effects'].items(): x[k] += int(v)
        x['commitment_active'] += int(bool(e['selection']['commitment_bias']))
        x['retention_active'] += int(e['selection']['retention']['active'])
        if b['end']:
            completed.append(dict(episode=b['episode'], length=b['length'], end=b['end'],
                                  outcome=b['outcome'], route=list(route)))
            route = []
    outcomes = Counter(x['outcome'] for x in completed if x['end'] == 'boundary')
    boundary_n = sum(outcomes.values())
    return dict(completed_episodes=len(completed), boundary_episodes=boundary_n,
        warp=outcomes['Warp'], plex=outcomes['Plex'],
        warp_fraction=outcomes['Warp']/boundary_n if boundary_n else None,
        cap_terminated=sum(x['end']=='cap' for x in completed),
        mean_completed_length=sum(x['length'] for x in completed)/len(completed) if completed else None,
        completed=completed, right_censored=dict(length=len(route)-1,route=route) if route else None,
        effects_by_source=effects)
