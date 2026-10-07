"""Queue parser and restart-safety helpers. No network and no live-ledger mutation."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import queue_outside2 as Q

T32 = "T H T T H H T H T T T H H T H T H H T T H T T H H H T T H T H T"


class BatchParsing(unittest.TestCase):
    def parse(self, text, name="b.txt"):
        d = Path(tempfile.mkdtemp())
        (d / name).write_text(text)
        return Q.parse_requests(d)

    def test_spaces_comments_and_line(self):
        r = self.parse("# note\nW020 %s  # first\n\nW021 HTTTHHTHTHHTTTHHHTHTHTTHHTHTHTTH\n" % T32)
        self.assertEqual(r["W020"]["tosses"], T32.replace(" ", ""))
        self.assertEqual(sorted(r), ["W020", "W021"])
        self.assertEqual(r["W020"]["line"], 2)

    def test_short_cast_halts(self):
        with self.assertRaises(Q.Halt):
            self.parse("W020 HTTTHHTHTHHTTTHHHTHTHTTHHTHTHTT\n")

    def test_bad_character_halts(self):
        with self.assertRaises(Q.Halt):
            self.parse("W020 HTTTHHTHTHHTTTHHHTHTHTTHHTHTHTTX\n")

    def test_conflict_halts(self):
        with self.assertRaises(Q.Halt):
            self.parse("W020 %s\nW020 %s\n" % (T32, "T" * 32))

    def test_identical_repeat_is_harmless(self):
        self.assertEqual(len(self.parse("W020 %s\nW020 %s\n" %
                                        (T32, T32.replace(" ", "")))), 1)

    def test_bad_working_id_halts(self):
        with self.assertRaises(Q.Halt):
            self.parse("X020 %s\n" % T32)


class ImmutableEvidence(unittest.TestCase):
    def test_identical_existing_json_is_restart_safe(self):
        p = Path(tempfile.mkdtemp()) / "x.json"
        Q.write_once(p, {"a": 1, "b": [2, 3]})
        Q.write_once(p, {"b": [2, 3], "a": 1})

    def test_conflicting_existing_json_halts(self):
        p = Path(tempfile.mkdtemp()) / "x.json"
        Q.write_once(p, {"a": 1})
        with self.assertRaises(Q.Halt):
            Q.write_once(p, {"a": 2})


if __name__ == "__main__":
    unittest.main()
