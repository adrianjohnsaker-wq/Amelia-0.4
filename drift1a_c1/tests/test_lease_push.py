"""Local Git failure-injection tests; no network or beacon admission."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from drift1a_c1.lease_push import acquire

def run(cwd, *args, check=True):
    p=subprocess.run(["git",*args],cwd=cwd,text=True,capture_output=True)
    if check and p.returncode: raise AssertionError(p.stderr)
    return p

class LeasePushTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        self.remote=root/"remote.git";self.seed=root/"seed";self.work=root/"work";self.rival=root/"rival"
        run(root,"init","--bare",str(self.remote))
        run(root,"init",str(self.seed))
        for k,v in [("user.name","C1 Test"),("user.email","test@example.invalid")]:
            run(self.seed,"config",k,v)
        (self.seed/"drift1a_c1/runner_state").mkdir(parents=True)
        (self.seed/"README").write_text("base")
        run(self.seed,"add",".");run(self.seed,"commit","-m","base")
        run(self.seed,"branch","-M","amelia-1.0")
        run(self.seed,"remote","add","origin",str(self.remote))
        run(self.seed,"push","-u","origin","amelia-1.0")
        for dst in (self.work,self.rival):
            run(root,"clone","--branch","amelia-1.0",str(self.remote),str(dst))
            run(dst,"config","user.name","C1 Test")
            run(dst,"config","user.email","test@example.invalid")
        self.prev=Path.cwd();os.chdir(self.work);self.addCleanup(os.chdir,self.prev)

    def test_competing_commit_rebases_and_retries(self):
        # A pre-push hook injects a rival remote commit on the first push.
        hook=self.work/".git/hooks/pre-push"
        hook.write_text("#!/bin/sh\nif [ ! -f .git/c1-hook-fired ]; then\n"
                        " touch .git/c1-hook-fired\n"
                        " git -C ../rival -c user.name=Rival -c user.email=rival@example.invalid "
                        "commit --allow-empty -m rival >/dev/null || exit 1\n"
                        " git -C ../rival push origin HEAD:amelia-1.0 >/dev/null || exit 1\nfi\n")
        hook.chmod(0o755)
        result=acquire("123-1")
        self.assertEqual(result["attempts"],2)
        self.assertTrue(result["admission_authorized"])
        run(self.work,"fetch","origin","amelia-1.0")
        self.assertEqual(run(self.work,"show","FETCH_HEAD:drift1a_c1/runner_state/leases/123-1.json").returncode,0)

    def test_unreachable_push_three_attempts_no_admission(self):
        # Fetch remains available, but the push URL is unreachable.
        run(self.work,"remote","set-url","--push","origin",str(self.work/"nonexistent.git"))
        with self.assertRaisesRegex(RuntimeError,"three attempts: no admission"):
            acquire("124-1")
        self.assertNotEqual(run(self.work,"rev-parse","--verify","origin/amelia-1.0").returncode,1)
        self.assertFalse((self.remote/"drift1a_c1/runner_state/leases/124-1.json").exists())
        self.assertNotIn("124-1",run(self.work,"ls-tree","-r","--name-only","origin/amelia-1.0").stdout)

if __name__=="__main__":
    unittest.main()
