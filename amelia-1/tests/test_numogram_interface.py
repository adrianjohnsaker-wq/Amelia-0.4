"""
test_numogram_interface.py -- tests for the episodic interface (1.1).
Run:  python -m unittest test_numogram_interface -v
"""

import ast
import dataclasses
import os
import random
import unittest

import CanonicalNumogram as C
import NumogramDynamics as D
import NumogramInterface as I
import NullInterfaces as N

HERE = os.path.dirname(os.path.abspath(__file__))
ITF = I.primary_interfaces()


class Recorder(I.Embodiment):
    name = "recorder"

    def __init__(self, us):
        self.us, self.k, self.seen = list(us), 0, []

    def observe(self):
        u = self.us[self.k % len(self.us)]
        self.k += 1
        return u

    def update(self, packet):
        self.seen.append(packet)

    def state_digest(self):
        return "rec:%d" % self.k


class TestIngress(unittest.TestCase):
    def test_iota_is_topology_blind(self):
        itf = ITF["D0"]
        self.assertEqual([itf.iota(u) for u in (0.0, 0.099, 0.1, 0.55, 0.999, 1.0)], [0, 0, 1, 5, 9, 9])
        b12 = I.NumogramInterface(D.D0Uniform(N.n2_base(12)))
        self.assertEqual([b12.iota(u) for u in (0.0, 0.5, 0.99, 1.0)], [0, 6, 11, 11])
        with self.assertRaises(ValueError):
            itf.iota(1.01)


class TestPacket(unittest.TestCase):
    def test_schema_is_fixed_and_neutral(self):
        self.assertEqual(tuple(f.name for f in dataclasses.fields(I.ObservationPacket)), I.PACKET_FIELDS)
        for g in (D.canonical_graph(), N.n2_base(12), N.n2_base(8)):
            itf = I.NumogramInterface(D.D0Uniform(g))
            log = I.run_transactions(I.NullEmbodiment(1), itf, n=200, seed=2)
            for p in log.packets():
                self.assertTrue(all(0.0 <= v <= 1.0 for v in p.as_tuple()), g.family)

    def test_embodiment_receives_packets_only(self):
        emb = Recorder([0.15, 0.85])
        I.run_transactions(emb, ITF["D0"], n=10, seed=1)
        self.assertTrue(all(isinstance(p, I.ObservationPacket) for p in emb.seen))

    def test_packet_values(self):
        raw = I.RawEpisodeRecord("g", 10, 2, 3, (3, 6),
                                 ((0, 2, C.SYZYGY, "s", 7), (1, 7, C.GATE, "Gt-28", 1),
                                  (2, 1, C.SYZYGY, "s", 8), (3, 8, C.SYZYGY, "s", 1),
                                  (4, 1, C.SYZYGY, "s", 8)), False)
        p = I.make_packet(raw, 1260)
        self.assertAlmostEqual(p.entry_position, 2 / 9)
        self.assertAlmostEqual(p.edge_fraction_syzygy, 4 / 5)
        self.assertAlmostEqual(p.transition_recurrence, 1 / 5)   # 1->8 repeated once
        self.assertAlmostEqual(p.node_coverage, 4 / 10)


class TestEpisodes(unittest.TestCase):
    def test_canonical_episode_rules(self):
        itf = ITF["D0"]
        for k in range(300):
            z0 = k % 10
            raw = itf.episode(z0, I.episode_rng(5, k))
            self.assertGreaterEqual(raw.length, 1)
            self.assertFalse(raw.truncated)
            self.assertIn(raw.exit, (0, 3, 6, 9))
            if z0 in (0, 9, 3, 6):
                self.assertEqual(raw.length, 1)

    def test_terminal_classes_are_structural_under_d2(self):
        for g in N.family(seed=3).values():
            a = I.NumogramInterface(D.D0Uniform(g)).closed
            b = I.NumogramInterface(D.D2GatedChannels("D2a", g)).closed
            self.assertEqual(a, b, g.family)

    def test_no_truncation_under_primary_family(self):
        for k, itf in ITF.items():
            log = I.run_transactions(I.NullEmbodiment(3), itf, n=300, seed=4)
            self.assertEqual(log.truncation_rate(), 0.0, k)

    def test_d3_episodes_obey_traversal_rule(self):
        itf = ITF["D3"]
        for k in range(300):
            raw = itf.episode((1, 2, 4, 5, 7, 8)[k % 6], I.episode_rng(9, k))
            prev = None
            for (_, src, typ, _, _) in raw.steps:
                if typ == C.CURRENT and src in (1, 2, 4, 5, 7, 8):
                    self.assertEqual(prev, C.SYZYGY)
                prev = typ

    def test_strongly_connected_graph_truncates(self):
        ring = D.TypedGraph(10, tuple(D.Edge(z, (z + 1) % 10, C.SYZYGY, "s") for z in range(10)), "ring")
        itf = I.NumogramInterface(D.D0Uniform(ring), l_max=50)
        raw = itf.episode(2, random.Random(0))
        self.assertTrue(raw.truncated)
        self.assertEqual(raw.length, 50)

    def test_sink_entry_is_zero_length(self):
        g = D.TypedGraph(3, (D.Edge(0, 1, C.SYZYGY, "s"), D.Edge(1, 0, C.SYZYGY, "s")), "sink")
        itf = I.NumogramInterface(D.D0Uniform(g))
        raw = itf.episode(2, random.Random(0))
        self.assertEqual((raw.length, raw.exit, raw.truncated), (0, 2, False))

    def test_holds_are_recorded(self):
        g = D.TypedGraph(3, (D.Edge(0, 1, C.CURRENT, "c"), D.Edge(1, 2, C.SYZYGY, "s"),
                             D.Edge(2, 2, C.SYZYGY, "s")), "hold")
        itf = I.NumogramInterface(D.D3Lemurian(g), l_max=5)
        raw = itf.episode(0, random.Random(0))
        self.assertTrue(raw.truncated)
        self.assertEqual({s[2] for s in raw.steps}, {D.HOLD})


class TestTransactions(unittest.TestCase):
    def test_reproducible(self):
        itf = ITF["D2b"]
        a = I.run_transactions(Recorder([0.15, 0.45, 0.85]), itf, n=60, seed=21)
        b = I.run_transactions(Recorder([0.15, 0.45, 0.85]), itf, n=60, seed=21)
        self.assertEqual(a.digest(), b.digest())
        self.assertNotEqual(a.digest(), I.run_transactions(Recorder([0.15, 0.45, 0.85]), itf,
                                                           n=60, seed=22).digest())

    def test_episode_clock_keeps_interface_memoryless(self):
        itf = ITF["D2a"]
        first = itf.episode(2, I.episode_rng(1, 0))
        for k in range(20):
            itf.episode(5, I.episode_rng(2, k))
        self.assertEqual(itf.episode(2, I.episode_rng(1, 0)), first)

    def test_hashes(self):
        h = {k: itf.interface_hash() for k, itf in ITF.items()}
        self.assertEqual(len(set(h.values())), 5)
        self.assertNotEqual(I.NumogramInterface(D.D0Uniform(), l_max=64).interface_hash(), h["D0"])


class TestDiscipline(unittest.TestCase):
    def test_interface_reads_no_identity_or_canonical_labels(self):
        with open(os.path.join(HERE, "NumogramInterface.py"), encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        mods |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        self.assertFalse(mods & {"GreenBookTranscription", "FidelityAssay", "NullInterfaces"})
        attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        self.assertFalse(attrs & {"demons", "rites", "nests", "region_of_zone", "regions", "family"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
