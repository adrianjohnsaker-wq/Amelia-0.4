"""Three ISO week labels, one complete 10080-tick week, interruption and exact replay."""
import argparse
import json
import time
from datetime import datetime,timezone
from pathlib import Path
from .common import cj,publish,week
from .engine import Engine,genesis,locked,NAMES
from .beacon import SyntheticBeacon,SyntheticSealer,round_time,first_round,RetrievalError
from .reports import weekly,interpretations
from .metrics import VERSION,constant_primary_statistics

class Flaky(SyntheticBeacon):
    blocked=None
    def fetch(self,r):
        if r==self.blocked:raise RetrievalError('simulated relay outage')
        return super().fetch(r)

def simulate(root,ticks=10082):
    start=time.monotonic()
    # R0 is Sunday 23:59:xx UTC: one-minute sample spacing crosses two week boundaries.
    target=datetime(2026,10,11,23,59,tzinfo=timezone.utc).timestamp()
    created=target-600
    now=[created];seal=SyntheticSealer(lambda:now[0]);beacon=Flaky()
    with locked(root):
        g=genesis(root,'SIMULATION',created,seal);e=Engine(root,beacon,seal,lambda:now[0])
        beacon.blocked=g['R0']+20*17;now[0]=round_time(g['R0']+20*59)+10
        out=e.ingest(now[0],60)
        assert e.tick==17 and out['blocked_round']==beacon.blocked
        # A stale unpublished temp file is not a committed chunk or cursor.
        pending=Path(root)/'record/chunks/.crashed-batch.pending';pending.write_text('incomplete')
        e=Engine(root,beacon,seal,lambda:now[0]);assert e.tick==17
        beacon.blocked=None
        while e.tick<ticks:
            count=min(120,ticks-e.tick);now[0]=round_time(g['R0']+20*(e.tick+count-1))+10
            e.ingest(now[0],count)
            if e.seq%20==0:print(json.dumps(dict(progress_ticks=e.tick,elapsed_seconds=round(time.monotonic()-start,1))),flush=True)
        # Independent process-style reload before replay.
        e=Engine(root,beacon,seal,lambda:now[0]);verified=e.replay()
        reports=weekly(e)
        for item in reports:
            report=json.loads((Path(root)/'reports'/item['week']/'report.json').read_text())
            assert report['flags']['N']==29 and len(report['references'])==29
            if report['week']=='2026-W42':
                assert not constant_primary_statistics(report['arms']), constant_primary_statistics(report['arms'])
            for arm,metrics in report['arms'].items():
                classes=metrics['episode_classes']
                assert classes['traversal']['completed']+classes['boundary_entry']['completed']==classes['all']['completed']
                assert metrics['boundary_entry_diagnostic']['status']==('NOT_APPLICABLE' if arm.startswith('G') else 'PASS')
        notes=Path(root)/'operator_notes';notes.mkdir()
        (notes/'reading.txt').write_text('Retrospective SIMULATION reading; no anticipation claim.')
        interpretations(e,notes);interpretations(e,notes)
        summary=dict(measurement_version=VERSION,declared_statistics=29,canonical_boundary_diagnostics='PASS',mode='SIMULATION',not_live_evidence=True,arms=len(NAMES),ticks=e.tick,first_week=week(round_time(g['R0'])),last_week=week(round_time(g['R0']+20*(e.tick-1))),
            sealed_simulated_weeks=[r['week'] for r in reports],replay=verified,outage_resume_tick=17,
            runtime_seconds=round(time.monotonic()-start,2))
        publish(Path(root)/'simulation_summary.json',cj(summary));print(json.dumps(summary,indent=2),flush=True)
        return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--ticks',type=int,default=10082);a=p.parse_args();simulate(a.root,a.ticks)
