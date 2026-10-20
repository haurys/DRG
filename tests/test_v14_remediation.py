"""Bounded v1.4 remediation: physical Course, Gear metadata, and action budgets."""
import copy
import json
import unittest
from pathlib import Path
from engine.simulate import Sim, make_condition

ROOT = Path(__file__).resolve().parents[1]
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
CFG = json.loads((ROOT / 'simulation/config.json').read_text())

def card(cid):
    return copy.deepcopy(CARDS[cid])

def fixture(players=1):
    config = copy.deepcopy(CFG)
    config['player_count'] = players
    sim = Sim(ROOT, config)
    sim.build_course()
    sim.runners = [sim.new_runner(i, 'Balanced', []) for i in range(players)]
    sim.draw, sim.discard = [], []
    return sim, sim.runners[0]

class CoursePhysicalLayout(unittest.TestCase):
    def test_marathon_pairs_thirteen_cards_out_and_back(self):
        sim, _ = fixture()
        self.assertEqual(len(sim.course), 26)
        self.assertEqual(len({s['course_card_id'] for s in sim.course}), 13)
        for position in range(13):
            outbound, returning = sim.course[position], sim.course[25-position]
            self.assertEqual(outbound['course_card_id'], returning['course_card_id'])
            self.assertNotEqual(outbound['side'], returning['side'])
            self.assertEqual((outbound['mile'], returning['mile']), (position+1, 26-position))
            self.assertEqual(len(outbound['quarter_positions']), 4)
            self.assertEqual(len(returning['quarter_positions']), 4)
        self.assertEqual(sim.runners[0]['quarter_mile_space'], 0)
        self.assertEqual(sim.runners[0]['current_course_card'], sim.course[0]['course_card_id'])
        self.assertEqual(sim.course[0]['course_card_id'], sim.course[-1]['course_card_id'])
        self.assertEqual(sim.course[0]['quarter_positions'], [1, 2, 3, 4])
        self.assertEqual(sim.course[-1]['quarter_positions'], [101, 102, 103, 104])

class CardMetadata(unittest.TestCase):
    def test_new_titles_and_printed_nausea(self):
        expected = {'GE-006': 'All-Weather Cap', 'GE-009': 'Split Shorts',
                    'GE-010': 'Glare Shades', 'GE-013': 'Weather Shell',
                    'GE-016': 'Pace Watch', 'GE-020': 'Support Insoles'}
        for cid, title in expected.items():
            self.assertEqual(CARDS[cid]['title'], title)
        self.assertEqual(CARDS['CO-012']['effect_text'], 'Cannot use Fuel')
        self.assertEqual(len(CARDS), 108)

    def test_footwear_flag_is_sole_category_legality(self):
        shoes = {'GE-001','GE-002','GE-004','GE-005','GE-007','GE-011'}
        gear = [c for c in CARDS.values() if c['family']=='Gear']
        self.assertEqual({c['id'] for c in gear if c['is_footwear']}, shoes)
        self.assertTrue(all(c['category']=='Footwear' for c in gear if c['is_footwear']))
        self.assertEqual(CARDS['GE-003']['category'], 'Apparel')
        self.assertFalse(CARDS['GE-003']['is_footwear'])
        for cid in ('GE-007','GE-011'):
            self.assertEqual(CARDS[cid]['category'], 'Footwear')

    def test_shoes_replace_shoes_socks_do_not_occupy_shoe_limit(self):
        for cid in ('GE-001','GE-004','GE-005','GE-007','GE-011'):
            with self.subTest(cid=cid):
                sim, r = fixture()
                r['equipped_gear'] = [{'card': card('GE-002'), 'remaining_turns': None}]
                r['hand'] = [card(cid)]
                self.assertFalse(sim.legal_treat_prepare(r, {'action':'gear','card_id':cid}))
                self.assertTrue(sim.legal_treat_prepare(r, {'action':'gear','card_id':cid,'replace_id':'GE-002'}))
                self.assertFalse(any(p['card_id']==cid and not p.get('replace_id')
                                     for p in sim.treat_candidates(r) if p))
        sim, r = fixture()
        r['equipped_gear'] = [{'card': card('GE-001'), 'remaining_turns': None}]
        condition=make_condition(card('CO-005'))
        r['active_conditions']=[condition]
        r['hand']=[card('GE-003')]
        self.assertTrue(sim.legal_treat_prepare(r, {'action':'attach','card_id':'GE-003','condition_id':'CO-005'}))
        # Broad category has no bearing on an otherwise legal non-footwear installation.
        other = card('GE-009')
        other['category'] = 'Footwear'
        r['hand'] = [other]
        self.assertTrue(sim.legal_treat_prepare(r, {'action':'gear','card_id':'GE-009'}))

    def test_nausea_blocks_effect_but_allows_zero_cost_fuel_movement(self):
        sim, r = fixture()
        r['active_conditions']=[make_condition(card('CO-012'))]
        r['hand']=[card('FU-001')]
        self.assertFalse(sim.legal_treat_prepare(r, {'action':'fuel','card_id':'FU-001','choice':'energy'}))
        self.assertEqual(CARDS['FU-001']['movement_energy_cost'], 0)
        sim.turn(r, {'movement_cards':['FU-001']})
        plays=[e['payload'] for e in sim.events if e['type']=='PLAY']
        self.assertEqual([(p['card']['id'],p['mode']) for p in plays], [('FU-001','MOVEMENT')])
        self.assertFalse(any(e['type']=='FUEL_USE' for e in sim.events))

class ActionCosts(unittest.TestCase):
    def test_new_card_treat_uses_one_action_and_one_play(self):
        cases=[('TR-001', {'action':'training','card_id':'TR-001'}),
               ('GE-006', {'action':'gear','card_id':'GE-006'}),
               ('FU-001', {'action':'fuel','card_id':'FU-001','choice':'energy'}),
               ('GE-003', {'action':'attach','card_id':'GE-003','condition_id':'CO-005'})]
        for cid, plan in cases:
            with self.subTest(action=plan['action']):
                sim, r=fixture()
                r['hand']=[card(cid),card('FU-002')]
                if plan['action']=='attach':
                    r['active_conditions']=[make_condition(card('CO-005'))]
                sim.turn(r, {'treat_prepare':plan,'movement_cards':['FU-002']})
                self.assertEqual(r['stats']['treat_prepare_actions'],1)
                self.assertEqual(r['stats']['cards_played'],2)
                self.assertEqual([e['payload']['card']['id'] for e in sim.events if e['type']=='PLAY'],['FU-002'])
                self.assertEqual([e['payload']['movement_effort'] for e in sim.events
                                  if e['type']=='TREAT_PREPARE'],[0])

    def test_relocate_uses_action_without_new_card_play(self):
        sim,r=fixture()
        r['equipped_gear']=[{'card':card('GE-006'),'remaining_turns':None,'installed_turn':0}]
        r['hand']=[card('FU-001'),card('FU-002')]
        sim.turn(r, {'treat_prepare':{'action':'relocate','card_id':'GE-006'},
                     'movement_cards':['FU-001','FU-002']})
        self.assertEqual(r['stats']['treat_prepare_actions'],1)
        self.assertEqual(r['stats']['cards_played'],2)
        self.assertEqual(len([e for e in sim.events if e['type']=='PLAY']),2)

    def test_assistance_uses_treat_but_no_card_play(self):
        sim,r=fixture(2)
        helper=sim.runners[1]
        r['energy'],r['will_available']=0,False
        r['hand']=[card('FU-002')]
        helper['hand']=[card('FU-001')]
        helper['quarter_mile_space']=1
        self.assertTrue(sim.request_assistance(r))
        self.assertEqual(r['stats']['treat_prepare_actions'],1)
        self.assertEqual(r['stats']['cards_played'],0)
        self.assertIn('FU-001',[c['id'] for c in r['hand']])
        self.assertEqual(helper['stats']['treat_prepare_actions'],0)

    def test_slot_movement_uses_play_without_treat(self):
        sim,r=fixture()
        r['race_turn_number']=2
        r['active_training']=[{'card':card('TR-019'),'remaining_turns':None,'installed_turn':0}]
        sim.turn(r, {'movement_cards':['TR-019']})
        self.assertEqual(r['stats']['treat_prepare_actions'],0)
        self.assertEqual(r['stats']['cards_played'],1)
        self.assertEqual(len([e for e in sim.events if e['type']=='SLOT_SACRIFICE']),1)

if __name__=='__main__':
    unittest.main()
