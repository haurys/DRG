"""Stage 1 payment and uncapped stored-Energy regression fixtures."""

import copy
import itertools
import json
import unittest
from pathlib import Path

from engine import simulate as m


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(energy=15, pace='Race', hand=('TR-001',)):
    sim = m.Sim(ROOT, copy.deepcopy(CONFIG))
    sim.build_course()
    runner = sim.new_runner(0, 'Balanced', [card(cid) for cid in hand])
    sim.runners = [runner]
    sim.draw = []
    sim.round = 1
    runner.update(energy=energy, pace=pace)
    return sim, runner


def events(sim, kind):
    return [e['payload'] for e in sim.events if e['type'] == kind]


class StageOnePayment(unittest.TestCase):
    def test_newly_drawn_condition_changes_ai_preview_and_live_pace(self):
        sim, runner = fixture(20, 'Push')
        # Draw pops the Condition first, then the normal replacement card.
        sim.draw = [card('FU-014'), card('CO-016')]
        sim.turn(runner)
        decision = events(sim, 'AI_TURN_RATIONALE')[0]['selected_plan']
        paid = events(sim, 'PACE_PAYMENT')[0]
        self.assertEqual((decision['selected_pace'], paid['selected_pace']), ('Easy', 'Easy'))
        self.assertEqual(decision['projected_energy_cost'],
                         paid['paid'] + sum(e['paid'] for e in events(sim, 'MOVEMENT_ENERGY_PAYMENT')))
        self.assertEqual(decision['projected_energy_after_action'], runner['energy'])
        self.assertGreater(decision['projected_energy_after_action'], 15)
        self.assertEqual(decision['projected_movement_quarters'], events(sim, 'MOVE')[0]['quarter_miles'])

    def test_each_drawn_pace_limit_is_priced_before_ai_scoring(self):
        for condition_id, expected_pace in [('CO-001', 'Race'), ('CO-015', 'Steady'),
                                            ('CO-016', 'Easy')]:
            with self.subTest(condition=condition_id):
                sim, runner = fixture(20, 'Push')
                sim.draw = [card('FU-014'), card(condition_id)]
                sim.turn(runner)
                selected = events(sim, 'AI_TURN_RATIONALE')[0]['selected_plan']
                self.assertEqual(selected['selected_pace'], expected_pace)
                self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['selected_pace'], expected_pace)
                self.assertEqual(selected['projected_energy_after_action'], runner['energy'])
                self.assertEqual(selected['projected_movement_quarters'],
                                 events(sim, 'MOVE')[0]['quarter_miles'])

    def test_treatment_precedes_legal_pace_and_payment(self):
        sim, runner = fixture(6, 'Push', ('FU-019', 'TR-001'))
        runner['active_conditions'] = [m.make_condition(card('CO-001'))]
        runner['race_turn_number'] = 1  # Preview the same turn that live execution will run.
        plan = {'action': 'fuel', 'card_id': 'FU-019', 'choice': 'remedy'}
        prepared = sim.preview_preparation(runner, plan)
        self.assertEqual(prepared['pace'], 'Push')
        expected = sim.preview_payment(prepared, 2)
        self.assertEqual((expected['pace'], expected['energy']), ('Push', 2))
        runner['race_turn_number'] = 0
        sim.turn(runner, {'treat_prepare': plan, 'movement_cards': ['TR-001']})
        self.assertEqual((runner['pace'], runner['energy']), ('Push', expected['energy']))
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['paid'], 2)

    def test_pack_and_training_preservation_stack_to_zero(self):
        sim, runner = fixture(18, 'Race', ('FU-001',))
        runner['pack_state'] = 'fixture-pack'
        runner['active_training'] = [{'card': card('TR-001'), 'remaining_turns': None,
                                      'installed_turn': 0}]
        preview = sim.preview_payment(runner, 0)
        self.assertEqual(preview['energy'], 18)
        self.assertEqual(sim.pace_cost(runner, 'Race')['preservation_sources'], ['Pack', 'Long Run'])
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['paid'], 0)
        self.assertEqual(runner['energy'], 18)

    def test_insufficient_energy_fallback_and_no_future_borrowing(self):
        sim, runner = fixture(0, 'Push', ('TR-001',))
        runner['will_available'] = False
        self.assertIsNone(sim.preview_payment(runner, 2))
        runner['energy'] = 2
        runner['will_available'] = False
        self.assertIsNone(sim.preview_payment(runner, 3))
        runner['energy'] = 1
        actual = sim.preview_payment(runner, 0)
        self.assertEqual((actual['pace'], actual['energy']), ('Race', 0))
        later, other = fixture(0, 'Race', ('TR-001', 'EV-021'))
        other['will_available'] = False
        # This Event gains Energy after Movement; it cannot fund the payment.
        with self.assertRaisesRegex(ValueError, 'Movement Energy unavailable'):
            later.turn(other, {'movement_cards': ['TR-001', 'EV-021'],
                               'card_modes': ['MOVEMENT', 'EFFECT']})

    def test_will_covers_exact_combined_shortfall_once(self):
        sim, runner = fixture(1, 'Push', ('TR-001',))
        expected = sim.preview_payment(runner, 2)
        self.assertEqual((expected['energy'], expected['will_available']), (0, False))
        sim.turn(runner, {'movement_cards': ['TR-001']})
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 3)
        self.assertEqual((runner['energy'], runner['will_available']), (0, False))

    def test_fuel_gain_over_fifteen_matches_preview(self):
        sim, runner = fixture(20, 'Easy', ('FU-001', 'TR-001'))
        plan = {'action': 'fuel', 'card_id': 'FU-001'}
        prepared = sim.preview_preparation(runner, plan)
        self.assertEqual(prepared['energy'], 22)
        expected = sim.preview_payment(prepared, 2)
        sim.turn(runner, {'treat_prepare': plan, 'movement_cards': ['TR-001']})
        self.assertEqual((runner['energy'], expected['energy']), (20, 20))
        self.assertEqual(events(sim, 'FUEL_USE')[0]['energy_after'], 22)

    def test_installed_gain_over_fifteen_matches_payment(self):
        sim, runner = fixture(20, 'Race', ('FU-001',))
        runner['equipped_gear'] = [{'card': card('GE-016'), 'remaining_turns': 2,
                                    'installed_turn': 0}]
        expected = sim.preview_payment(runner, 0)
        self.assertEqual(expected['energy'], 20)  # +1 installed, -1 Pace
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(events(sim, 'ENERGY_CHANGE')[0]['to'], 21)
        self.assertEqual(runner['energy'], expected['energy'])

    def test_pace_limited_installed_gain_uses_paid_pace(self):
        sim, runner = fixture(20, 'Push', ('FU-001',))
        runner['active_conditions'] = [m.make_condition(card('CO-016'))]
        runner['active_training'] = [{'card': card('TR-003'), 'remaining_turns': None,
                                      'installed_turn': 0}]
        expected = sim.preview_payment(runner, 0)
        self.assertEqual((expected['pace'], expected['energy']), ('Easy', 21))
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(events(sim, 'ENERGY_CHANGE')[0]['to'], 21)
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['selected_pace'], 'Easy')
        self.assertEqual(runner['energy'], expected['energy'])

    def test_general_gain_and_loss_have_no_upper_cap_and_a_zero_floor(self):
        sim, runner = fixture(20)
        sim.apply_energy(runner, 4, 'Event fixture')
        self.assertEqual(runner['energy'], 24)
        sim.apply_energy(runner, -99, 'Condition fixture')
        self.assertEqual(runner['energy'], 0)

    def test_water_gut_preview_retains_energy_above_fifteen(self):
        sim, runner = fixture(16, 'Easy')
        runner['quarter_mile_space'] = 31  # Water at 8, then Gut at 10.
        runner['equipped_gear'] = [{'card': card('GE-012'), 'remaining_turns': None,
                                    'installed_turn': 0}]
        runner['hand'] = [card('TR-001'), card('TR-002'), card('TR-003'), card('TR-004')]
        resolved = {'to_space': 40, 'quarter_miles': 9, 'positive_finish_movement': False,
                    'milestone_energy_gain': 1}
        result = sim.preview_gut_progress(runner, resolved)
        self.assertEqual(result['gut_preview']['energy'], 17)

    def test_continuation_recognizes_installed_gain_above_fifteen(self):
        sim, runner = fixture(16, 'Easy', ())
        runner['equipped_gear'] = [{'card': card('GE-016'), 'remaining_turns': 2,
                                    'installed_turn': 0}]
        path = sim.continuation_paths(runner, future_replenish=False)
        self.assertEqual((path['viable'], path['kind']), (True, 'installed_energy'))

    def test_zero_energy_can_continue_with_a_legal_zero_cost_move(self):
        sim, runner = fixture(0, 'Easy', ('FU-001',))
        runner['will_available'] = False
        self.assertTrue(sim.continuation_paths(runner)['viable'])
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(runner['energy'], 0)
        self.assertFalse(runner.get('dnf'))

    def test_preview_matches_live_payment_across_bounded_states(self):
        sim, base = fixture()
        for pace, condition, energy, will, pack, installed, card_cost in itertools.product(
                m.PACE_ORDER, (None, 'CO-001', 'CO-015', 'CO-016'),
                (0, 1, 2, 4, 16, 20), (False, True), (False, True), (False, True),
                (0, 1, 2, 3)):
            live = copy.deepcopy(base)
            live.update(pace=pace, energy=energy, will_available=will,
                        pack_state='fixture-pack' if pack else None,
                        active_conditions=[m.make_condition(card(condition))] if condition else [],
                        active_training=[{'card': card('TR-003'), 'remaining_turns': None,
                                          'installed_turn': 0}] if installed else [])
            expected = sim.preview_payment(live, card_cost)
            live['pace'] = sim.payable_pace(live)
            sim.apply_installed_energy(live)
            case = (pace, condition, energy, will, pack, installed, card_cost)
            if expected is None:
                with self.assertRaisesRegex(ValueError, 'Movement Energy unavailable', msg=case):
                    sim.pay_pace(live, card_cost)
                continue
            _, used_will = sim.pay_pace(live, card_cost)
            if card_cost > live['energy']:
                self.assertTrue(used_will, case)
            live['energy'] -= min(live['energy'], card_cost)
            self.assertEqual((live['pace'], live['energy'], live['will_available']),
                             (expected['pace'], expected['energy'], expected['will_available']), case)


if __name__ == '__main__':
    unittest.main()
