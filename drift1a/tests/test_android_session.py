import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
import android_session as A

class AndroidSession(unittest.TestCase):
    def test_reference(self):
        self.assertTrue(A.check_reference().startswith('PASS'))

    def test_persistent_three_arm_resume_replay_export(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertFalse(json.loads(A.status(root))['exists'])
            s=json.loads(A.create(root,101,1))
            self.assertEqual(s['ticks'],0)
            s=json.loads(A.advance(root,32))
            self.assertEqual(s['ticks'],32)
            self.assertEqual(json.loads(A.status(root)),s)
            self.assertTrue(A.verify_run(root).startswith('PASS'))
            s=json.loads(A.advance(root,512))
            self.assertEqual(s['ticks'],512)
            self.assertEqual(json.loads(A.advance(root,1)),s)
            self.assertTrue(A.verify_run(root).startswith('PASS'))
            A.export_zip(root,str(Path(root)/'evidence.zip'))
            import zipfile
            with zipfile.ZipFile(Path(root)/'evidence.zip') as z:
                self.assertEqual(len(z.namelist()),513)
            old=s['session']
            new=json.loads(A.create(root,202,9))
            self.assertNotEqual(old,new['session'])
            self.assertTrue((Path(root)/old/'tick_000511.json').exists())

    def test_reject_tampered_ledger(self):
        with tempfile.TemporaryDirectory() as root:
            state=json.loads(A.create(root,101,1))
            A.advance(root,1)
            path=Path(root)/state['session']/'tick_000000.json'
            d=json.loads(path.read_text());d['input']='00'*32
            path.write_text(json.dumps(d))
            with self.assertRaises(ValueError):A.status(root)
