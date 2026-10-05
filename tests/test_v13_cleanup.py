"""Bounded v1.3 station, assistance, and DNF regressions; no marathon."""
import copy
import json
import unittest
from pathlib import Path

from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
FUEL = [c['id'] for c in CARDS.values() if c['family'] == 'Fuel' and c['effort'] >= 4]


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(position=0, hand=(), energy=0, will=False):
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    p4 = sim.new_runner(3, 'Course Planner', [card(cid) for cid in hand])
    p4.update(quarter_mile_space=position, distance_completed=position / 4,
              energy=energy, will_available=will)
    sim.runners = [p4]
    sim.round = 1
    sim.draw = []
    return sim, p4


def add_helper(sim, hand, position=44):
    helper = sim.new_runner(0, 'Balanced', [card(cid) for cid in hand])
    helper.update(quarter_mile_space=position, distance_completed=position / 4)
    sim.runners.append(helper)
    return helper


class StationTreatment(unittest.TestCase):
    def test_p4_mile8_all_eligible_and_fuel_legality(self):
        sim, p4 = fixture(position=31, hand=('FU-001',))
        p4['active_conditions'] = [m.make_condition(card(cid)) for cid in
                                    ('CO-012', 'CO-013', 'CO-015', 'CO-016', 'CO-010', 'CO-004')]
        p4['equipped_gear'] = [{'card': card('GE-012'), 'remaining_turns': None}]
        self.assertFalse(sim.fuel_available(p4))
        sim.resolve_milestones(p4, 31, 32)
        remaining = {c['title']: c['current_severity'] for c in p4['active_conditions']}
        self.assertNotIn('Nausea', remaining)
        self.assertNotIn('Gashed Knee', remaining)
        self.assertNotIn('Dehydrated', remaining)
        self.assertEqual(remaining['Twisted Ankle'], 4)
        self.assertEqual(remaining['Heat Exhaustion'], 4)
        self.assertEqual(remaining['Dead Legs'], 5)
        self.assertTrue(sim.fuel_available(p4))
        self.assertEqual(p4['energy'], 1)  # Hydration Belt; independent of remedies.
        self.assertEqual(sum(e['type'] == 'CONDITION_REMEDY' for e in sim.events), 5)

    def test_multiple_water_fixture_and_noneligible_unchanged(self):
        sim, p4 = fixture(position=15)
        sim.station_zero_remedies['Water'].add('Cramp')  # Future data fixture.
        p4['active_conditions'] = [m.make_condition(card(cid)) for cid in
                                    ('CO-010', 'CO-001', 'CO-004')]
        sim.resolve_milestones(p4, 15, 16)
        self.assertEqual([c['title'] for c in p4['active_conditions']], ['Dead Legs'])

    def test_aid_partial_reduction_and_persistence(self):
        sim, p4 = fixture(position=31)
        p4['active_conditions'] = [m.make_condition(card(cid)) for cid in ('CO-015', 'CO-016')]
        sim.resolve_milestones(p4, 31, 32)
        self.assertEqual([c['current_severity'] for c in p4['active_conditions']], [4, 4])
        self.assertTrue(p4['active_conditions'][0]['persistent'])


class AssistanceAndDNF(unittest.TestCase):
    def stranded(self, helper_hand=('EV-021',), helper_position=44):
        sim, p4 = fixture(position=38, hand=FUEL[:7])
        p4['active_conditions'] = [m.make_condition(card('CO-012'))]
        helper = add_helper(sim, helper_hand, helper_position)
        return sim, p4, helper

    def test_recoverable_p4_swap_and_action_budgets(self):
        sim, p4, helper = self.stranded()
        before = copy.deepcopy(helper)
        self.assertFalse(sim.continuation_paths(p4)['viable'])
        self.assertTrue(sim.request_assistance(p4))
        self.assertIn('EV-021', [c['id'] for c in p4['hand']])
        self.assertEqual(p4['stats']['treat_prepare_actions'], 1)
        self.assertEqual(p4['stats']['cards_played'], 0)
        self.assertEqual(helper['stats'], before['stats'])
        self.assertEqual(helper['race_turn_number'], before['race_turn_number'])
        self.assertEqual(sum(e['type'] == 'ASSISTANCE_SWAP' for e in sim.events), 1)
        self.assertEqual([e['payload']['card_plays_used'] for e in sim.events
                          if e['type'] == 'ASSISTANCE_SWAP'], [0])
        self.assertFalse(sim.evaluate_dnf(p4, True, treat_available=False))

    def test_helper_selection_and_stable_ties(self):
        sim, p4, leader = self.stranded()
        second = add_helper(sim, ('EV-022',), 42)
        self.assertEqual(sim.assistance_helper(p4)[0], leader)
        p4['quarter_mile_space'] = 48
        self.assertEqual(sim.assistance_helper(p4)[0], leader)
        self.assertEqual(sim.assistance_helper(p4)[2], 2)
        p4['quarter_mile_space'] = 44
        self.assertEqual(sim.assistance_helper(p4)[0], leader)  # P1 before P4.
        second['quarter_mile_space'] = 44
        self.assertEqual(sim.assistance_helper(p4)[0], leader)

    def test_all_swaps_evaluated_and_meaningless_swap_rejected(self):
        sim, p4, helper = self.stranded(helper_hand=(FUEL[7],))
        self.assertFalse(sim.request_assistance(p4))
        evaluation = next(e['payload'] for e in sim.events if e['type'] == 'ASSISTANCE_SWAP_EVALUATE')
        self.assertEqual(len(evaluation['legal_swaps']), 7)
        self.assertEqual(evaluation['rescue_capable_count'], 0)
        self.assertEqual([c['id'] for c in helper['hand']], [FUEL[7]])
        self.assertTrue(sim.evaluate_dnf(p4, True, treat_available=False))
        self.assertEqual(p4['race_status'], 'DNF')
        self.assertIsNone(p4['finish_order'])
        self.assertEqual((p4['distance_completed'], p4['energy']), (9.5, 0))

    def test_energy_or_will_alone_never_dnf(self):
        for energy, will in ((0, True), (1, False)):
            with self.subTest(energy=energy, will=will):
                sim, p4, _ = self.stranded()
                p4.update(energy=energy, will_available=will)
                self.assertFalse(sim.evaluate_dnf(p4, True))

    def test_zero_cost_movement_and_recovery_block_dnf(self):
        for cid, nausea in (('FU-001', False), ('EV-021', True), ('FU-001', True)):
            with self.subTest(card=cid, nausea=nausea):
                sim, p4 = fixture(position=0, hand=(cid,))
                if nausea:
                    p4['active_conditions'] = [m.make_condition(card('CO-012'))]
                self.assertFalse(sim.evaluate_dnf(p4, True))

    def test_replenishment_and_reachable_station_block_dnf(self):
        sim, p4 = fixture(position=15, hand=())
        sim.draw = [card('EV-021')]
        self.assertFalse(sim.evaluate_dnf(p4, True))
        sim, p4 = fixture(position=15, hand=('FU-001',))
        p4['active_conditions'] = [m.make_condition(card('CO-010'))]
        self.assertFalse(sim.evaluate_dnf(p4, True))

    def test_assistance_must_be_evaluated_first(self):
        sim, p4, _ = self.stranded(helper_hand=(FUEL[7],))
        self.assertFalse(sim.evaluate_dnf(p4, False))
        self.assertFalse(p4['dnf'])

    def test_received_fuel_next_turn_no_second_treat(self):
        sim, p4, _ = self.stranded(helper_hand=('FU-001',))
        p4['quarter_mile_space'] = 4  # Mile 2 Difficulty 2: Effort 3 advances.
        p4['distance_completed'] = 1.0
        self.assertFalse(sim.fuel_available(p4))
        self.assertEqual(m.movement_energy_cost(card('FU-001')), 0)
        self.assertTrue(sim.request_assistance(p4))
        self.assertIn('FU-001', [c['id'] for c in p4['hand']])
        self.assertEqual(sim.continuation_paths(p4, allow_treat=False)['kind'],
                         'forward_movement')
        self.assertFalse(sim.evaluate_dnf(p4, True, treat_available=False))
        sim, p4 = fixture(position=0, hand=('FU-002',))
        self.assertTrue(sim.continuation_paths(p4, allow_treat=False)['viable'])
        self.assertEqual(sim.continuation_paths(p4, allow_treat=False)['kind'],
                         'next_turn_treat_recovery')

    def test_nausea_blocks_fuel_effect_only_rescue(self):
        sim, p4, helper = self.stranded(helper_hand=('FU-002',))
        self.assertFalse(sim.fuel_available(p4))
        self.assertEqual(m.movement_energy_cost(card('FU-002')), 1)
        self.assertFalse(sim.request_assistance(p4))
        self.assertEqual([c['id'] for c in helper['hand']], ['FU-002'])
        self.assertTrue(sim.evaluate_dnf(p4, True, treat_available=False))

    def test_dnf_skips_future_turn_and_mixed_termination(self):
        sim, p4, helper = self.stranded(helper_hand=(FUEL[7],))
        sim.request_assistance(p4)
        sim.evaluate_dnf(p4, True, treat_available=False)
        self.assertIsNone(sim.turn(p4))
        self.assertEqual(p4['race_turn_number'], 0)
        helper.update(finish_pending=True, finish_round=sim.round, finish_turn=1)
        sim.pending_finishers = [helper]
        sim.end_round()
        self.assertEqual((helper['race_status'], p4['race_status']), ('FINISHED', 'DNF'))
        sim.setup = lambda: None  # bounded termination check; no second marathon.
        self.assertEqual(sim.run()[-1]['type'], 'SIMULATION_END')


if __name__ == '__main__':
    unittest.main()
