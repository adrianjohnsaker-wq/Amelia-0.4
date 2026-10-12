import copy
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from drift1a_c1.common import read,cj,sha,digest,week
from drift1a_c1.beacon import SyntheticBeacon,SyntheticSealer,LiveBeacon,Sealer,first_round,round_time,VerificationError,KAT
from drift1a_c1.engine import Engine,genesis,graphs,input_for,NAMES
from drift1a_c1.metrics import mutual_information,ranks,js_divergence
from drift1a_c1.reports import weekly,interpretations,week_record_digest
from drift_core import digest as core_digest,empty_history,degree_signature

class C1(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.now=[1791762550.] # arbitrary fixture; no live input
        self.sealer=SyntheticSealer(lambda:self.now[0]);self.beacon=SyntheticBeacon()
        self.g=genesis(self.root,'SIMULATION',self.now[0],self.sealer)
        self.e=Engine(self.root,self.beacon,self.sealer,lambda:self.now[0])
    def tearDown(self):self.tmp.cleanup()
    def run_ticks(self,n):
        self.now[0]=round_time(self.g['R0']+20*(self.e.tick+n-1))+10
        return self.e.ingest(self.now[0],n)
    def test_genesis_cadence_and_distinct_degree_matched_graphs(self):
        r=self.g['R0'];self.assertEqual(r%20,0);self.assertGreaterEqual(round_time(r),self.g['created_at']+600)
        self.assertLess(round_time(r-20),self.g['created_at']+600)
        gs=graphs();self.assertEqual(len({digest(gs[a]) for a in NAMES if a.startswith('G')}),8)
        self.assertTrue(all(degree_signature(g)==degree_signature(gs['C']) for g in gs.values()))
    def test_mode_isolation_and_frozen_files(self):
        with self.assertRaises(ValueError):genesis(self.root/'bad','LIVE',self.now[0],self.sealer)
        with patch('drift1a_c1.engine.frozen_files',return_value={}):
            with self.assertRaises(ValueError):Engine(self.root,self.beacon,self.sealer)
    def test_pairing_reset_reentry_and_replay(self):
        self.run_ticks(48)
        for r in self.e.records():
            arms=r['arms'];shared=[arms[a]['embodiment']['ingress_u'] for a in NAMES if not a.startswith('R')]
            self.assertEqual(len(set(shared)),1)
            self.assertEqual(arms['M']['memory_read_digest'],core_digest(empty_history()))
            self.assertTrue(all(e['edge'] in self.g['graphs'][a] for a,e in arms.items()))
        self.assertEqual(self.e.replay()['ticks'],48)
        self.assertNotEqual(input_for('R01','00'*32),input_for('R02','00'*32))
    def test_restart_ignores_temp_and_does_not_duplicate_ticks(self):
        self.run_ticks(5);head=self.e.head
        (self.root/'record/chunks/.abandoned.pending').write_bytes(b'partial')
        self.e=Engine(self.root,self.beacon,self.sealer,lambda:self.now[0]);self.assertEqual(self.e.tick,5);self.assertEqual(self.e.head,head)
        self.run_ticks(4);self.assertEqual([r['tick'] for r in self.e.records()],list(range(9)))
        self.assertEqual(self.e.replay()['ticks'],9)
    def test_fetch_failure_commits_prefix_and_retries_same_round(self):
        original=self.beacon.fetch;blocked=self.g['R0']+40
        def fetch(r):
            if r==blocked:raise RuntimeError('offline')
            return original(r)
        with patch.object(self.beacon,'fetch',side_effect=fetch):self.run_ticks(5)
        self.assertEqual(self.e.tick,2)
        self.e=Engine(self.root,self.beacon,self.sealer,lambda:self.now[0]);self.run_ticks(3)
        self.assertEqual(self.e.tick,5)
        self.assertIn('retrieval_failure',(self.root/'record/incidents.jsonl').read_text())
    def test_invalid_beacon_halts_without_cursor_advance(self):
        with patch.object(self.beacon,'fetch',return_value={'round':self.g['R0'],'randomness':'00'*32}):self.run_ticks(1)
        self.assertEqual(self.e.tick,0)
        self.assertIn('verification_failure',(self.root/'record/incidents.jsonl').read_text())
    def test_lag_and_not_yet_published(self):
        self.assertEqual(self.e.ingest(round_time(self.g['R0'])-1,1)['ticks'],0)
        self.now[0]=round_time(self.g['R0'])+5401;self.e.ingest(self.now[0],1)
        self.assertTrue(next(self.e.records())['catch_up'])
    def test_tamper_and_gap_rejected(self):
        self.run_ticks(3);self.run_ticks(2)
        p=next((self.root/'record/chunks').glob('00000000*'));p.unlink()
        with self.assertRaises(ValueError):Engine(self.root,self.beacon,self.sealer)
    def test_interpretation_retry_preserves_first_observed_and_deduplicates(self):
        notes=self.root/'input';notes.mkdir();f=notes/'note.txt';f.write_text('retrospective fixture')
        with patch.object(self.sealer,'seal',side_effect=RuntimeError('TSA offline')):
            with self.assertRaises(RuntimeError):interpretations(self.e,notes)
        f.unlink();self.now[0]+=60;interpretations(self.e,notes);interpretations(self.e,notes)
        rows=(self.root/'record/interpretations_index.jsonl').read_text().splitlines()
        self.assertEqual(len(rows),1);r=json.loads(rows[0]);self.assertLess(r['first_observed_at'],r['verified_sealing_time'])
    def test_interpretation_recovers_after_publication_interruption(self):
        from drift1a_c1.common import publish
        notes=self.root/'input';notes.mkdir();f=notes/'note.txt';f.write_text('preserve this note')
        def interrupted(path,raw):
            if Path(path).name=='note':raise OSError('simulated interruption')
            return publish(path,raw)
        with patch('drift1a_c1.reports.publish',side_effect=interrupted):
            with self.assertRaises(OSError):interpretations(self.e,notes)
        f.unlink();interpretations(self.e,notes)
        self.assertEqual(len((self.root/'record/interpretations_index.jsonl').read_text().splitlines()),1)
    def test_hosted_lease_blocks_until_evidence_completion(self):
        from drift1a_c1.runner import claim,complete
        root=self.root/'runner';claim(root,'101-1')
        with self.assertRaises(ValueError):claim(root,'102-1')
        complete(root,'101-1');claim(root,'102-1')
    def test_mutual_information_ties_and_empty_routes(self):
        self.assertEqual(mutual_information([(1,'Warp'),(2,'Plex')])['bits'],1.)
        self.assertIsNone(mutual_information([])['bits'])
        self.assertIsNone(js_divergence({},{}));self.assertEqual(js_divergence({'a':1},{'a':2}),0.)
        r=ranks({a:{'x':2} for a in NAMES})['/x'];self.assertEqual((r['rank_low'],r['rank_high']),(1,9));self.assertFalse(r['strict_outside'])
    def test_streaming_record_digest_equals_canonical_list(self):
        rows=[dict(round_time=1791762550.,tick=i) for i in range(3)]
        hashed,last=week_record_digest(iter(rows),week(rows[0]['round_time']))
        self.assertEqual(hashed,digest(rows));self.assertEqual(last,rows[-1])

class Crypto(unittest.TestCase):
    def test_real_known_answer_wrong_round_and_forgery(self):
        b=LiveBeacon();b.verify(KAT,KAT['round'])
        with self.assertRaises(VerificationError):b.verify(KAT,KAT['round']+1)
        f=dict(KAT,signature='00'*48,randomness=sha(bytes(48)))
        with self.assertRaises(VerificationError):b.verify(f,KAT['round'])

class Weekly(unittest.TestCase):
    def test_failed_seal_retry_and_week_assignment_preserve_bytes(self):
        from datetime import datetime,timezone
        with tempfile.TemporaryDirectory() as root:
            t=datetime(2026,10,11,23,59,tzinfo=timezone.utc).timestamp()-600
            now=[t];s=SyntheticSealer(lambda:now[0]);g=genesis(root,'SIMULATION',t,s)
            e=Engine(root,SyntheticBeacon(),s,lambda:now[0])
            now[0]=round_time(g['R0'])+70;e.ingest(now[0],1)
            with patch.object(s,'seal',side_effect=RuntimeError('simulated TSA outage')):
                with self.assertRaises(RuntimeError):weekly(e)
            folder=next((Path(root)/'reports').iterdir());before=(folder/'report.json').read_bytes();markdown=(folder/'report.md').read_bytes()
            now[0]+=60
            with patch('drift1a_c1.reports.render',side_effect=RuntimeError('must not regenerate')):weekly(e)
            self.assertEqual(before,(folder/'report.json').read_bytes());self.assertEqual(markdown,(folder/'report.md').read_bytes())
            self.assertTrue((folder/'seal/receipt.json').exists())
            with patch('drift1a_c1.reports.summarize',side_effect=RuntimeError('must reuse sealed report')):
                weekly(e) # repeat invocation is idempotent and does not reprocess history
            r=read(folder/'report.json');self.assertTrue(all(m['ticks']==1 for m in r['arms'].values()))
    def test_late_genesis_fails_and_remains_unactivated(self):
        with tempfile.TemporaryDirectory() as root:
            t=1791762550.;s=SyntheticSealer(lambda:round_time(first_round(t)))
            with self.assertRaises(VerificationError):genesis(root,'SIMULATION',t,s)
            self.assertFalse((Path(root)/'genesis.json').exists())
