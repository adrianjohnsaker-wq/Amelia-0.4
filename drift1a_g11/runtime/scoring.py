"""Offline scoring utilities. No live-beacon or witness verification is claimed."""
import math
from collections import Counter


def brier(p, outcome):
    if not math.isfinite(p) or not 0 <= p <= 1 or type(outcome) is not int or outcome not in (0, 1):
        raise ValueError('invalid prediction/outcome')
    return (p - outcome) ** 2


class EProcess:
    def __init__(self):
        self.logs = [0.0, 0.0, 0.0]
        self.n = 0

    def update(self, hit):
        if type(hit) is not bool:
            raise ValueError('hit must be bool')
        for i, rate in enumerate((.02, .05, .10)):
            self.logs[i] += math.log1p(rate * (1 if hit else -1))
        self.n += 1
        return self.log_e()

    def log_e(self):
        m = max(self.logs)
        return m + math.log(sum(math.exp(x - m) for x in self.logs) / 3)


class OnlineLogistic:
    """Explicit-dimensional proposal; caller freezes features before registration."""
    def __init__(self, dimensions):
        self.weights = [0.0] * (dimensions + 1)
        self.seen = set()
        self.last_tick = -1

    def predict(self, features):
        if len(features) + 1 != len(self.weights) or any(not math.isfinite(x) for x in features):
            raise ValueError('invalid features')
        x = [1.0] + [max(-1, min(1, v)) for v in features]
        z = max(-20, min(20, sum(w * v for w, v in zip(self.weights, x))))
        return 1 / (1 + math.exp(-z))

    def learn(self, tick, features, committed_p, outcome, release_time, scheduled_now):
        if tick in self.seen or tick <= self.last_tick or release_time >= scheduled_now:
            raise ValueError('duplicate, out-of-order or unmatured training example')
        self.predict(features)  # schema validation
        brier(committed_p, outcome)
        x = [1.0] + [max(-1, min(1, v)) for v in features]
        # Draft convention: gradient uses the original committed probability.
        self.weights = [w - .01 * (committed_p - outcome) * v for w, v in zip(self.weights, x)]
        self.seen.add(tick)
        self.last_tick = tick


def synthetic_eligibility(scheduled_tick, receipt_time, target_release, target_read_time, catch_up=False):
    """Timing-logic fixture only: supplied timestamps are NOT independent receipts."""
    return (not catch_up and scheduled_tick <= receipt_time <= target_release - 60
            and target_read_time >= target_release)


def describe(records, allowed_edges):
    from drift_core import edge_id
    zones = [r['selected_edge'][1] for r in records]
    n = len(zones)
    occupancy = [zones.count(z) / n if n else 0 for z in range(10)]
    dwell = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and zones[j] == zones[i]:
            j += 1
        dwell.append(dict(zone=zones[i], length=j-i, left_censored=i == 0, right_censored=j == n))
        i = j
    edges = Counter(edge_id(r['selected_edge']) for r in records)
    by_source = {}
    for r in records:
        a, b = r['selected_edge'][:2]
        by_source.setdefault(a, Counter())[b] += 1
    h = 0.0
    for counts in by_source.values():
        total = sum(counts.values())
        h += total / n * -sum(c / total * math.log2(c / total) for c in counts.values())
    return dict(ticks=n, occupancy=occupancy, dwell=dwell,
                longest_zone9_run=max([x['length'] for x in dwell if x['zone'] == 9] or [0]),
                unique_typed_edges=len(edges), edge_fraction=len(edges) / len(allowed_edges),
                unique_four_zone_words=len({tuple(zones[i:i+4]) for i in range(max(0, n-3))}),
                conditional_entropy_bits=h,
                source_visit_counts={str(k): sum(v.values()) for k, v in by_source.items()},
                commitment_applications=sum(bool(r['selection']['commitment_bias']) for r in records),
                retention_floor_applications=sum(r['selection']['retention']['floor_applied'] for r in records),
                governor_reweighted_ticks=sum(len({g['multiplier'] for g in r['selection']['governor']}) > 1 for r in records))
