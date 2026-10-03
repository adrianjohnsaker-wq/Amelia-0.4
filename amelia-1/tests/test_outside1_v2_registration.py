import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
OUTSIDE = os.path.abspath(os.path.join(HERE, "..", "outside"))
if OUTSIDE not in sys.path:
    sys.path.insert(0, OUTSIDE)

import Outside1_v2 as O


class OutsideV2Registration(unittest.TestCase):
    def test_registration_only(self):
        r = O.register()
        print("OUTSIDE_V2_REGISTRATION=" + json.dumps(r, sort_keys=True))
        self.assertEqual(r["protocol_sha256"], O.PROTOCOL_SHA256)
        self.assertEqual(r["canonical_runtime_digest"], O.CANONICAL_DIGEST)


if __name__ == "__main__":
    unittest.main()
