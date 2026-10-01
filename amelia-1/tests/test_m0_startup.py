"""M0/M1: startup integrity check for source checkout and packaged Android runtime."""
import ast
import json
import os
import shutil
import tempfile
import unittest

import amelia_core as A

HERE = os.path.dirname(os.path.abspath(__file__))
SHIPPED = ("amelia_core.py", "amelia_substrate.py", "CanonicalNumogram.py", "NumogramDynamics.py", "NumogramInterface.py")
STDLIB = {"__future__", "hashlib", "importlib", "json", "os", "platform", "sys", "itertools", "dataclasses",
          "typing", "random", "fractions", "functools", "math", "copy"}
LOCAL = {"CanonicalNumogram", "NumogramDynamics", "NumogramInterface", "amelia_substrate"}


class Startup(unittest.TestCase):
    def test_accepts_canonical_source_checkout(self):
        r = A.check()
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["integrity_mode"], "source-bytes")
        self.assertEqual(r["canonical_digest"][:8], "df164ce7")
        self.assertEqual(r["edge_counts"], {"syzygy": 10, "current": 10, "gate": 10})
        self.assertEqual(json.loads(A.startup_check())["status"], "ACCEPTED")

    def test_accepts_packaged_operational_mode(self):
        """Chaquopy omits raw .py sources: imports + operational digests must still verify."""
        d = tempfile.mkdtemp()
        try:
            shutil.copy(os.path.join(A.HERE, A.MANIFEST_FILE), d)
            r = A.check(d)
            self.assertTrue(r["ok"], r)
            self.assertEqual(r["integrity_mode"], "packaged-operational")
            self.assertTrue(all(m["match"] for m in r["modules"].values()))
            self.assertEqual(r["canonical_digest"][:8], "df164ce7")
            self.assertEqual(r["graph_digest"][:8], "9760268d")
        finally:
            shutil.rmtree(d)

    def test_refuses_altered_module(self):
        d = tempfile.mkdtemp()
        try:
            for f in SHIPPED + (A.MANIFEST_FILE,):
                shutil.copy(os.path.join(A.HERE, f), d)
            with open(os.path.join(d, "NumogramDynamics.py"), "a") as fh:
                fh.write("\n# altered\n")
            r = A.check(d)
            self.assertFalse(r["ok"])
            self.assertEqual(r["status"], "REFUSED")
            self.assertFalse(r["modules"]["NumogramDynamics.py"]["match"])
        finally:
            shutil.rmtree(d)

    def test_refuses_partial_source_set(self):
        d = tempfile.mkdtemp()
        try:
            shutil.copy(os.path.join(A.HERE, A.MANIFEST_FILE), d)
            shutil.copy(os.path.join(A.HERE, "CanonicalNumogram.py"), d)
            r = A.check(d)
            self.assertFalse(r["ok"], r)
            self.assertEqual(r["integrity_mode"], "invalid")
            self.assertEqual(r["reason"], "canonical module source set incomplete")
        finally:
            shutil.rmtree(d)

    def test_standard_library_only(self):
        for f in SHIPPED:
            with open(os.path.join(A.HERE, f), encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name.split(".")[0] for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module.split(".")[0]]
                for n in names:
                    self.assertIn(n, STDLIB | LOCAL, "%s imports %s" % (f, n))


if __name__ == "__main__":
    unittest.main()
