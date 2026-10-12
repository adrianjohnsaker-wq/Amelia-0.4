"""Pinned quicknet and RFC3161 adapters; synthetic evidence can never pass live mode."""
import hashlib
import math
import time
import urllib.request
import json
from pathlib import Path
from .common import cj, digest, publish, read, sha
from .vendor.beacon_audit import QUICKNET, KAT, BLS, chain_hash_from_key, round_time, RELAYS
from .vendor.timing import obtain_token, verify_token, TRUST

class RetrievalError(RuntimeError): pass
class VerificationError(RuntimeError): pass

def first_round(created):
    minimum=math.ceil((created+600-QUICKNET['genesis_time'])/3)+1
    return max(20,20*math.ceil(minimum/20))

def current_round(at):return max(0,math.floor((at-QUICKNET['genesis_time'])/3)+1)

class LiveBeacon:
    mode='LIVE'
    def __init__(self):
        self.bls=BLS()
        if chain_hash_from_key()!=QUICKNET['chain_hash'] or not self.bls.verify(KAT['round'],KAT['signature']) or self.bls.verify(KAT['round']+1,KAT['signature']):
            raise VerificationError('BLS known-answer/key binding failed')
    def verify(self,b,r):
        try:
            good=(type(b['round']) is int and b['round']==r and len(bytes.fromhex(b['signature']))==48
                and len(bytes.fromhex(b['randomness']))==32
                and sha(bytes.fromhex(b['signature']))==b['randomness']
                and self.bls.verify(r,b['signature']))
        except (KeyError,ValueError,TypeError):good=False
        if not good:raise VerificationError('invalid quicknet round/signature/randomness')
    def fetch(self,r):
        errors=[]
        for relay in RELAYS:
            try:
                with urllib.request.urlopen(f'{relay}/{QUICKNET["chain_hash"]}/public/{r}',timeout=20) as f:
                    b=json.loads(f.read(16384))
                self.verify(b,r)
                return {k:b[k] for k in ('round','randomness','signature')}
            except VerificationError:raise
            except Exception as e:errors.append(type(e).__name__+': '+str(e))
        raise RetrievalError('; '.join(errors))

class SyntheticBeacon:
    mode='SIMULATION'
    def fetch(self,r):
        return dict(round=r,randomness=sha(f'C1-SIMULATION|{r}'.encode()),signature=None,synthetic=True)
    def verify(self,b,r):
        if b!=SyntheticBeacon.fetch(self,r):raise VerificationError('synthetic fixture mismatch')

class Sealer:
    def seal(self,folder,imprint,before=float('inf')):
        p=Path(folder);p.mkdir(parents=True,exist_ok=True)
        if (p/'receipt.json').exists():
            self.verify(p,imprint,before)
            return read(p/'receipt.json')
        # Separate attempts keep rejected/malformed replies; only a verified reply is committed.
        for old in sorted(p.glob('attempt-*.tsr')):
            result=verify_token(old,imprint,before)
            if result['status']=='PASS':return self._receipt(p,old,imprint,result)
        n=len(list(p.glob('attempt-*.tsq')))
        reply=obtain_token(p/f'attempt-{n:04d}',imprint)
        result=verify_token(reply,imprint,before)
        if result['status']!='PASS':raise VerificationError('RFC3161: '+str(result))
        return self._receipt(p,reply,imprint,result)
    def _receipt(self,p,reply,imprint,result):
        result=dict(result)
        # An unrestricted report seal has no deadline; JSON must never contain Infinity.
        if not math.isfinite(result['deadline_unix']):result['deadline_unix']=None
        result=dict(result,imprint=imprint,token=reply.name,mode='LIVE',
                    recorded_at=time.time(),round_current_at_sealing=current_round(time.time()))
        publish(p/'receipt.json',cj(result));return result
    def verify(self,folder,imprint,before=float('inf')):
        p=Path(folder);receipt=read(p/'receipt.json')
        token=receipt['token']
        if Path(token).name!=token or receipt['mode']!='LIVE' or receipt['imprint']!=imprint:raise VerificationError('seal identity')
        checked=verify_token(p/token,imprint,before)
        if checked['status']!='PASS' or checked['response_sha256']!=receipt['response_sha256']:raise VerificationError('seal verification')
        for key in ('gen_time','accuracy_seconds','accuracy_declared','comparison_time_unix','trust_anchor_sha256'):
            if checked[key]!=receipt[key]:raise VerificationError('seal receipt differs from signed token: '+key)
        return checked

class SyntheticSealer:
    def __init__(self,clock):self.clock=clock
    def seal(self,folder,imprint,before=float('inf')):
        p=Path(folder)/'receipt.json'
        if p.exists():return self.verify(folder,imprint,before)
        t=self.clock()
        if t>=before:raise VerificationError('late synthetic seal')
        x=dict(mode='SIMULATION',status='SIMULATED_NOT_RFC3161',imprint=imprint,comparison_time_unix=t,recorded_at=t,round_current_at_sealing=current_round(t))
        publish(p,cj(x));return x
    def verify(self,folder,imprint,before=float('inf')):
        x=read(Path(folder)/'receipt.json')
        if x['mode']!='SIMULATION' or x['imprint']!=imprint or x['comparison_time_unix']>=before:raise VerificationError('synthetic seal invalid')
        return x
