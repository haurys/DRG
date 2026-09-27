import importlib.util, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sim_boundary',ROOT/'engine/simulate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def resolve(start,result,difficulties):
 return m.resolve_movement(start,result,difficulties,len(difficulties)*4)

class MovementBoundaryRules(unittest.TestCase):
 def test_a_no_boundary_crossing(self):
  x=resolve(16,4,[2]*10);self.assertEqual((x['to_space'],x['quarter_miles'],len(x['boundaries'])),(18,2,0))
 def test_b_equal_difficulty(self):
  x=resolve(19,10,[2]*10);self.assertEqual(x['quarter_miles'],5);self.assertEqual(x['boundaries'][0]['adjusted_remaining'],8)
 def test_c_harder_terrain(self):
  x=resolve(19,10,[2]*5+[6]+[2]*4);self.assertEqual(x['quarter_miles'],3);self.assertEqual(x['boundaries'][0]['difficulty_change'],4)
 def test_d_easier_terrain(self):
  x=resolve(19,6,[6]*5+[2]+[6]*4);self.assertEqual(x['quarter_miles'],5);self.assertEqual(x['boundaries'][0]['adjusted_remaining'],8)
 def test_e_harder_remainder_zero(self):
  x=resolve(19,6,[2]*5+[6]+[2]*4);self.assertEqual(x['to_space'],20);self.assertTrue(x['boundaries'][0]['stopped']);self.assertEqual(x['boundaries'][0]['adjusted_remaining'],0)
 def test_f_harder_remainder_below_zero(self):
  x=resolve(19,5,[2]*5+[6]+[2]*4);self.assertEqual(x['to_space'],20);self.assertLess(x['boundaries'][0]['adjusted_remaining'],0)
 def test_g_two_boundaries(self):
  x=resolve(19,15,[2]*10);self.assertEqual(x['quarter_miles'],8);self.assertEqual(len(x['boundaries']),2)
 def test_h_harder_then_easier(self):
  x=resolve(19,15,[2]*5+[6,2]+[2]*3);self.assertEqual([b['difficulty_change'] for b in x['boundaries']],[4,-4])
 def test_i_easier_then_harder(self):
  x=resolve(19,15,[6]*5+[2,6]+[6]*3);self.assertEqual([b['difficulty_change'] for b in x['boundaries']],[-4,4])
 def test_j_two_mile_cap_across_boundaries(self):
  x=resolve(19,30,[2]*10);self.assertEqual(x['quarter_miles'],8);self.assertTrue(x['cap_prevented']);self.assertEqual(x['result_wasted_above_cap'],14)
 def test_k_one_effort_card(self):
  self.assertEqual(m.calculate_total_effort([{'effort':8}],['EFFORT']),8)
 def test_l_two_effort_cards(self):
  self.assertEqual(m.calculate_total_effort([{'effort':8},{'effort':4}],['EFFORT','EFFORT']),12)
 def test_m_effort_plus_energy_effect(self):
  self.assertEqual(m.calculate_total_effort([{'effort':8},{'effort':7}],['EFFORT','ENERGY_EFFECT']),8)
 def test_n_nonpositive_result(self):
  for result in (0,-3):self.assertEqual(resolve(17,result,[4]*10)['quarter_miles'],0)
 def test_o_begins_exactly_on_boundary(self):
  x=resolve(20,4,[2]*5+[6]+[2]*4);self.assertEqual(x['quarter_miles'],2);self.assertEqual(len(x['boundaries']),0)
 def test_p_quarter_before_boundary(self):
  x=resolve(19,4,[2]*10);self.assertEqual(x['to_space'],21)
 def test_q_half_before_boundary(self):
  x=resolve(18,4,[2]*10);self.assertEqual(x['to_space'],20)
 def test_r_three_quarters_before_boundary(self):
  x=resolve(17,4,[2]*10);self.assertEqual(x['to_space'],19);self.assertEqual(len(x['boundaries']),0)

if __name__=='__main__':unittest.main()
