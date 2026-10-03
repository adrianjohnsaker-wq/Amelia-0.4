import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
OUTSIDE = os.path.abspath(os.path.join(HERE, "..", "outside"))
if OUTSIDE not in sys.path:
    sys.path.insert(0, OUTSIDE)

import Outside1_v2 as O


class OutsideV2RegisteredDiagnostics(unittest.TestCase):
    def test_registration_is_sealed(self):
        r = O.check_registered()
        self.assertEqual(r["protocol_sha256"], "056ab407d4833232af540aff965c179762103f967370d2e7bae16bb25378cceb")
        self.assertEqual(r["canonical_runtime_digest"], O.CANONICAL_DIGEST)

    def test_D1_trace_sensitivity(self):
        r = O.diagnose_D1()
        print("OUTSIDE_V2_D1=" + json.dumps(r, sort_keys=True))
        self.assertTrue(r["pass"], r)


if __name__ == "__main__":
    unittest.main()
