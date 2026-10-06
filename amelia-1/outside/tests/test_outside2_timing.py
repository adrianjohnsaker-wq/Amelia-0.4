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
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import outside2_timing as T
import audit_beacon_outside2 as A

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
    def test_audit_marks_unresolved_reading_missing_token(self):
        reg=json.loads((T.HERE/'outside2_registration.json').read_text())
        stamp='2026-10-06T14:00:00.000Z'
        event={'event_type':'READING','working':'W013','created_utc':stamp,'event_hash':self.digest,
               'payload':{'beacon_round':A.registered_round(A.unix(stamp))}}
        self.assertEqual(T.audit_readings([event],reg,self.d)['W013']['status'],'INCOMPLETE')
        event['payload']['beacon_round']+=1
        self.assertEqual(T.audit_readings([event],reg,self.d)['W013']['status'],'FAIL')

if __name__=='__main__': unittest.main()
