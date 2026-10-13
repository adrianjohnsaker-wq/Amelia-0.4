"""Reanalyse the fixed, previously replayed validation ledger; never admit live input."""
import argparse
import gzip
import json
import time
import zipfile
from pathlib import Path
from .common import cj,digest,sha,publish,week
from .metrics import summarize,ranks,flag_summary,retrospective,leave_one_out_flags,constant_primary_statistics,VERSION
from .reports import render,week_record_digest
from .engine import frozen_files
from .beacon import SyntheticSealer

SOURCE_SHA256='4ed2bb9bd5bc1e713f36b4c7bce68513108ecdfacd54e35e42c9d1bf8bf9493a'

def remeasure(archive,root):
    archive=Path(archive);root=Path(root)
    assert sha(archive.read_bytes())==SOURCE_SHA256,'unexpected validation artifact'
    with zipfile.ZipFile(archive) as z:
        source=json.loads(z.read('c1-simulation/genesis.json'))
        assert source['mode']=='SIMULATION'
        baseline=json.loads(z.read('c1-simulation/simulation_summary.json'))
        assert baseline['replay']['exact_replay'] and baseline['ticks']==10082
        current=frozen_files()
        changed=[p for p,h in source['files'].items() if current.get(p)!=h]
        assert set(changed)=={'drift1a_c1/metrics.py','claude/DRIFT1A_C1_CHARTER_draft.md'},changed
        def records():
            for name in sorted(z.namelist()):
                if name.startswith('c1-simulation/record/chunks/') and name.endswith('.json.gz'):
                    yield from json.loads(gzip.decompress(z.read(name)))['records']
        summaries=summarize(records());earlier={};results={}
        for w in baseline['sealed_simulated_weeks']:
            old=json.loads(z.read(f'c1-simulation/reports/{w}/report.json'))
            arms=summaries[w];refs=ranks(arms)
            record_digest,last=week_record_digest(records(),w)
            assert record_digest==old['records_digest']
            if w=='2026-W42':
                constants=constant_primary_statistics(arms)
                assert not constants, f'constant declared statistics: {constants}'
            for a,m in arms.items():
                assert m==old['arms'][a],f'unexpected change to raw arm measurements: {a}'
            report=dict(old,version='C1-report-0.3-A11',measurement_version=VERSION,
                renderer_sha256=sha(Path(__file__).with_name('reports.py').read_bytes()),
                arms=arms,references=refs,flags=flag_summary(refs,earlier),
                leave_one_out_flags=leave_one_out_flags(arms),retrospective=retrospective(arms,earlier,w),
                reanalysis=dict(source_artifact_sha256=SOURCE_SHA256,measurement_files=current,
                    source_report_sha256=sha(z.read(f'c1-simulation/reports/{w}/report.json')),
                    note='New measurement of the validated synthetic ledger; source genesis froze the earlier measurement version. No new dynamics or live genesis.'),
                limitations=old['limitations']+['A11 reanalysis of the previously replayed synthetic ledger; no new dynamics run or live timestamp is claimed.'])
            folder=root/w
            raw=cj(report);md=render(report).encode()
            publish(folder/'report.json',raw);publish(folder/'report.md',md)
            bundle=dict(json_sha256=sha(raw),markdown_sha256=sha(md));publish(folder/'bundle.json',cj(bundle))
            seal=SyntheticSealer(lambda:old['generated_at']);seal.seal(folder/'seal',digest(bundle));seal.verify(folder/'seal',digest(bundle))
            earlier[w]=dict(report=report,seal_digest=sha((folder/'seal/receipt.json').read_bytes()))
            results[w]=dict(N=report['flags']['N'],F=report['flags']['F'],leave_one_out=report['leave_one_out_flags'],records_digest=record_digest,bundle=bundle)
        result=dict(status='PASS',measurement_version=VERSION,source_artifact_sha256=SOURCE_SHA256,
            source_exact_replay=True,source_ticks_per_arm=10082,source_arms=18,
            reanalysis_only=True,all_raw_arm_measurements_unchanged=True,
            validation_week_constant_statistics=[],measurement_files=current,reports=results)
        publish(root/'validation.json',cj(result))
        print(json.dumps({k:v for k,v in result.items() if k!='measurement_files'},indent=2))
        return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--root',required=True)
    a=p.parse_args();remeasure(a.archive,a.root)
