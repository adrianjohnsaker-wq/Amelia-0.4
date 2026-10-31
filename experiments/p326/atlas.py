"""Create-only gzip JSONL SHA-256 chain archive for P3.26 encounters."""
from __future__ import annotations
import gzip,hashlib,json
from pathlib import Path
from typing import Dict
GENESIS="0"*64

def canonical_json(value:object)->str:
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False)

def _open_read(path:Path):
    return gzip.open(path,"rt",encoding="utf-8") if path.suffix==".gz" else path.open("r",encoding="utf-8")

def verify(path:str)->str:
    previous=GENESIS; fp=Path(path)
    if not fp.exists(): return previous
    with _open_read(fp) as handle:
        for no,line in enumerate(handle,1):
            record=json.loads(line); stated_previous=record.pop("previous_digest",None); stated_digest=record.pop("record_digest",None)
            if stated_previous!=previous: raise ValueError("P3.26 atlas chain break at line {}".format(no))
            computed=hashlib.sha256((previous+canonical_json(record)).encode("utf-8")).hexdigest()
            if stated_digest!=computed: raise ValueError("P3.26 atlas digest mismatch at line {}".format(no))
            previous=computed
    return previous

class CreateOnlyAtlas:
    def __init__(self,path:str)->None:
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self.previous_digest=verify(path)
        if self.path.suffix==".gz": self.handle=gzip.open(self.path,"xt",encoding="utf-8",compresslevel=6)
        else: self.handle=self.path.open("x",encoding="utf-8")
        self._count=0
    def append(self,record:Dict[str,object])->str:
        body=dict(record)
        if "record_digest" in body or "previous_digest" in body: raise ValueError("record may not supply chain fields")
        digest=hashlib.sha256((self.previous_digest+canonical_json(body)).encode("utf-8")).hexdigest()
        linked=dict(body); linked["previous_digest"]=self.previous_digest; linked["record_digest"]=digest
        self.handle.write(canonical_json(linked)+"\n"); self._count+=1
        if self._count%64==0: self.handle.flush()
        self.previous_digest=digest
        return digest
    def close(self)->None:
        self.handle.flush(); self.handle.close()
    def __enter__(self)->"CreateOnlyAtlas": return self
    def __exit__(self,exc_type:object,exc:object,tb:object)->None: self.close()
