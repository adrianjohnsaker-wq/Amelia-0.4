import copy
import hashlib
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from drift1a_c1.engine import NAMES
from drift1a_c1.metrics import (blank, mutual_information, outcome_predictability,
    boundary_diagnostic, PRIMARY_KEYS, ranks, flag_summary, route_rarity, retrospective, summarize)
from drift1a_c1.common import week, read
import test_c1


def arm_fixture(routes=None):
    t=blank();t.pop('lag_pairs')
    t.update(warp_fraction=.5,mean_completed_length=4.,distinct_routes_per_100_episodes=10.,
        zone_occupancy=[.1]*10,remembered_exit_ratio=1.,routes=routes or {},completed=100,
        outcome_predictability_at_lag={str(k):dict(status='sufficient',miller_madow_bits=.01) for k in range(1,9)})
    return dict(boundary_ending_rate=.25,episode_classes={'traversal':t})


class Amendments(unittest.TestCase):
    def test_boundary_entry_diagnostic_is_canonical_only_and_has_fixed_outcomes(self):
        for z,outcome in [(0,'Plex'),(9,'Plex'),(3,'Warp'),(6,'Warp')]:
            self.assertTrue(boundary_diagnostic(z,1,'boundary',outcome))
            self.assertFalse(boundary_diagnostic(z,2,'boundary',outcome))
            self.assertFalse(boundary_diagnostic(z,1,'cap',None))
            self.assertFalse(boundary_diagnostic(z,1,'boundary','Warp' if outcome=='Plex' else 'Plex'))

    def test_miller_madow_against_hand_computed_two_by_two_table(self):
        pairs=[(0,'W')]*3+[(0,'P')]+[(1,'W')]+[(1,'P')]*3
        m=mutual_information(pairs)
        expected=.75*math.log2(1.5)+.25*math.log2(.5)
        self.assertAlmostEqual(m['bits'],expected)
        self.assertAlmostEqual(m['miller_madow_bits'],expected-1/(16*math.log(2)))
        self.assertEqual((m['m_Z'],m['m_O'],m['m_ZO']),(2,2,4))
        balanced=mutual_information([(0,'W'),(0,'P'),(1,'W'),(1,'P')])
        self.assertLess(balanced['miller_madow_bits'],0)

    def test_permutation_stream_is_deterministic_and_marks_small_n(self):
        pairs=[(i%3,'Warp' if i%5<2 else 'Plex') for i in range(80)]
        a=outcome_predictability(pairs,'2026-W42','C',4)
        self.assertEqual(a,outcome_predictability(pairs,'2026-W42','C',4))
        self.assertEqual(a['seed_sha256'],hashlib.sha256(b'DRIFT-1A-C1-PERM|2026-W42|C|4').hexdigest())
        self.assertEqual(a['permutations'],200)
        self.assertEqual(outcome_predictability(pairs[:49],'2026-W42','C',4)['status'],'insufficient')
        self.assertEqual(outcome_predictability(pairs[:50],'2026-W42','C',4)['status'],'sufficient')
        self.assertIsNone(outcome_predictability([],'2026-W42','C',4)['bits'])

    def test_flags_use_exactly_declared_thirty_not_derived_counts(self):
        arms={a:arm_fixture() for a in NAMES}
        arms['C']['ticks']=1000000
        arms['C']['episode_classes']['traversal']['warp_fraction']=.75
        rows=ranks(arms);f=flag_summary(rows,{})
        self.assertEqual(list(rows),PRIMARY_KEYS);self.assertEqual((f['N'],f['N_compared'],f['F']),(30,30,1))
        self.assertAlmostEqual(f['expected_flags'],60/9)
        tied=rows['mean_completed_length'];self.assertEqual((tied['rank_low'],tied['rank_high']),(1,9))
        arms['C']['episode_classes']['traversal']['outcome_predictability_at_lag']['8']['status']='insufficient'
        rows=ranks(arms);f=flag_summary(rows,{})
        self.assertEqual(f['N_compared'],29)
        self.assertEqual(f['cross_week']['outcome_mm_lag_8']['weeks_compared'],0)
        prior={'old':{'report':{'references':rows}}};f=flag_summary(rows,prior)
        self.assertEqual(f['cross_week']['warp_fraction']['weeks_flagged'],2)

    def test_leave_one_out_rarity_swaps_symmetrically(self):
        arms={a:arm_fixture() for a in NAMES}
        for a,r in [('C',{'shared':2,'onlyC':1}),('R01',{'shared':1,'onlyR':1}),('R02',{'shared':3})]:
            arms[a]['episode_classes']['traversal']['routes']=r
        rarity=route_rarity(arms);self.assertFalse(rarity['C']['shared']);self.assertTrue(rarity['C']['onlyC'])
        result=retrospective(arms,{},'2026-W42')
        swapped=copy.deepcopy(arms);swapped['C'],swapped['R01']=swapped['R01'],swapped['C']
        other=retrospective(swapped,{},'2026-W42')
        self.assertEqual(result['C'],other['R01']);self.assertEqual(result['R01'],other['C'])

    def test_rare_at_first_is_retained_and_seals_are_cited(self):
        arms={a:arm_fixture({'route':1} if a=='C' else {}) for a in NAMES}
        first=retrospective(arms,{},'2026-W41')
        earlier={'2026-W41':{'report':{'arms':copy.deepcopy(arms),'retrospective':first},'seal_digest':'seal41'}}
        for a in ('R01','R02','R03'):arms[a]['episode_classes']['traversal']['routes']={'route':1}
        second=retrospective(arms,earlier,'2026-W42')
        self.assertEqual(second['C']['reference_rare_count'],0)
        rare=second['C']['recurring_rare_routes'][0]
        self.assertEqual((rare['first_week'],rare['recurrence_weeks'],rare['first_seal_digest']),('2026-W41',['2026-W42'],'seal41'))


class RecordedClasses(unittest.TestCase):
    setUp = test_c1.C1.setUp
    tearDown = test_c1.C1.tearDown
    run_ticks = test_c1.C1.run_ticks
    def test_recorded_class_accounting_and_canonical_diagnostic(self):
        self.run_ticks(150)
        data=summarize(self.e.records())
        for arms in data.values():
            for a,m in arms.items():
                t=m['episode_classes']['traversal'];b=m['episode_classes']['boundary_entry']
                self.assertEqual(t['ticks']+b['ticks'],m['ticks'])
                self.assertEqual(t['completed']+b['completed'],m['completed'])
                d=m['boundary_entry_diagnostic']
                self.assertEqual(d['status'],'NOT_APPLICABLE' if a.startswith('G') else 'PASS')
                if not a.startswith('G'):self.assertEqual(set(b['length_distribution'])-{'1'},set())

    def test_diagnostic_failure_is_written_as_an_incident(self):
        from datetime import datetime,timezone
        from drift1a_c1.engine import Engine,genesis
        from drift1a_c1.beacon import SyntheticBeacon,SyntheticSealer,round_time
        from drift1a_c1.reports import weekly
        with tempfile.TemporaryDirectory() as root:
            now=[datetime(2026,10,11,23,59,tzinfo=timezone.utc).timestamp()-600]
            seal=SyntheticSealer(lambda:now[0]);g=genesis(root,'SIMULATION',now[0],seal)
            e=Engine(root,SyntheticBeacon(),seal,lambda:now[0]);now[0]=round_time(g['R0'])+70;e.ingest(now[0],1)
            summaries=summarize(e.records());w=next(iter(summaries))
            summaries[w]['C']['boundary_entry_diagnostic']=dict(status='FAIL',checked=1,failures=[{'fixture':True}])
            with patch('drift1a_c1.reports.summarize',return_value=summaries):weekly(e)
            self.assertIn('canonical_boundary_entry_diagnostic',(Path(root)/'record/incidents.jsonl').read_text())

