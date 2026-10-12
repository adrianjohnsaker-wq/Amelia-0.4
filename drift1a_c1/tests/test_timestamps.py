"""Synthetic local TSA only. Never reads or writes the real experiment ledger."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from drift1a_c1.vendor import timing as T

class TimestampTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.d=Path(cls.tmp.name)
        cls.digest=hashlib.sha256(b'synthetic reading only').hexdigest()
        cls.ca=cls.d/'tsa.pem'
        cls.key=cls.d/'tsa.key'
        T.command(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1',
                   '-subj','/CN=Synthetic Test TSA','-keyout',str(cls.key),'-out',str(cls.ca),
                   '-addext','basicConstraints=critical,CA:FALSE',
                   '-addext','keyUsage=critical,digitalSignature',
                   '-addext','extendedKeyUsage=critical,timeStamping'])
        q=cls.d/'test.tsq'
        q.write_bytes(T.command(['openssl','ts','-query','-sha256','-digest',cls.digest,'-cert']))
        (cls.d/'serial').write_text('01\n')
        config=cls.d/'tsa.cnf'
        config.write_text('[tsa]\ndefault_tsa = test\n[test]\nserial = '+str(cls.d/'serial')+
                          '\ncrypto_device = builtin\nsigner_cert = '+str(cls.ca)+
                          '\ncerts = '+str(cls.ca)+'\nsigner_key = '+str(cls.key)+
                          '\nsigner_digest = sha256\ndefault_policy = 1.2.3.4\ndigests = sha256\naccuracy = secs:1\nordering = yes\ntsa_name = yes\ness_cert_id_chain = no\n')
        cls.response=cls.d/'test.tsr'
        T.command(['openssl','ts','-reply','-config',str(config),'-queryfile',str(q),'-out',str(cls.response)])
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()
    def verify(self,digest=None,deadline=None,path=None,ca=None):
        return T.verify_token(path or self.response,digest or self.digest,
                              deadline if deadline is not None else time.time()+600,ca or self.ca)
    def test_genuine_offline(self): self.assertEqual(self.verify()['status'],'PASS')
    def test_wrong_reading(self): self.assertEqual(self.verify(digest='00'*32)['status'],'FAIL')
    def test_late(self): self.assertEqual(self.verify(deadline=0)['status'],'FAIL')
    def test_missing(self): self.assertEqual(self.verify(path=self.d/'missing')['status'],'INCOMPLETE')
    def test_wrong_trust(self): self.assertEqual(self.verify(ca=T.TRUST)['status'],'FAIL')
    def test_altered_signature(self):
        from asn1crypto import tsp
        data=tsp.TimeStampResp.load(self.response.read_bytes())
        signer=data['time_stamp_token']['content']['signer_infos'][0]
        sig=bytearray(signer['signature'].native);sig[0]^=1
        signer['signature']=bytes(sig)
        path=self.d/'altered.tsr';path.write_bytes(data.dump())
        self.assertEqual(self.verify(path=path)['status'],'FAIL')
    def test_accuracy_boundary(self):
        upper=self.verify()['comparison_time_unix']
        self.assertEqual(self.verify(deadline=upper)['status'],'FAIL')
        self.assertEqual(self.verify(deadline=upper+0.001)['status'],'PASS')
    def test_missing_openssl(self):
        with patch.object(T,'command',side_effect=FileNotFoundError('openssl')):
            self.assertEqual(self.verify()['status'],'INCOMPLETE')
    def test_report_seal_serializes_without_deadline_and_rejects_receipt_tamper(self):
        from drift1a_c1.beacon import Sealer,VerificationError
        with tempfile.TemporaryDirectory() as root:
            folder=Path(root);(folder/'attempt-0000.tsr').write_bytes(self.response.read_bytes())
            verifier=lambda path,digest,before:T.verify_token(path,digest,before,self.ca)
            with patch('drift1a_c1.beacon.verify_token',side_effect=verifier):
                seal=Sealer();receipt=seal.seal(folder,self.digest)
                self.assertIsNone(receipt['deadline_unix'])
                self.assertEqual(seal.seal(folder,self.digest),receipt)
                seal.verify(folder,self.digest)
                receipt['comparison_time_unix']-=100
                (folder/'receipt.json').write_text(json.dumps(receipt))
                with self.assertRaises(VerificationError):seal.verify(folder,self.digest)
