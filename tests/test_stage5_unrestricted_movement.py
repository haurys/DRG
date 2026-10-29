"""Bounded Stage 5 conversion, traversal, and live/preview checks."""

import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim, diagnostics, movement, resolve_movement


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {card['id']: card for card in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(card_id):
    return copy.deepcopy(CARDS[card_id])


def fixture(hand=('EV-023', 'TR-019'), position=0):
    sim = Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    for segment in sim.course:
        segment['difficulty'] = 0
    sim.round = 1
    runner = sim.new_runner(0, 'Balanced', [card(cid) for cid in hand])
    runner.update(pace='Steady', energy=30, quarter_mile_space=position,
                  distance_completed=position / 4)
    sim.runners = [runner]
    sim.draw = []
    sim.discard = []
    return sim, runner


class UnrestrictedMovement(unittest.TestCase):
    def test_conversion_never_saturates(self):
        for effort, expected in ((-5, 0), (0, 0), (1, 1), (2, 1),
                                 (13, 7), (14, 7), (15, 8), (16, 8),
                                 (17, 9), (18, 9), (19, 10), (20, 10),
                                 (21, 11), (22, 11), (23, 12), (24, 12),
                                 (60, 30), (61, 31)):
            with self.subTest(effort=effort):
                self.assertEqual(movement(effort), expected)
        self.assertEqual([movement(n) for n in range(1, 100)], sorted(
            movement(n) for n in range(1, 100)))

    def test_multiple_boundaries_and_terrain_deltas(self):
        flat = resolve_movement(19, 20, [0] * 26, 104)
        self.assertEqual((flat['quarter_miles'], flat['to_space']), (10, 29))
        self.assertEqual([b['boundary_space'] for b in flat['boundaries']], [20, 24, 28])
        for difficulties, expected in (([0] * 5 + [4] * 21, 8),
                                       ([4] * 5 + [0] * 21, 12)):
            with self.subTest(difficulties=difficulties[:7]):
                actual = resolve_movement(19, 20, difficulties, 104)
                self.assertEqual(actual['quarter_miles'], expected)
                self.assertEqual([b['difficulty_change'] for b in actual['boundaries'][:2]],
                                 [difficulties[5] - difficulties[4],
                                  difficulties[6] - difficulties[5]])

    def test_direct_movement_is_not_clamped_at_two_miles(self):
        plus = resolve_movement(0, 16, [0] * 26, 104, direct_movement=3)
        self.assertEqual((plus['base_quarter_miles'], plus['direct_quarter_miles'],
                          plus['quarter_miles']), (8, 3, 11))
        minus = resolve_movement(0, 20, [0] * 26, 104, direct_movement=-2)
        self.assertEqual((minus['base_quarter_miles'], minus['direct_quarter_miles'],
                          minus['quarter_miles']), (10, -2, 8))
        self.assertEqual(resolve_movement(0, 0, [0] * 26, 104,
                                          direct_movement=10)['quarter_miles'], 10)

    def test_preview_and_live_two_card_movement_above_two_miles(self):
        sim, runner = fixture()
        selected = [card('EV-023'), card('TR-019')]
        for item in selected:
            item.update(use_mode='MOVEMENT', source='hand')
        preview = sim.preview_movement(runner, selected)
        actual = sim.turn(runner, {'movement_cards': ['EV-023', 'TR-019']})
        self.assertEqual((preview['quarter_miles'], actual['quarter_miles']), (10, 10))
        self.assertEqual(sim.turn_records[-1]['cards_played'], 2)
        self.assertEqual(diagnostics(sim)['movement_distribution']['2.50'], 1)

    def test_ai_selects_high_movement_without_clamp(self):
        sim, runner = fixture()
        choice = sim.choose_turn_plan(runner)
        self.assertEqual(choice['movement_quarters'], 10)
        actual = sim.turn(runner)
        self.assertEqual(actual['quarter_miles'], choice['movement_quarters'])

    def test_high_effort_hand_slot_and_two_slots(self):
        for ids, sources in ((('EV-023', 'TR-019'), ('hand', 'active_training')),
                             (('TR-019', 'TR-020'), ('active_training', 'active_training'))):
            with self.subTest(sources=sources):
                sim, runner = fixture(hand=('EV-023',))
                runner['active_training'] = [
                    {'card': card(cid), 'remaining_turns': None, 'installed_turn': -3}
                    for cid in ('TR-019', 'TR-020')]
                actual = sim.turn(runner, {'movement_cards': list(ids),
                                          'card_sources': list(sources)})
                self.assertGreater(actual['quarter_miles'], 8)
                self.assertEqual(len([e for e in sim.events
                                      if e['type'] == 'SLOT_SACRIFICE']), sources.count('active_training'))

    def test_gut_pass_and_failure_interrupt_high_movement(self):
        for requirement, passed in ((0, True), (100, False)):
            with self.subTest(passed=passed):
                sim, runner = fixture(position=36)
                sim.marathon_gut[10] = {'prepared_effort': requirement, 'energy': 0}
                selected = [card('EV-023'), card('TR-019')]
                for item in selected:
                    item.update(use_mode='MOVEMENT', source='hand')
                paid = copy.deepcopy(runner)
                paid['hand'] = []
                preview = sim.preview_gut_progress(paid, sim.preview_movement(paid, selected),
                                                   selected)
                actual = sim.turn(runner, {'movement_cards': ['EV-023', 'TR-019']})
                self.assertEqual(preview['quarter_miles'], actual['quarter_miles'])
                self.assertEqual(bool(runner['gut_stall']), not passed)
                if passed:
                    self.assertGreater(actual['to_space'], 40)
                    self.assertIn(10, runner['gut_cleared'])
                else:
                    self.assertEqual(actual['to_space'], 40)
                    self.assertGreater(actual['gut_movement_lost_quarters'], 0)

    def test_finish_requires_positive_remainder_and_discards_overshoot(self):
        endpoint = resolve_movement(100, 8, [0] * 26, 104)
        self.assertEqual(endpoint['to_space'], 104)
        self.assertFalse(endpoint['positive_finish_movement'])
        sim, runner = fixture(position=100)
        actual = sim.turn(runner, {'movement_cards': ['EV-023', 'TR-019']})
        self.assertEqual(actual['quarter_miles'], 4)
        self.assertTrue(actual['positive_finish_movement'])
        self.assertEqual(actual['finish_discarded_quarters'], 5)
        self.assertEqual(diagnostics(sim)['movement_discarded_at_finish_miles'], 1.25)
        self.assertTrue(runner['finish_pending'])
        self.assertEqual(runner['quarter_mile_space'], 104)
        self.assertEqual(len([event for event in sim.events
                              if event['type'] == 'POST_MOVEMENT_TREAT']), 0)

    def test_multiple_station_crossings_resolve_once_in_order(self):
        sim, runner = fixture(position=12)
        runner['equipped_gear'] = [{'card': card('GE-012'), 'remaining_turns': None}]
        # A synthetic high result exercises several stations in one bounded turn;
        # no physical card or race configuration is changed.
        runner['hand'][0]['effort'] = 40
        before = runner['energy']
        actual = sim.turn(runner, {'movement_cards': ['EV-023', 'TR-019']})
        self.assertEqual(actual['to_space'], 37)
        milestones = [(event['payload']['mile'], event['payload']['kind'])
                      for event in sim.events if event['type'] == 'MILESTONE']
        self.assertEqual(milestones, [(4, 'Water'), (8, 'Water'), (8, 'Aid/Fuel')])
        self.assertEqual(len([event for event in sim.events if event['type'] == 'MILE_CROSS']), 6)
        self.assertEqual(runner['energy'], before - 5 + 2)

    def test_multiple_gut_checks_do_not_reuse_will_in_preview(self):
        sim, runner = fixture(position=36)
        runner.update(energy=0, will_available=True)
        for mile in (10, 18, 23):
            sim.marathon_gut[mile] = {'prepared_effort': 0, 'energy': 1}
        hypothetical = resolve_movement(36, 120, [0] * 26, 104)
        projected = sim.preview_gut_progress(runner, hypothetical)
        self.assertEqual(projected['to_space'], 72)
        self.assertEqual(projected['gut_preview']['mile'], 18)
        self.assertFalse(projected['gut_preview']['passed'])
        self.assertEqual(sim.resolve_milestones(runner, 36, 104), 18)
        self.assertEqual(runner['gut_cleared'], [10])
        self.assertFalse(runner['will_available'])


if __name__ == '__main__':
    unittest.main()
