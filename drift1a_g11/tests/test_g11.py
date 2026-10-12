import copy
import math
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from episodic import EpisodicSubstrate, BOUNDARY, EPISODE_CAP, variates, episode_metrics
from drift_core import canonical_edges, rewire, digest, empty_history, Substrate
from run_drift import synthetic_tape

class G11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arms={a:EpisodicSubstrate(rewire(canonical_edges()) if a=='G' else canonical_edges()) for a in 'CGM'}
        cls.records=[]
        for i,x in enumerate(synthetic_tape(101,512)):
            v=variates(x,i)
            cls.records.append({a:(s.advance(v['transition'],v['ingress'],reset=a=='M'),s.snapshot()) for a,s in cls.arms.items()})

    def test_shared_entry_proposals_every_tick_even_when_episode_schedules_diverge(self):
        different_entry_times=0
        for r in self.records:
            bs=[r[a][0]['embodiment'] for a in 'CGM']
            self.assertEqual(len({b['ingress_u'] for b in bs}),1)
            self.assertEqual(len({b['proposed_entry'] for b in bs}),1)
            self.assertEqual(len({r[a][0]['u'] for a in 'CGM'}),1)
            for b in bs:
                if b['entry'] is not None:self.assertEqual(b['entry']['zone'],b['proposed_entry'])
            different_entry_times += (bs[0]['entry'] is None) != (bs[2]['entry'] is None)
        self.assertGreater(different_entry_times,0)

    def test_one_legal_move_per_tick_and_no_ingress_updates(self):
        prev={a:EpisodicSubstrate(s.edges).snapshot() for a,s in self.arms.items()}
        for i,r in enumerate(self.records):
            for a,(e,snap) in r.items():
                b=e['embodiment'];old=prev[a];core=snap['core']
                self.assertEqual(e['pre_embodiment_digest'],old['digest'])
                self.assertEqual(e['post_embodiment_digest'],snap['digest'])
                self.assertEqual(core['P']['tick'],i+1)
                self.assertIn(e['selected_edge'],self.arms[a].edges)
                self.assertEqual(b['entry'] is not None,old['episode']['pending_entry'])
                self.assertEqual(e['selected_edge'][0],b['proposed_entry'] if b['entry'] else old['core']['P']['zone'])
                h=empty_history() if a=='M' else old['core']['H']
                self.assertEqual(e['memory_read_digest'],digest(h))
                self.assertEqual(core['H']['updates'],1 if a=='M' else i+1)
                before=copy.deepcopy(old['core']);before.pop('digest')
                before['H']=h;before['P']['zone']=e['selected_edge'][0]
                self.assertEqual(e['pre_state_digest'],digest(before))
                self.assertEqual(e['post_state_digest'],core['digest'])
                self.assertEqual(b['end']=='boundary',e['selected_edge'][1] in BOUNDARY)
                self.assertEqual(b['length'],1 if b['entry'] else old['episode']['length']+1)
                prev[a]=snap

    def test_entry_into_boundary_still_makes_one_move_and_reenters_next_tick(self):
        s=EpisodicSubstrate()
        e=s.advance(.1,.35) # enter3 then move3->6
        self.assertEqual(e['selected_edge'][:2],[3,6])
        self.assertEqual(e['embodiment']['length'],1)
        self.assertEqual(e['embodiment']['outcome'],'Warp')
        e=s.advance(.1,.05) # enter0 then move0->9
        self.assertEqual(e['selected_edge'][:2],[0,9])
        self.assertEqual(e['embodiment']['outcome'],'Plex')
        self.assertEqual(s.core.H['updates'],2)

    def test_wrapper_preserves_selector_behavior_after_entry(self):
        s=EpisodicSubstrate();plain=Substrate(start=1)
        e=s.advance(.95,.15)
        expected=plain.advance(.95)
        self.assertEqual({k:e[k] for k in expected},expected)
        self.assertEqual(s.core.snapshot(),plain.snapshot())

    def test_global_operation_keying_is_distinct_and_stateless(self):
        x=synthetic_tape(101,2)
        v=variates(x[0],0)
        self.assertNotEqual(v['ingress'],v['transition'])
        self.assertNotEqual(v,variates(x[0],1))
        self.assertEqual(v,variates(x[0],0))

    def test_cap_and_boundary_precedence(self):
        s=EpisodicSubstrate();s.core.P['zone']=1
        s.episode=dict(index=0,length=EPISODE_CAP-1,pending_entry=False)
        e=s.advance(.99,.0)
        self.assertEqual(e['embodiment']['end'],'cap');self.assertIsNone(e['embodiment']['outcome'])
        s=EpisodicSubstrate();s.core.P['zone']=3
        s.episode=dict(index=0,length=EPISODE_CAP-1,pending_entry=False)
        self.assertEqual(s.advance(.1,.0)['embodiment']['end'],'boundary')

    def test_checkpoint_resume_and_invalid_variate_transaction(self):
        for a in 'CGM':
            e,snap=self.records[255][a]
            s=EpisodicSubstrate.restore(snap)
            next_event=self.records[256][a][0]
            self.assertEqual(s.advance(next_event['u'],next_event['embodiment']['ingress_u'],reset=a=='M'),next_event)
        s=EpisodicSubstrate();before=s.snapshot()
        for u,v in [(math.nan,.5),(.5,1),(-.1,.2)]:
            with self.assertRaises(ValueError):s.advance(u,v)
            self.assertEqual(s.snapshot(),before)

    def test_metrics_denominators_routes_censoring_and_actual_effects(self):
        for a in 'CGM':
            es=[r[a][0] for r in self.records];m=episode_metrics(es)
            self.assertEqual(m['warp']+m['plex'],m['boundary_episodes'])
            self.assertEqual(sum(x['choices'] for x in m['effects_by_source'].values()),512)
            total=sum(x['length'] for x in m['completed'])+(m['right_censored']['length'] if m['right_censored'] else 0)
            self.assertEqual(total,512)
            self.assertTrue(all(len(x['route'])==x['length']+1 for x in m['completed']))
            if a=='M':
                self.assertEqual(sum(x['commitment_changed']+x['retention_changed'] for x in m['effects_by_source'].values()),0)
        s=EpisodicSubstrate();e=s.advance(.99,.15)
        self.assertEqual(episode_metrics([e])['right_censored']['length'],1)
        self.assertEqual(episode_metrics([e])['boundary_episodes'],0)

    def test_memory_changes_same_present_choice_distribution(self):
        found=False
        for r in self.records:
            for a in 'CG':
                s=EpisodicSubstrate.restore(r[a][1]);blank=Substrate.restore(s.core.snapshot())
                blank.reset_memory()
                if s.core.distribution()['probabilities']!=blank.distribution()['probabilities']:
                    found=True;break
            if found:break
        self.assertTrue(found)
