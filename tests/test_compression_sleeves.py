"""Compression Sleeves: slotted prevents Cramp and Tight Calf; attaches only to Tight Calf."""
import unittest

from engine.simulate import make_condition
from tests.test_v14_candidate import card, fixture


class CompressionSleeves(unittest.TestCase):
    def test_slotted_prevents_cramp_and_tight_calf(self):
        for cid in ('CO-001', 'CO-003'):
            with self.subTest(condition=cid):
                sim, r = fixture()
                sim.equip_gear(r, card('GE-019'))
                sim.draw = [card('TR-001'), card(cid)]
                sim.draw_one(r)
                self.assertEqual(r['active_conditions'], [])
                prevent = [e for e in sim.events if e['type'] == 'CONDITION_PREVENT']
                self.assertEqual(prevent[-1]['payload'], {'condition': cid, 'source': 'Compression Sleeves'})

    def test_slotted_does_not_prevent_other_conditions(self):
        sim, r = fixture()
        sim.equip_gear(r, card('GE-019'))
        sim.draw = [card('TR-001'), card('CO-005')]
        sim.draw_one(r)
        self.assertEqual([c['title'] for c in r['active_conditions']], ['Blister'])

    def test_attaches_to_tight_calf_not_cramp(self):
        sim, r = fixture()
        cramp, calf = make_condition(card('CO-001')), make_condition(card('CO-003'))
        r['active_conditions'] = [cramp, calf]
        self.assertFalse(sim.attach_gear(r, card('GE-019'), cramp))
        self.assertTrue(sim.attach_gear(r, card('GE-019'), calf))
        self.assertEqual(calf['effective_severity'], 1)

    def test_can_be_slotted_from_hand(self):
        sim, r = fixture()
        r['hand'] = [card('GE-019')]
        plans = sim.treat_candidates(r)
        self.assertIn('gear', {plan['action'] for plan in plans if plan})


if __name__ == '__main__':
    unittest.main()
