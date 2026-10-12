"""python -m drift1a_c1.cli --help. Live consumption is explicitly gated."""
import argparse
import json
import os
import time
from pathlib import Path
from .common import ROOT
from .engine import Engine,genesis,locked
from .beacon import LiveBeacon,Sealer
from .reports import weekly,interpretations

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['genesis','run','replay']);p.add_argument('--root',default='drift1a_c1/recorded_live');p.add_argument('--max-ticks',type=int,default=120)
    args=p.parse_args()
    if args.action!='replay' and os.getenv('DRIFT_C1_ENABLE_LIVE')!='true':p.error('live mode disabled; DRIFT_C1_ENABLE_LIVE must explicitly equal true')
    if not 1<=args.max_ticks<=1440:p.error('max-ticks must be 1..1440')
    with locked(args.root):
        beacon=LiveBeacon();sealer=Sealer()
        if args.action=='genesis':out=genesis(args.root,'LIVE',time.time(),sealer)
        else:
            engine=Engine(args.root,beacon,sealer)
            if args.action=='replay':out=engine.replay()
            else:
                # Retry pending notes before reports/inputs. Failures are visible and do not fabricate seals.
                for name,fn in [('interpretations',lambda:interpretations(engine,ROOT/'drift1a_c1/interpretations'))]:
                    try:fn()
                    except Exception as exc:engine.incident(name+'_seal_failure',exc,engine.g['R0']+20*engine.tick)
                out=engine.ingest(time.time(),args.max_ticks)
                try:out['reports']=weekly(engine)
                except Exception as exc:engine.incident('report_seal_failure',exc,engine.g['R0']+20*engine.tick);out['report_status']='UNSEALED: '+str(exc)
        print(json.dumps(out,indent=2))
if __name__=='__main__':main()
