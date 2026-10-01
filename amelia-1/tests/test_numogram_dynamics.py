"""
test_numogram_dynamics.py -- tests for the D0-D3 dynamics contracts.
Run:  python -m unittest test_numogram_dynamics -v
"""

import ast
import os
import random
import unittest
from fractions import Fraction

import CanonicalNumogram as C
import GreenBookTranscription as G
import NumogramDynamics as D

HERE = os.path.dirname(os.path.abspath(__file__))
REG = D.registry()
NG = C.CanonicalNumogram()


def path_probability(contract, route):
    """Exact probability of following the zone sequence from a fresh start,
    summed over parallel edges (the next D3 state depends on the edge type)."""
    return _rest(contract, D.State(route[0], None), route, 0)


def _rest(contract, state, route, t0):
    if len(route) == 1:
        return Fraction(1)
    total = Fraction(0)
    for e, q in contract.probabilities(state, t0):
        if e.dst == route[1]:
            total += q * _rest(contract, D.State(e.dst, e.type), route[1:], t0 + 1)
    return total


class TestLaws(unittest.TestCase):
    def test_probabilities_are_exact_distributions(self):
        for key, c in REG.items():
            for s in c.states():
                for t in range(0, 40):
                    probs = (c.exact_probabilities(s, t) if isinstance(c, D.D2GatedChannels)
                             else c.probabilities(s, t))
                    self.assertEqual(sum(p for _, p in probs), 1, (key, s, t))
                    self.assertTrue(all(p > 0 for _, p in probs))

    def test_d0_uniform_one_third(self):
        for z in C.ZONES:
            probs = REG["D0"].probabilities(D.State(z))
            self.assertEqual([p for _, p in probs], [Fraction(1, 3)] * 3)

    def test_d1_weights_and_constraint(self):
        probs = dict((e.type, p) for e, p in REG["D1"].probabilities(D.State(8)))
        self.assertEqual(probs, {C.CURRENT: Fraction(1, 2), C.SYZYGY: Fraction(1, 4),
                                 C.GATE: Fraction(1, 4)})
        with self.assertRaises(ValueError):
            D.D1TypedWeights(1, 1, 1)          # currents must outweigh gates
        with self.assertRaises(ValueError):
            D.D1TypedWeights(2, 0, 1)

    def test_d2a_schedule(self):
        c = REG["D2a"]
        self.assertEqual(c.period(), 1260)
        open_at = lambda t: sorted(e.label for z in C.ZONES
                                   for e, _ in c.exact_probabilities(D.State(z), t)
                                   if e.type == C.GATE)
        self.assertEqual(open_at(0), ["Gt-01"])            # no synchronised first step
        self.assertEqual(open_at(2), ["Gt-01", "Gt-03"])   # Gt-03 on steps 3, 6, 9, ...
        self.assertNotIn("Gt-00", open_at(1259))
        self.assertEqual(len(open_at(1259)), 9)            # all nine meet once per period
        self.assertIn("Gt-36", {e.label for e, _ in c.exact_probabilities(D.State(8), 35)})

    def test_d2b_exact_marginals(self):
        probs = {e.type: p for e, p in REG["D2b"].exact_probabilities(D.State(8), 5)}
        q = Fraction(1, 36)
        self.assertEqual(probs[C.GATE], q / 3)
        self.assertEqual(probs[C.SYZYGY], q / 3 + (1 - q) / 2)

    def test_d3_rule(self):
        c = REG["D3"]
        fresh = {e.type for e, _ in c.probabilities(D.State(2, None))}
        after_cross = {e.type for e, _ in c.probabilities(D.State(2, C.SYZYGY))}
        after_gate = {e.type for e, _ in c.probabilities(D.State(2, C.GATE))}
        self.assertEqual(fresh, {C.SYZYGY, C.GATE})
        self.assertEqual(after_cross, {C.SYZYGY, C.CURRENT, C.GATE})
        self.assertEqual(after_gate, {C.SYZYGY, C.GATE})
        warp = {e.type for e, _ in c.probabilities(D.State(6, None))}
        self.assertEqual(warp, {C.SYZYGY, C.CURRENT, C.GATE})

    def test_d3_reaches_printed_rites(self):
        """Every printed rite except the sentinel's [256] has positive probability
        under D3 when started fresh; [256] has probability zero."""
        c = REG["D3"]
        zero = []
        for e in G.MATRIX:
            for (_, r, _, _) in e["rites"]:
                if r in ("X", "?"):
                    continue
                if path_probability(c, [int(ch) for ch in r]) == 0:
                    zero.append(r)
        self.assertEqual(zero, ["256"])


class TestStructureAndAnalysis(unittest.TestCase):
    def test_warp_and_plex_are_closed_under_every_law(self):
        for key, c in REG.items():
            self.assertTrue(D.closed_region_check(c), key)

    def test_absorption_exact(self):
        a0 = D.absorption(REG["D0"])
        for z, r in a0.items():
            self.assertEqual(r["p_warp"] + r["p_plex"], 1)
        self.assertEqual(a0[8]["expected_steps_in_time_circuit"], 7)
        self.assertEqual(a0[2]["p_warp"], Fraction(29, 36))
        a3 = D.absorption(REG["D3"])
        self.assertEqual(a3[8]["p_plex"], Fraction(149, 184))

    def test_absorption_matches_simulation(self):
        c = REG["D0"]
        rng = random.Random(20260928)
        n, warp = 20000, 0
        for _ in range(n):
            s, t = D.State(2), 0
            while NG.region_of_zone[s.zone] == C.REGION_TC:
                _, s = c.step(s, t, rng)
                t += 1
            warp += NG.region_of_zone[s.zone] == C.REGION_WARP
        self.assertAlmostEqual(warp / n, 29 / 36, delta=0.015)


class TestContracts(unittest.TestCase):
    def test_reproducible_traces(self):
        c = REG["D3"]
        a, b = c.run(1, 200, seed=7), c.run(1, 200, seed=7)
        self.assertEqual(a.digest(), b.digest())
        self.assertNotEqual(a.digest(), c.run(1, 200, seed=8).digest())
        z = a.zones()
        for u, v in zip(z, z[1:]):
            self.assertTrue(NG.step_types(u, v) or u == v)

    def test_hash_covers_parameters_and_structure(self):
        h = {k: c.contract_hash() for k, c in REG.items()}
        self.assertEqual(len(set(h.values())), len(h))
        self.assertNotEqual(D.D1TypedWeights(2, 1, 1).contract_hash(),
                            D.D1TypedWeights(3, 1, 1).contract_hash())
        self.assertNotEqual(D.D0Uniform(gt00=D.GT00_EXCLUDE).contract_hash(), h["D0"])
        self.assertEqual(REG["D0"].declaration()["canonical_digest"], C.CanonicalNumogram().digest())

    def test_provenance(self):
        for key, c in REG.items():
            deps = c.provenance_dependencies()
            self.assertEqual(deps["SOURCE_CONFLICT"], [], key)
            self.assertEqual(deps["PROGRAMME_INFERRED"], ["lemurian_traversal"] if key == "D3" else [],
                             key)

    def test_preregistration_sealed(self):
        self.assertEqual(REG["D1"].parameters()["w_current"], 2)
        self.assertEqual(D.D1_PRIMARY_WEIGHTS, (2, 1, 1))
        self.assertEqual(set(REG), {"D0", "D1", "D2a", "D2b", "D3"})
        self.assertEqual(D.family_hash(), D.family_hash())
        self.assertNotEqual(D.family_hash(), D.family_hash(gt00=D.GT00_EXCLUDE))

    def test_source_branches_gt00(self):
        br = D.source_branches(D.D0Uniform)
        self.assertEqual(len(br[D.GT00_EXCLUDE].edges[0]), 2)
        vals = {k: float(D.absorption(c)[8]["p_plex"]) for k, c in br.items()}
        concl = {k: v > 0.5 for k, v in vals.items()}
        self.assertEqual(D.classify_robustness(vals, concl), "source-robust")
        self.assertEqual(D.classify_robustness({"a": 0.6, "b": 0.4}, {"a": True, "b": False}),
                         "source-dependent")
        self.assertEqual(D.classify_robustness({"a": 0.7, "b": 0.6}, {"a": True, "b": True}),
                         "source-sensitive")


class TestGraphGenericity(unittest.TestCase):
    def test_canonical_graph_matches_engine(self):
        g = D.canonical_graph()
        self.assertEqual(len(g.edges), 30)
        self.assertEqual(sorted(e.key() for e in g.edges),
                         sorted("%s:%d->%d" % (e["type"], e["src"], e["dst"]) for e in NG.typed_edges()))
        self.assertEqual([sorted(c) for c in REG["D0"].terminal], [[0, 9], [3, 6]])
        self.assertEqual(REG["D3"].transient, frozenset({1, 2, 4, 5, 7, 8}))

    def test_structural_d3_equals_rite_rule_on_canonical(self):
        """D3 stated structurally (transient node) is the engine's lemurian rule."""
        for e in G.MATRIX:
            for (_, r, _, _) in e["rites"]:
                if r in ("X", "?"):
                    continue
                z = [int(ch) for ch in r]
                self.assertEqual(path_probability(REG["D3"], z) > 0,
                                 NG.is_valid_route(z, C.RULE_LEMURIAN), r)

    def test_law_hash_is_graph_independent(self):
        ring = D.TypedGraph(n=10, edges=tuple(D.Edge(z, (z + 1) % 10, C.SYZYGY, "s") for z in range(10)),
                            family="test")
        a, b = D.D0Uniform(), D.D0Uniform(ring)
        self.assertEqual(a.law_hash(), b.law_hash())
        self.assertNotEqual(a.contract_hash(), b.contract_hash())

    def test_hold_when_nothing_permitted(self):
        g = D.TypedGraph(n=3, edges=(D.Edge(0, 1, C.CURRENT, "c"), D.Edge(1, 2, C.SYZYGY, "s"),
                                     D.Edge(2, 2, C.SYZYGY, "s")), family="test")
        c = D.D3Lemurian(g)
        self.assertEqual(c.transient, frozenset({0, 1}))
        e, s = c.step(D.State(0, None), 0, random.Random(0))
        self.assertIsNone(e)
        self.assertEqual(s, D.State(0, D.HOLD))


class TestDiscipline(unittest.TestCase):
    def _code_constants(self, filename):
        with open(os.path.join(HERE, filename), encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                body = getattr(node, "body", [])
                if body and isinstance(body[0], ast.Expr) and isinstance(
                        getattr(body[0], "value", None), ast.Constant):
                    docstrings.add(id(body[0].value))
        consts = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Tuple) and all(isinstance(x, ast.Constant) for x in node.elts):
                consts.append(tuple(x.value for x in node.elts))
            if isinstance(node, ast.Constant) and id(node) not in docstrings:
                consts.append(node.value)
        return consts, tree

    def test_no_special_case_for_the_sentinel(self):
        for f in ("CanonicalNumogram.py", "NumogramDynamics.py"):
            consts, _ = self._code_constants(f)
            self.assertNotIn((6, 2), consts, f)
            self.assertNotIn("6::2", consts, f)

    def test_dynamics_reads_no_matrix_attribute_or_print(self):
        _, tree = self._code_constants("NumogramDynamics.py")
        mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        mods |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        self.assertFalse(mods & {"GreenBookTranscription", "FidelityAssay"})
        attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        self.assertFalse(attrs & {"demons", "demon_by_mesh", "rites", "nests"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
