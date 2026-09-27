import copy, importlib.util, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sim',ROOT/'engine/simulate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Foundation(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cards=m.load_json(ROOT/'data/race_cards.json');cls.course=m.load_json(ROOT/'data/course_cards.json');cls.cfg=m.load_json(ROOT/'simulation/config.json')
 def test_inventory(self):
  self.assertEqual(len(self.cards),108);self.assertEqual(len({x['id'] for x in self.cards}),108)
  counts={f:sum(x['family']==f for x in self.cards) for f in ['Training','Gear','Fuel','Event','Condition']};self.assertEqual(counts,{'Training':20,'Gear':20,'Fuel':22,'Event':30,'Condition':16})
  self.assertTrue(all(x['effort'] is None or 0<=x['effort']<=10 for x in self.cards))
 def test_course_data(self):
  self.assertEqual(len(self.course),60);self.assertEqual(len({x['id'] for x in self.course}),60);self.assertEqual(len({x['course_card_id'] for x in self.course}),30)
  self.assertTrue(all(1<=x['difficulty']<=10 for x in self.course));self.assertTrue(set(x['elevation'] for x in self.course)<=set(['Steep Descent','Descent','Flat','Rolling','Incline','Steep Incline']))
 def test_layouts(self):
  for fmt,count,segments,quarters in [('marathon',13,26,104),('half',7,13,52)]:
   c=copy.deepcopy(self.cfg);c['race_format']=fmt;s=m.Sim(ROOT,c);s.build_course();self.assertEqual(len({x['course_card_id'] for x in s.course}),count);self.assertEqual(len(s.course),segments);self.assertEqual(sum(len(x['quarter_positions']) for x in s.course),quarters)
 def test_setup_rules(self):
  s=m.Sim(ROOT,self.cfg);s.setup();self.assertTrue(all(len(r['hand'])==7 for r in s.runners));self.assertTrue(all(all(c['family']!='Condition' for c in r['hand']) for r in s.runners));self.assertTrue(all(r['exchanges_used']<=3 for r in s.runners));self.assertTrue(all(r['pace'] for r in s.runners))
 def test_modes_and_movement(self):
  self.assertEqual(m.movement(0),0);self.assertEqual(m.movement(1),1);self.assertEqual(m.movement(14),7);self.assertEqual(m.movement(15),8)
 def test_determinism(self):
  cfg=copy.deepcopy(self.cfg);cfg['player_count']=2
  a=m.Sim(ROOT,copy.deepcopy(cfg));b=m.Sim(ROOT,copy.deepcopy(cfg));a.setup();b.setup()
  a.run_round();b.run_round();self.assertEqual(a.events,b.events);self.assertEqual(a.turn_records,b.turn_records)
 def test_information_boundary(self):
  s=m.Sim(ROOT,self.cfg);s.setup();pub=m.public_runner(s.runners[0]);self.assertNotIn('hand',pub)
if __name__=='__main__':unittest.main()
