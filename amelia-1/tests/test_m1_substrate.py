"""M1: substrate core. Mechanics only, on off-cohort seeds 907xx. No acceptance statistic."""
import ast
import os
import unittest

import NumogramDynamics as D
import NumogramInterface as I
import amelia_substrate as S

LAWS = ("D0", "D1", "D2a", "D2b", "D3")


def records(sub, n):
    return [sub.transact() for _ in range(n)]


class LawIdentity(unittest.TestCase):
    def test_zero_modulation_equals_sealed_interface(self):
        """beta = gamma = 0: every episode equals NumogramInterface.episode on the same stream."""
        for law in LAWS:
            itf = I.NumogramInterface(S.contract_for(law))
            for seed in (90701, 90702):
                sub = S.AmeliaSubstrate(seed, {"law": law, "beta": 0.0, "gamma": 0.0})
                for k in range(60):
                    z0 = sub.choose_entry()
                    self.assertEqual(z0, itf.iota(S._uniform("INGRESS", seed, k)))
                    ref = itf.episode(z0, I.episode_rng(seed, k))
                    got = sub.transact()
                    self.assertEqual(got["raw_digest"], ref.digest(), (law, seed, k))

    def test_fresh_trace_first_episode_is_unmodulated(self):
        itf = I.NumogramInterface(S.contract_for("D1"))
        sub = S.AmeliaSubstrate(90703)
        z0 = sub.choose_entry()
        self.assertEqual(sub.transact()["raw_digest"], itf.episode(z0, I.episode_rng(90703, 0)).digest())

    def test_edges_are_canonical(self):
        allowed = {(e.src, e.dst) for e in D.canonical_graph().edges}
        sub = S.AmeliaSubstrate(90704)
        for r in records(sub, 300):
            for a, b, t in r["passages"]:
                if t != D.HOLD:
                    self.assertIn((a, b), allowed)


class State(unittest.TestCase):
    def test_round_trip_is_bit_exact(self):
        a = S.AmeliaSubstrate(90711)
        full = records(a, 100)
        b = S.AmeliaSubstrate(90711)
        first = records(b, 60)
        c = S.AmeliaSubstrate.import_state(b.export_state())
        rest = records(c, 40)
        self.assertEqual(full, first + rest)
        self.assertEqual((a.digest_P(), a.digest_H()), (c.digest_P(), c.digest_H()))

    def test_fork_independence_and_identity(self):
        a = S.AmeliaSubstrate(90712)
        records(a, 50)
        b = a.fork()
        self.assertEqual(records(a, 30), records(b, 30))
        c = a.fork()
        records(c, 5)
        self.assertNotEqual(a.digest_P(), c.digest_P())

    def test_restore_present_leaves_trace(self):
        a, b = S.AmeliaSubstrate(90713), S.AmeliaSubstrate(90714)
        records(a, 80)
        records(b, 80)
        hb = b.digest_H()
        b.P["seed"] = a.P["seed"]
        b.restore_present(a.P)
        self.assertEqual(a.digest_P(), b.digest_P())
        self.assertEqual(b.digest_H(), hb)
        self.assertNotEqual(a.digest_H(), b.digest_H())

    def test_transplant_reproduces_future(self):
        a, b = S.AmeliaSubstrate(90715), S.AmeliaSubstrate(90716)
        records(a, 80)
        records(b, 80)
        c = b.fork()
        c.H = S.copy.deepcopy(a.H)
        c.restore_present(a.P)
        self.assertEqual(records(a.fork(), 40), records(c, 40))

    def test_trace_reaches_behaviour(self):
        """The TypeScript fault: different traces under identical P must be able to act on behaviour."""
        diverged = 0
        for i in range(5):
            a, b = S.AmeliaSubstrate(90720 + i), S.AmeliaSubstrate(90730 + i)
            records(a, 120)
            records(b, 120)
            b.restore_present(a.P)
            if records(a, 20) != records(b, 20):
                diverged += 1
        self.assertGreater(diverged, 0)

    def test_ablated_trace_equals_fresh(self):
        a = S.AmeliaSubstrate(90717)
        records(a, 50)
        a.H = a.empty_trace()
        f = S.AmeliaSubstrate(90717)
        f.restore_present(a.P)
        self.assertEqual(records(a, 30), records(f, 30))

    def test_import_rejects_tampered_state(self):
        a = S.AmeliaSubstrate(90718)
        records(a, 10)
        blob = a.export_state().replace('"k":10', '"k":11')
        with self.assertRaises(ValueError):
            S.AmeliaSubstrate.import_state(blob)


class Layers(unittest.TestCase):
    def test_l3_bistable_with_hysteresis(self):
        f = lambda x, h: x + 0.05 * (x - x * x * x + h)
        x = -1.0
        for _ in range(400):
            x = f(x, 0.0)
        self.assertLess(x, 0.0)
        for _ in range(400):
            x = f(x, 0.5)                  # beyond the fold at 0.385
        self.assertGreater(x, 0.0)
        for _ in range(400):
            x = f(x, 0.0)
        self.assertGreater(x, 0.0)         # stays: hysteresis

    def test_reconsolidation_rewrites_only_retrieved(self):
        sub = S.AmeliaSubstrate(90719)
        for _ in range(200):
            before = S.copy.deepcopy(sub.H["L2"]["traces"])
            r = sub.transact()
            if r["retrieved"]:
                after = {t["id"]: t for t in sub.H["L2"]["traces"]}
                changed = {t["id"] for t in before if t["id"] in after and t["content"] != after[t["id"]]["content"]}
                self.assertTrue(changed <= set(r["retrieved"]))
                self.assertTrue(changed)
                return
        self.fail("no retrieval in 200 episodes")

    def test_regions_are_structural(self):
        regs = S.regions_of(S.contract_for("D1"))
        self.assertEqual(regs, ((1, 2, 4, 5, 7, 8), (0, 9), (3, 6)))


class Determinism(unittest.TestCase):
    def test_no_transcendental_or_pow(self):
        path = os.path.join(os.path.dirname(S.__file__), "amelia_substrate.py")
        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        for node in ast.walk(tree):
            self.assertNotIsInstance(node, ast.Pow)
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "math":
                self.assertEqual(node.attr, "sqrt")


if __name__ == "__main__":
    unittest.main()
