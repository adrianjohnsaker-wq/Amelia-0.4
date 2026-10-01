"""
test_canonical_numogram.py -- tests for Canonical Numogram 1.1, the Green Book
transcription and Fidelity Assay 2.0. Standard library only.

Run:  python -m unittest test_canonical_numogram -v
"""

import ast
import os
import unittest

import CanonicalNumogram as C
import FidelityAssay as FA
import GreenBookTranscription as G

HERE = os.path.dirname(os.path.abspath(__file__))


def _imports(filename):
    with open(os.path.join(HERE, filename), "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    return mods


NG = C.CanonicalNumogram()


class TestArithmetic(unittest.TestCase):
    def test_cumulation(self):
        self.assertEqual([C.cumulation(n) for n in range(10)],
                         [0, 1, 3, 6, 10, 15, 21, 28, 36, 45])

    def test_reduction_paths(self):
        self.assertEqual(C.reduction_path(28), (28, 10, 1))
        self.assertEqual(C.reduction_path(36), (36, 9))
        self.assertEqual(C.digital_reduction(0), 0)

    def test_twin(self):
        for z in C.ZONES:
            self.assertEqual(z + C.twin(z), 9)
        with self.assertRaises(ValueError):
            C.twin(10)

    def test_prime_ordination(self):
        """Green Book: zeroth prime = 1, first prime = 2, second prime = 3."""
        self.assertEqual([C.nth_prime(n) for n in range(5)], [1, 2, 3, 5, 7])


class TestNumogram(unittest.TestCase):
    def test_syzygies(self):
        self.assertEqual([s.label for s in NG.syzygies], ["9::0", "8::1", "7::2", "6::3", "5::4"])

    def test_currents_named_from_green_book(self):
        expected = {"Plex": ((9, 0), 9), "Surge": ((8, 1), 7), "Hold": ((7, 2), 5),
                    "Warp": ((6, 3), 3), "Sink": ((5, 4), 1)}
        for name, (syz, tractor) in expected.items():
            c = NG.current_named(name)
            self.assertEqual((c.syzygy, c.tractor), (syz, tractor))

    def test_time_systems(self):
        self.assertEqual(NG.time_circuit_cycle, ((8, 1), (7, 2), (5, 4)))
        self.assertEqual(NG.autonomous_loops, frozenset({(6, 3), (9, 0)}))
        self.assertEqual(NG.binary_cycle, (1, 2, 4, 8, 7, 5))

    def test_region_ordinals_follow_binary_cycle(self):
        order = sorted((zi.region_ordinal, z) for z, zi in NG.zone_info.items()
                       if zi.region == C.REGION_TC)
        self.assertEqual([z for _, z in order], [1, 2, 4, 8, 7, 5])

    def test_gates(self):
        expected = {0: 0, 1: 1, 2: 3, 3: 6, 4: 1, 5: 6, 6: 3, 7: 1, 8: 9, 9: 9}
        self.assertEqual({z: g.target for z, g in NG.gates.items()}, expected)

    def test_gate_status(self):
        self.assertEqual([g.number for g in NG.gates.values() if g.disputed], [0])
        self.assertEqual(sorted(g.number for g in NG.gates.values() if g.involutionary), [0, 1, 45])
        orient = {g.number: g.orientation for g in NG.gates.values() if g.orientation}
        self.assertEqual(orient, {10: "pro", 28: "counter"})


class TestMatrix(unittest.TestCase):
    def test_mesh_is_sequential(self):
        self.assertEqual(sorted(d.mesh for d in NG.demons.values()), list(range(45)))

    def test_classes(self):
        from collections import Counter
        c = Counter(d.demon_class for d in NG.demons.values())
        self.assertEqual(c, Counter({"Amphidemon": 24, "Cyclic Chronodemon": 12,
                                     "Syzygetic Chronodemon": 3, "Chaotic Xenodemon": 4,
                                     "Syzygetic Xenodemon": 2}))

    def test_prowl_and_shadow_definitions(self):
        prowls = {d.net_span for d in NG.demons.values() if "Sink" in d.prowls}
        shadows = {d.net_span for d in NG.demons.values() if "Sink" in d.shadows}
        self.assertEqual(prowls, {"4::1", "5::1"})
        self.assertEqual(shadows, {"8::4", "8::5"})

    def test_clicks_and_ciphers(self):
        clicked = {d.net_span: d.click_gates for d in NG.demons.values() if d.click_gates}
        self.assertEqual(len(clicked), 9)
        self.assertEqual(NG.demons[(1, 0)].net_span_click_gates, (10,))
        self.assertEqual(NG.demons[(6, 0)].cipher_gates, frozenset({6}))

    def test_pitch_rule_range_and_symmetry(self):
        from collections import Counter
        p = Counter(d.pitch for d in NG.demons.values())
        self.assertEqual((min(p), max(p), len(p)), (-7, 7, 15))
        self.assertTrue(all(p[k] == p[-k] for k in range(1, 8)))
        self.assertEqual(NG.demons[(4, 3)].pitch_label, "Ana-7")
        self.assertEqual(NG.demons[(6, 5)].pitch_label, "Cth-7")

    def test_imps(self):
        self.assertEqual(sum(d.imps_allotted for d in NG.demons.values()), 120)
        self.assertEqual(NG.demons[(5, 4)].imps_hosted, 10)


class TestProvenanceSeparation(unittest.TestCase):
    def test_inferred_haunt_kept_out_of_canonical(self):
        d = NG.demons[(9, 0)]
        self.assertEqual((d.haunts, d.direct_nesting_haunts), ((), (45,)))
        self.assertEqual(NG.to_spec()["matrix"]["Mesh-36"]["haunts"], [])
        self.assertIn("9::0", NG.to_spec(include_inferred=True)["inferred"]["direct_nesting_haunts"])

    def test_inferred_rule_change_leaves_canonical_digest(self):
        class AltPitch(C.CanonicalNumogram):
            @staticmethod
            def _pitch(z):
                return z
        alt = AltPitch()
        self.assertEqual(alt.digest(), NG.digest())
        self.assertNotEqual(alt.digest(include_inferred=True), NG.digest(include_inferred=True))


class TestMultigraph(unittest.TestCase):
    def test_summary(self):
        m = NG.multigraph_summary()
        self.assertEqual(m["edges"], 30)
        self.assertEqual(m["by_type"], {C.SYZYGY: 10, C.CURRENT: 10, C.GATE: 10})
        self.assertEqual(m["self_loops"], [(C.CURRENT, 3), (C.CURRENT, 9), (C.GATE, 0),
                                           (C.GATE, 1), (C.GATE, 9)])
        self.assertEqual(m["parallel"], {"0->9": [C.CURRENT, C.SYZYGY],
                                         "3->6": [C.GATE, C.SYZYGY],
                                         "4->1": [C.CURRENT, C.GATE],
                                         "6->3": [C.CURRENT, C.GATE, C.SYZYGY],
                                         "9->9": [C.CURRENT, C.GATE]})

    def test_typed_degrees(self):
        deg = NG.typed_degrees()
        for t in (C.SYZYGY, C.CURRENT, C.GATE):
            self.assertEqual(sum(deg[z][t][0] for z in C.ZONES), 10)
            self.assertEqual(sum(deg[z][t][1] for z in C.ZONES), 10)
        self.assertEqual(deg[1][C.GATE], (3, 1))      # Gt-01 loop, Gt-10, Gt-28 end in Zone-1
        self.assertEqual(deg[9][C.CURRENT], (2, 1))   # 0->9 and the 9->9 loop


class TestRoutes(unittest.TestCase):
    def test_gate_possible_and_required(self):
        r41 = [r for r in NG.rites(4, 1) if r.route == (4, 1)][0]
        self.assertEqual((r41.gate_possible, r41.gate_required), (True, True))
        r541 = [r for r in NG.rites(5, 1) if r.route == (5, 4, 1)][0]
        self.assertEqual((r541.gate_possible, r541.gate_required), (True, False))

    def test_step_types(self):
        self.assertEqual(NG.step_types(1, 8), frozenset({C.SYZYGY}))
        self.assertEqual(NG.step_types(8, 9), frozenset({C.GATE}))
        self.assertEqual(NG.step_types(4, 1), frozenset({C.CURRENT, C.GATE}))
        self.assertEqual(NG.step_types(3, 5), frozenset())

    def test_lemurian_rule(self):
        self.assertTrue(NG.is_valid_route([1, 8, 7, 2, 5, 4], C.RULE_LEMURIAN))
        self.assertFalse(NG.is_valid_route([1, 7, 2, 5, 4], C.RULE_LEMURIAN))
        self.assertTrue(NG.is_valid_route([1, 7, 2, 5, 4], C.RULE_PERMISSIVE))

    def test_warp_and_plex_are_closed(self):
        for a in (3, 6, 0, 9):
            for b in (1, 2, 4, 5, 7, 8):
                self.assertEqual(NG.routes(a, b), [])

    def test_lurgo_and_katak(self):
        self.assertEqual([r.route for r in NG.rites(1, 0)], [(1, 8, 9, 0)])
        self.assertEqual(sorted((r.route, r.kind) for r in NG.rites(5, 4)),
                         [((4, 1, 8, 7, 2, 5), "minor"), ((5, 4), "syzygetic")])
        self.assertEqual(NG.nests(1, 0), ((8, 0), (8, 1), (9, 0), (9, 1), (9, 8)))


class TestTranscription(unittest.TestCase):
    def test_complete_matrix(self):
        self.assertEqual([e["mesh"] for e in G.MATRIX], list(range(45)))
        self.assertTrue(all(e["line"] for e in G.MATRIX))

    def test_source_recorded(self):
        self.assertEqual(len(G.SOURCE["extraction_sha256"]), 64)

    def test_extraction_hash_if_present(self):
        path = os.path.join(HERE, "gb", "ccru_writings.txt")
        if not os.path.exists(path):
            self.skipTest("Green Book extraction not present")
        import hashlib
        with open(path, "rb") as fh:
            self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), G.SOURCE["extraction_sha256"])

    def test_names_blinded(self):
        with self.assertRaises(G.BlindingError):
            G.demon_names()
        self.assertEqual(len(G.demon_names(unblind=True)), 45)


class TestAssay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = FA.run()

    def test_tier_a_verdict(self):
        a = self.rep["tier_a"]
        self.assertEqual(a["unregistered_failures"], [])
        self.assertEqual(a["verdict"], "PASS_WITH_REGISTERED_DEVIATIONS")

    def test_registered_deviations_are_exactly_these(self):
        self.assertEqual(sorted(self.rep["tier_a"]["registered_deviations"]), sorted([
            "matrix.4::0.clicks", "matrix.5::0.clicks", "matrix.6::0.clicks",
            "matrix.7::0.clicks", "matrix.8::0.clicks", "matrix.6::0.ciphers",
            "matrix.8::4.prowls", "matrix.8::4.shadows"]))

    def test_every_deviation_is_used(self):
        used = set(self.rep["tier_a"]["registered_deviations"])
        self.assertEqual(used, set(FA.KNOWN_DEVIATIONS))

    def test_tier_b_fit_regression(self):
        fit = {k: (v["pass"], v["total"]) for k, v in self.rep["tier_b"].items()}
        self.assertEqual(fit["pitch"], (46, 47))
        self.assertEqual(fit["zone_mesh_tag"], (10, 10))
        self.assertEqual(fit["phase_population"], (9, 9))
        self.assertEqual(fit["sub_rites"], (74, 80))
        self.assertEqual(fit["lemurian_traversal"], (123, 129))
        self.assertEqual(fit["direct_nesting_haunt"], (45, 45))
        self.assertEqual(fit["secret_gate_required"], (30, 31))
        self.assertEqual(fit["secret_gate_possible"], (22, 31))

    def test_every_tier_b_failure_has_a_note(self):
        for f in self.rep["tier_b_failures"]:
            self.assertTrue(f["note"], f["id"])


class TestIntegrity(unittest.TestCase):
    def test_engine_has_no_dynamics_or_transcription(self):
        mods = _imports("CanonicalNumogram.py")
        self.assertFalse(mods & {"random", "numpy", "torch", "secrets", "time",
                                 "GreenBookTranscription", "FidelityAssay"})

    def test_transcription_is_data_only(self):
        self.assertEqual(_imports("GreenBookTranscription.py"), set())

    def test_digests(self):
        self.assertEqual(NG.digest(), C.CanonicalNumogram().digest())
        self.assertNotEqual(NG.digest(), NG.digest(include_inferred=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
