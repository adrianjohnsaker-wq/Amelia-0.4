# assets/python/numogram_engine_compact_core.py
import json, math, random, time
from typing import Dict, Any, Optional, List

class NumogramEngine:
    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self.zone = 7
        self.resonance = [0.0] * 10
        self.tick_ms = int(time.time() * 1000)
        self.S = self._build_syzygy_matrix()
        self.entropy = 0.3
        self.temporal = 0.5

    def _build_syzygy_matrix(self) -> List[List[float]]:
        S = [[0.0]*10 for _ in range(10)]
        links = [(0,9),(9,0),(1,6),(6,1),(2,8),(8,2),(3,7),(7,3),(4,5),(5,4)]
        for i,j in links:
            S[i][j]=S[j][i]=1.0
        for i in range(10):
            S[i][i]=0.2
            S[i][(i+1)%10]+=0.3
            S[i][(i-1)%10]+=0.3
        return S

    def influence_from_text(self, text: str):
        t = text.lower()
        keys = {
            0:["void","silence","abyss"],1:["birth","spark","ignite"],
            2:["split","dual","cut"],3:["surge","erupt","fire"],
            4:["orbit","cycle","return"],5:["threshold","gate","limen"],
            6:["recursion","maze","labyrinth"],7:["mirror","reflect","meta"],
            8:["synthesis","weave","assemblage"],9:["excess","burn","overflow"]
        }
        for z,ws in keys.items():
            if any(w in t for w in ws):
                self.resonance[z]=min(1.0,self.resonance[z]+0.2)

    def _softmax(self, xs):
        m=max(xs); ex=[math.exp(x-m) for x in xs]; s=sum(ex) or 1.0
        return [e/s for e in ex]

    def _transition_probs(self,i:int)->List[float]:
        α,β,γ,δ=1.7,1.2,0.8,0.6
        vals=[]
        for j in range(10):
            vals.append(α*self.S[i][j]+β*self.resonance[j]+γ*self.entropy+
                        δ*self.temporal*(1.0 if j%2==i%2 else 0.0))
        return self._softmax(vals)

    def tick(self, dt_ms:int=60000, text:Optional[str]=None)->Dict[str,Any]:
        self.tick_ms+=dt_ms
        if text: self.influence_from_text(text)
        probs=self._transition_probs(self.zone)
        r=self.rng.random();acc=0.0;nxt=self.zone
        for j,p in enumerate(probs):
            acc+=p
            if r<=acc: nxt=j;break
        self.zone=nxt
        self.resonance=[max(0.0,v-0.05) for v in self.resonance]
        return self.snapshot()

    def profile(self)->Dict[str,Any]:
        fold=[0.2,0.35,0.4,0.55,0.5,0.65,0.6,0.75,0.8,0.7]
        temp=[0.9,0.8,0.85,0.95,0.7,1.0,0.75,0.8,0.9,1.05]
        return {
            "zone":self.zone,"fold":fold[self.zone],"temperature":temp[self.zone],
            "module_affinity":{
                "desire":0.4+0.05*self.zone,
                "decision":0.6 if self.zone in (4,8) else 0.45,
                "becoming":0.7 if self.zone in (5,7,9) else 0.5}
        }

    def snapshot(self)->Dict[str,Any]:
        return {"timestamp":self.tick_ms,"zone":self.zone,
                "resonance":self.resonance,"profile":self.profile()}

_engine: Optional[NumogramEngine] = None

def init(seed:Optional[int]=None)->str:
    global _engine
    _engine=NumogramEngine(seed)
    return json.dumps({"status":"initialized","zone":_engine.zone})

def tick(dt_ms:int=60000,text:Optional[str]=None)->str:
    return json.dumps(_engine.tick(dt_ms,text))

def get_profile()->str:
    return json.dumps(_engine.profile())
