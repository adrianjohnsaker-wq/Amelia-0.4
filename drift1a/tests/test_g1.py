import copy
import gzip
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))
from memory import CommitmentMemory, LegacyRetention, ProcessFieldMemory, norm
from drift_core import (Substrate, canonical_edges, digest, empty_history, keyed_uniform, rewire,
                        degree_signature, sample, verify_canonical)
from run_drift import run, synthetic_tape
from scoring import EProcess, OnlineLogistic, brier, synthetic_eligibility, describe
import drift_android


class Parity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = json.loads(gzip.decompress((ROOT / 'evidence/ts_fixtures.json.gz').read_bytes()))

    def same(self, x, y):
        if isinstance(x, dict):
            self.assertEqual(set(x), set(y))
            for k in x:
                self.same(x[k], y[k])
        elif isinstance(x, list):
            self.assertEqual(len(x), len(y))
            for a, b in zip(x, y):
                self.same(a, b)
        elif type(x) in (int, float) and type(y) in (int, float):
            self.assertAlmostEqual(x, y, delta=1e-12)
        else:
            self.assertEqual(x, y)

    def test_commitment_ts_parity(self):
        for case in self.fixtures['commitment']:
            c = CommitmentMemory()
            c.save('key', case['input'])
            self.same(case['stored'], c.states.get('key'))
            for b in case['biases']:
                self.same(b['bias'], c.bias('key', case['input']['sourceZone'], b['step']))

    def test_retention_legacy_ts_parity(self):
        r = LegacyRetention()
        for c in self.fixtures['retention']:
            self.same(c['output'], r.apply(c['zone'], c['raw'], c['depth']))
            self.same(c['telemetry'], r.last)

    def test_field_ts_parity(self):
        f = ProcessFieldMemory()
        for c in self.fixtures['field']:
            self.same(c['modulation'], f.update(c['input']))
            self.same(c['state'], f.state)

    def test_legacy_selector_ts_parity(self):
        for c in self.fixtures['selector']:
            r = LegacyRetention()
            d = dict(c['scores'])
            d['zone-2-flux'] = r.apply('zone-2-flux', d['zone-2-flux'], c['depth'])
            d = norm(d)
            self.same(c['adjusted'], d)
            chosen = list(d)[sample(list(d.values()), c['u'])]
            self.assertEqual(c['selected'], chosen)

    def test_self_loop_probability_ts_parity(self):
        for c in self.fixtures['self_loop']:
            self.same(c['value'], c['scores'].get(c['zone'], 0) / sum(c['scores'].values()))


class G1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edges = canonical_edges()
        cls.control = rewire(cls.edges)

    def test_sealed_canonical_bytes(self):
        self.assertTrue(verify_canonical()['ok'])

    def test_typed_rewire_degrees_and_loops(self):
        self.assertEqual(degree_signature(self.edges), degree_signature(self.control))
        self.assertNotEqual(self.edges, self.control)
        self.assertEqual(self.control, rewire(self.edges))

    def test_all_start_zones_and_graphs_legal(self):
        for edges in (self.edges, self.control):
            allowed = {json.dumps(e) for e in edges}
            for start in range(10):
                s = Substrate(edges, start)
                for tick, x in enumerate(synthetic_tape(start, 80)):
                    r = s.advance(keyed_uniform(x, tick))
                    self.assertIn(json.dumps(r['selected_edge']), allowed)
                    self.assertEqual(r['selected_edge'][0], start if tick == 0 else prior)
                    prior = r['selected_edge'][1]
                    self.assertAlmostEqual(sum(r['selection']['probabilities']), 1)

    def test_d1_prior_matches_sealed_fraction_law(self):
        import NumogramDynamics as D
        law = D.registry()['D1']
        for zone in range(10):
            s = Substrate(self.edges, zone)
            observed = s.distribution()
            original = law.probabilities(D.State(zone))
            self.assertEqual(observed['candidates'], [e.as_list() for e, p in original])
            self.assertEqual(observed['base'], [float(p) for e, p in original])

    def test_disputed_gate_exclusion_and_no_added_self_loop(self):
        s = Substrate(self.edges, 0, {'gt00': 'exclude'})
        s.H['retention']['0'] = dict(above=True, activation_tick=0, expiry_tick=500)
        d = s.distribution()
        self.assertTrue(all(e[1] == 9 for e in d['candidates']))
        self.assertFalse(d['retention']['floor_applied'])

    def test_no_zone2_loop_even_with_corrupt_preference(self):
        s = Substrate(self.edges, 2)
        s.H['retention']['2'] = dict(above=True, activation_tick=0, expiry_tick=999)
        for e in s.distribution()['candidates']:
            self.assertNotEqual(e[1], 2)

    def test_distribution_and_governor_do_not_mutate(self):
        s = Substrate(self.edges, 9)
        for _ in range(6):
            s.advance(.9)
        before = s.snapshot()
        s.distribution()
        self.assertEqual(before, s.snapshot())

    def test_candidate_predictions_use_same_prior_and_commit_selected(self):
        s = Substrate(self.edges, 9)
        r = s.advance(.9)
        selected = next(g for g in r['selection']['governor'] if g['edge'] == r['selected_edge'])
        self.assertEqual(selected['predicted_field'], s.H['field'])
        self.assertEqual(r['memory_read_digest'], digest(empty_history()))
        self.assertEqual(s.H['updates'], 1)

    def test_governor_evaluates_and_reweights_candidates(self):
        s = Substrate(self.edges, 9)
        s.H['field']['compressionDebt'] = .8
        s.H['observations']['9'] = [9] * 8
        d = s.distribution()
        costs = [x['cost'] for x in d['governor']]
        self.assertGreater(max(costs), min(costs))
        self.assertEqual(len(costs), len(d['candidates']))
        self.assertNotEqual(d['base'], d['probabilities'])

    def test_retention_final_probability_floor(self):
        s = Substrate(self.edges, 1)
        s.H['retention']['1'] = dict(above=True, activation_tick=0, expiry_tick=500)
        d = s.distribution()
        self.assertTrue(d['retention']['floor_applied'])
        self.assertAlmostEqual(d['retention']['final'], .4)

    def test_retention_global_expiry_no_stale_reactivation(self):
        s = Substrate(self.edges, 9, dict(retention_steps=3))
        s.advance(.99)  # qualify; first active read tick 1
        self.assertTrue(s.distribution()['retention']['active'])
        for _ in range(3):
            s.advance(.99)
        self.assertEqual(s.P['tick'], 4)
        self.assertFalse(s.distribution()['retention']['active'])
        s.advance(.99)
        self.assertFalse(s.distribution()['retention']['active'])

    def test_retention_rearms_only_after_new_threshold_crossing(self):
        s = Substrate(self.edges, 1, dict(retention_steps=1, window=1))
        s.advance(.99)  # zone 1 self-loop
        s.advance(0.0)  # leave zone 1; observation goes below threshold
        s.P['zone'] = 1  # matched-state test intervention
        s.advance(.99)
        self.assertTrue(s.distribution()['retention']['active'])

    def test_complete_reset_matches_fresh_history_at_same_present(self):
        s = Substrate(self.edges, 9)
        for _ in range(20):
            s.advance(.99)
        self.assertTrue(s.H['commitment'])
        fresh = Substrate(self.edges, s.P['zone'])
        fresh.P = copy.deepcopy(s.P)
        s.reset_memory()
        self.assertEqual(s.H, empty_history())
        self.assertEqual(s.distribution(), fresh.distribution())
        self.assertEqual(s.advance(.3), fresh.advance(.3))

    def test_reset_every_tick_discards_all_history_before_read(self):
        s = Substrate(self.edges, 9)
        for i in range(20):
            r = s.advance(.99, reset=True)
            self.assertEqual(r['memory_read_digest'], digest(empty_history()))
            self.assertEqual(s.H['updates'], 1)
            self.assertFalse(r['selection']['commitment_bias'])
            self.assertFalse(r['selection']['retention']['active'])

    def test_same_present_different_memory_changes_distribution(self):
        s = Substrate(self.edges, 9)
        for _ in range(20):
            s.advance(.99)
        blank = Substrate(self.edges, s.P['zone'])
        blank.P = copy.deepcopy(s.P)
        a, b = s.distribution(), blank.distribution()
        self.assertTrue(a['commitment_bias'])
        self.assertEqual(a['candidates'], b['candidates'])
        self.assertNotEqual(a['probabilities'], b['probabilities'])
        # A concrete identical variate produces different next edges.
        bounds_a, bounds_b = [], []
        for probs, out in ((a['probabilities'], bounds_a), (b['probabilities'], bounds_b)):
            total = 0
            for p in probs[:-1]:
                total += p
                out.append(total)
        cuts = sorted(set([0.0, 1.0] + bounds_a + bounds_b))
        self.assertTrue(any(sample(a['probabilities'], (x+y)/2) != sample(b['probabilities'], (x+y)/2)
                            for x, y in zip(cuts, cuts[1:])))

    def test_variate_is_operation_keyed_and_candidate_count_independent(self):
        x = 'ab' * 32
        s = Substrate(self.edges)
        u = keyed_uniform(x, 7)
        for _ in range(50):
            s.distribution()
        self.assertEqual(u, keyed_uniform(x, 7))
        self.assertNotEqual(u, keyed_uniform(x, 7, 'another_operation'))

    def test_sampling_boundaries_and_invalid_input(self):
        self.assertEqual(sample([0, .5, .5], 0), 1)
        self.assertEqual(sample([0, .5, .5], .5), 2)
        for u in (-1, 1, float('nan'), float('inf'), True):
            with self.assertRaises(ValueError):
                sample([.5, .5], u)
        s = Substrate(self.edges)
        before = s.snapshot()
        with self.assertRaises(ValueError):
            s.advance(float('nan'), reset=True)
        self.assertEqual(before, s.snapshot())

    def test_checkpoint_resume_exact_and_tamper_rejected(self):
        s = Substrate(self.edges, 9)
        for _ in range(8):
            s.advance(.99)
        snap = s.snapshot()
        b = Substrate.restore(snap)
        for u in (.8, .4, .1, .9):
            self.assertEqual(s.advance(u), b.advance(u))
        snap['H']['field']['compressionDebt'] = .99
        with self.assertRaises(ValueError):
            Substrate.restore(snap)

    def test_android_boundary_roundtrip(self):
        blob = drift_android.initialize(9)
        x = '12' * 32
        a = json.loads(drift_android.advance(blob, x))
        s = Substrate.restore(json.loads(blob))
        r = s.advance(keyed_uniform(x, 0))
        self.assertEqual(r, a['event'])
        self.assertEqual(s.snapshot(), a['snapshot'])
        self.assertEqual(json.loads(drift_android.inspect(blob)), Substrate.restore(json.loads(blob)).distribution())

    def test_runner_replay_and_shared_variates(self):
        with tempfile.TemporaryDirectory() as p:
            tape = synthetic_tape(101, 12)
            first = run(p, tape)
            self.assertEqual(first, run(p, tape))
            for path in Path(p).glob('tick_*.json'):
                d = json.loads(path.read_text())
                self.assertEqual(len({x['u'] for x in d['events'].values()}), 1)
            with self.assertRaises(ValueError):
                run(p, synthetic_tape(102, 12))
            path = Path(p) / 'tick_000005.json'
            path.write_text(path.read_text().replace('"tick":5', '"tick":55', 1))
            with self.assertRaises(ValueError):
                run(p, tape)

    def test_single_writer_lock(self):
        with tempfile.TemporaryDirectory() as p:
            (Path(p) / 'writer.lock').touch()
            with self.assertRaises(FileExistsError):
                run(p, synthetic_tape(1, 1))

    def test_metrics_and_censoring(self):
        records = [dict(selected_edge=[0, z, 'gate', 'x', None, False],
                   selection=dict(commitment_bias=None, retention=dict(floor_applied=False), governor=[]))
                   for z in [9, 9, 0, 9]]
        m = describe(records, self.edges)
        self.assertEqual(m['occupancy'][9], .75)
        self.assertEqual(m['longest_zone9_run'], 2)
        self.assertEqual(m['unique_four_zone_words'], 1)
        self.assertTrue(m['dwell'][0]['left_censored'])
        self.assertTrue(m['dwell'][-1]['right_censored'])

    def test_brier_eprocess_and_temporal_leakage(self):
        self.assertAlmostEqual(brier(.75, 1), .0625)
        e = EProcess()
        e.update(True)
        self.assertAlmostEqual(math.exp(e.log_e()), (1.02 + 1.05 + 1.10)/3)
        e.update(False)
        self.assertAlmostEqual(math.exp(e.log_e()), (1.02*.98 + 1.05*.95 + 1.1*.9)/3)
        self.assertTrue(synthetic_eligibility(0, 100, 600, 600))
        self.assertFalse(synthetic_eligibility(0, 599, 600, 600))
        self.assertFalse(synthetic_eligibility(0, 100, 600, 599))
        self.assertFalse(synthetic_eligibility(0, 100, 600, 600, catch_up=True))
        learner = OnlineLogistic(2)
        self.assertEqual(learner.predict([0, 0]), .5)
        with self.assertRaises(ValueError):
            learner.learn(0, [1, 0], .5, 1, 600, 600)
        learner.learn(0, [1, 0], .5, 1, 600, 601)
        with self.assertRaises(ValueError):
            learner.learn(0, [1, 0], .5, 1, 600, 700)


if __name__ == '__main__':
    unittest.main(verbosity=2)
