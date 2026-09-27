import copy, importlib.util, json, random, unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('final_rules',ROOT/'engine/simulate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def card(cid):
 return next(c for c in json.loads((ROOT/'data/race_cards.json').read_text()) if c['id']==cid)

class FinalRules(unittest.TestCase):
 def test_gear_ids_efforts_and_family_counts(self):
  self.assertEqual({i:(card(i)['title'],card(i)['effort']) for i in ['GE-004','GE-007','GE-011','GE-015','GE-017']},{'GE-004':('Cushioned Shoes',6),'GE-007':('Tempo Shoes',7),'GE-011':('Carbon Racers',8),'GE-015':('Lightweight Singlet',5),'GE-017':('Recovery Sleeves',5)})
  cards=json.loads((ROOT/'data/race_cards.json').read_text());self.assertEqual(Counter(c['family'] for c in cards),Counter({'Training':20,'Gear':20,'Fuel':22,'Event':30,'Condition':16}))
 def test_course_distribution(self):
  sides=json.loads((ROOT/'data/course_cards.json').read_text());self.assertEqual(Counter(x['difficulty'] for x in sides),Counter({1:9,2:14,3:9,4:12,5:5,6:7,7:1,8:3}));self.assertEqual(sum(x['difficulty'] for x in sides),210)
 def test_numeric_severity_and_zero_suppression(self):
  c=m.make_condition(card('CO-007'));self.assertEqual(m.condition_effects(c,'Race')['effort_penalty'],2);m.set_suppression(c,2);self.assertEqual(m.condition_effects(c,'Push')['effort_penalty'],0)
  m.set_suppression(c,0);self.assertEqual(c['effective_severity'],2)
  s=m.make_condition(card('CO-009'));self.assertEqual(m.condition_effects(s,surface='Asphalt')['difficulty_penalty'],4)
 def test_binary_conditions_suppressed_at_zero(self):
  c=m.make_condition(card('CO-001'));m.set_suppression(c,4);self.assertTrue(m.condition_effects(c,'Push')['push_available'])
  self.assertTrue(m.anti_chafe_prevents('Hot Spot',True));self.assertFalse(m.anti_chafe_prevents('Blister',True))
 def test_remedies_and_twisted_ankle(self):
  self.assertIsNone(m.apply_remedy(m.make_condition(card('CO-010')),'Water'))
  persistent=m.make_condition(card('CO-003'));persistent['title']='Tight Calf';persistent['current_severity']=0;self.assertTrue(persistent['persistent'])
  self.assertIsNone(m.apply_remedy(m.make_condition(card('CO-015')),'Aid'))
 def test_tough_decision_zero_one_two(self):
  event=card('EV-017');a=card('TR-001');b=card('TR-002')
  self.assertEqual(len(m.tough_decision_cycle([event])),0);self.assertEqual(len(m.tough_decision_cycle([event,a])),1);self.assertEqual(len(m.tough_decision_cycle([event,a,b])),2)
 def test_sudden_rain_placement_expiry_stack_and_final(self):
  a=m.sudden_rain('EV-005',4,26,3);b=m.sudden_rain('X',4,26,4);self.assertEqual(a['affected_mile'],5);self.assertEqual(m.course_event_bonus([a,b],5),2)
  live=[a,b]
  for _ in range(3):live=m.tick_course_events(live)
  self.assertEqual(len(live),2);live=m.tick_course_events(live);self.assertEqual(live,[]);self.assertIsNone(m.sudden_rain('EV-005',26,26,3))
 def test_good_line_data(self):
  c=card('EV-014');self.assertEqual((c['title'],c['effect_type'],c['effort']),('Good Line','IGNORE_COURSE_DIFFICULTY',4))
 def test_canonical_event_replacements(self):
  self.assertEqual((card('EV-023')['title'],card('EV-023')['effort'],card('EV-023')['effect_type']),('Perfect Rhythm',10,'NONE'))
  self.assertEqual((card('EV-025')['title'],card('EV-030')['title']),('Wild Goose Chase','Untied Lace'))
 def test_high_five_pack_and_solo(self):
  self.assertEqual(m.high_five_beneficiaries('P1',['P1','P2']),['P1','P2']);self.assertEqual(m.high_five_beneficiaries('P1',[]),['P1'])
 def test_helpful_runner_transfer_limit_lock_and_repeat(self):
  c=copy.deepcopy(card('EV-020'));a={'player_id':'A','hand':[c],'energy':4};b={'player_id':'B','hand':[],'energy':3}
  self.assertTrue(m.transfer_helpful_runner(c,a,b,2));self.assertFalse(m.helpful_runner_playable(c,2));self.assertTrue(m.helpful_runner_playable(c,3));self.assertTrue(m.transfer_helpful_runner(c,b,a,3))
  full={'player_id':'C','hand':[{}]*7};self.assertFalse(m.transfer_helpful_runner(c,a,full,4))
 def test_gut_check_hand_total_thresholds_empty_and_modifiers(self):
  hand=[card('TR-001'),card('FU-001')];x=m.gut_check(hand,['Strength','Mental Toughness'],['Pace Band'],14);self.assertEqual((x['hand_effort'],x['modifiers'],x['total']),(10,4,14));self.assertTrue(x['passed'])
  self.assertEqual(m.gut_check([],threshold=25)['energy_loss'],2);self.assertEqual(m.GUT_CHECK_THRESHOLDS['marathon'],{10:25,18:30,23:35})
 def test_direct_movement_separate(self):
  x=m.resolve_movement(3,4,[1,8,1],12,direct_movement=1);self.assertEqual(x['direct_quarter_miles'],1);self.assertEqual(x['quarter_miles'],x['base_quarter_miles']+1)
 def test_training_difficulty_and_boundary(self):
  self.assertEqual(m.training_difficulty_reduction('Hill Repeats','Incline'),2);self.assertEqual(m.training_difficulty_reduction('Hill Repeats','Steep Incline'),1)
  self.assertEqual(m.training_difficulty_reduction('Downhill Practice','Descent'),2);self.assertEqual(m.training_difficulty_reduction('Downhill Practice','Steep Descent'),1)
  sore=m.make_condition(card('CO-009'));seg={'difficulty':3,'surface':'Asphalt','elevation':'Incline'};self.assertEqual(m.effective_difficulty(seg,[sore],['Hill Repeats'],1),6)
  x=m.resolve_movement(3,8,[1,5,1],12);self.assertEqual(x['boundaries'][0]['difficulty_change'],4)
 def test_trade_cost_per_participant(self):
  ca=card('TR-001');cb=card('TR-002');a={'hand':[ca],'exchanges_used':0};b={'hand':[cb],'exchanges_used':0};self.assertTrue(m.apply_trade(a,b,ca,cb));self.assertEqual((a['exchanges_used'],b['exchanges_used']),(1,1))
 def test_deck_recycle_exclusion_empty_and_determinism(self):
  cards=[copy.deepcopy(card('TR-001')),copy.deepcopy(card('TR-002'))]
  d1=[];q1=copy.deepcopy(cards);audit=[];self.assertTrue(m.recycle_discard(d1,q1,random.Random(4),{'TR-002'},audit));self.assertEqual([c['id'] for c in d1],['TR-001']);self.assertEqual([c['id'] for c in q1],['TR-002'])
  d2=[];q2=copy.deepcopy(cards);m.recycle_discard(d2,q2,random.Random(4),set());d3=[];q3=copy.deepcopy(cards);m.recycle_discard(d3,q3,random.Random(4),set());self.assertEqual(d2,d3)
  self.assertFalse(m.recycle_discard([],[],random.Random(1)))

if __name__=='__main__':unittest.main()
