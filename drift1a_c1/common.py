"""Canonical encoding and durable immutable publication for C1."""
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
def cj(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
def sha(b): return hashlib.sha256(b).hexdigest()
def digest(x): return sha(cj(x))
def week(t):
    d=datetime.fromtimestamp(t,timezone.utc).isocalendar()
    return f'{d.year}-W{d.week:02d}'
def publish(path, raw):
    """Link a fully fsynced temp inode; existing committed data is never overwritten."""
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        if p.read_bytes()!=raw:raise ValueError('immutable file differs: '+str(p))
        return
    tmp=p.with_name('.'+p.name+'.pending')
    with tmp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.link(tmp,p);tmp.unlink()
    fd=os.open(p.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def read(path):return json.loads(Path(path).read_bytes())

def project_journal(directory,target):
    raw=b''.join(p.read_bytes()+b'\n' for p in sorted(Path(directory).glob('*.json')))
    p=Path(target);old=p.read_bytes() if p.exists() else b''
    if not raw.startswith(old):raise ValueError('journal prefix changed')
    if raw==old:return
    p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name('.'+p.name+'.pending')
    with tmp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
