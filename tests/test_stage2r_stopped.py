"""Deterministic three-Pace and Energy Exhaustion turn transitions."""

import copy
import json
import unittest
from pathlib import Path

from engine import simulate as m


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def fixture(energy=0, hand=('FU-001',), will=False, player_count=1):
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.round = 1
    sim.runners = [sim.new_runner(i, 'Balanced',
                   [copy.deepcopy(CARDS[c]) for c in hand]) for i in range(player_count)]
    sim.draw = []
    runner = sim.runners[0]
    runner.update(energy=energy, will_available=will, pace='Steady')
    return sim, runner


def events(sim, kind):
    return [e['payload'] for e in sim.events if e['type'] == kind]


class PaceAndStopped(unittest.TestCase):
    def test_paces_and_physical_cards(self):
        self.assertEqual(m.PACE_ORDER, ['Steady', 'Race', 'Push'])
        self.assertEqual([(CFG['pace'][p]['modifier'], abs(CFG['pace'][p]['energy_cost']))
                          for p in m.PACE_ORDER], [(1, 1), (2, 2), (3, 3)])
        sim, runner = fixture()
        self.assertEqual(sim.maximum_legal_pace({**runner, 'active_conditions': [
                         m.make_condition(copy.deepcopy(CARDS['CO-016']))]}), 'Steady')
        self.assertEqual(CARDS['TR-003']['effect_components'][0]['pace'], 'Steady')
        self.assertEqual(len(CARDS), 108)

    def test_original_zero_energy_has_no_free_fallback(self):
        sim, runner = fixture()
        self.assertIsNone(sim.preview_payment(runner))
        self.assertIsNone(sim.ordinary_movement_plan(runner))
        sim.turn(runner)
        self.assertEqual((runner['race_status'], runner['energy_recovery'], runner['pace']),
                         ('STOPPED', 'ordinary', None))
        self.assertEqual(len(events(sim, 'PACE_PAYMENT')), 0)
        self.assertEqual(runner['stats']['zero_movement_turns'], 1)

    def test_no_ordinary_treat_only_or_empty_card_turn(self):
        sim, runner = fixture(energy=5, hand=('FU-001', 'EV-029'))
        with self.assertRaisesRegex(ValueError, 'Movement-phase card required'):
            sim.turn(runner, {'treat_prepare': {'action': 'fuel', 'card_id': 'FU-001'},
                              'movement_cards': []})
        self.assertEqual([c['id'] for c in runner['hand']], ['FU-001', 'EV-029'])
        self.assertEqual(runner['energy'], 5)

    def test_fuel_and_conservation_are_real_zero_energy_rescues(self):
        sim, runner = fixture(hand=('FU-001', 'FU-002'))
        plan = sim.ordinary_movement_plan(runner)
        self.assertIsNotNone(plan)
        self.assertEqual(plan['treat_prepare']['action'], 'fuel')
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'RUNNING')
        sim2, r2 = fixture()
        r2['active_training'] = [{'card': copy.deepcopy(CARDS['TR-002']),
                                  'installed_turn': 0, 'remaining_turns': None}]
        # Pace Practice preserves one Steady Energy.
        r2['active_training'][0]['card'] = copy.deepcopy(next(c for c in CARDS.values()
                                                 if c['title'] == 'Pace Practice'))
        self.assertEqual(sim2.preview_payment(r2)['energy'], 0)
        sim2.turn(r2)
        self.assertEqual(events(sim2, 'PACE_PAYMENT')[0]['paid'], 0)

    def test_round_start_pace_and_drawn_cap_drop_pack_before_payment(self):
        sim, runner = fixture(energy=20, hand=('FU-001',), player_count=2)
        sim.round = 1
        sim.runners[1]['hand'] = [copy.deepcopy(CARDS['FU-001'])]
        sim.start_round({'P1': 'Push', 'P2': 'Push'})
        self.assertIsNotNone(runner['pack_state'])
        self.assertEqual(runner['round_start_pace'], 'Push')
        sim.draw = [copy.deepcopy(CARDS['FU-014']), copy.deepcopy(CARDS['CO-016'])]
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(runner['pace'], 'Steady')
        self.assertIsNone(runner['pack_state'])
        self.assertEqual(events(sim, 'PACE_PAYMENT')[-1]['preservation_sources'], [])
        self.assertEqual(events(sim, 'PACE_PAYMENT')[-1]['paid'], 1)
        self.assertEqual(runner['round_start_pace'], 'Push')
        self.assertTrue(any(e.get('reason') == 'pace_adjustment' for e in events(sim, 'PACK_EXIT')))

    def test_installed_gain_uses_actual_pace_and_preserves_energy_above_fifteen(self):
        sim, runner = fixture(energy=20)
        runner['pace'] = 'Push'
        runner['active_conditions'] = [m.make_condition(copy.deepcopy(CARDS['CO-016']))]
        runner['active_training'] = [{'card': copy.deepcopy(CARDS['TR-003']),
                                      'installed_turn': 0, 'remaining_turns': None}]
        expected = sim.preview_payment(runner)
        self.assertEqual((expected['pace'], expected['energy']), ('Steady', 20))
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual((runner['pace'], runner['energy']), ('Steady', 20))
        self.assertEqual(events(sim, 'ENERGY_CHANGE')[0]['to'], 21)

    def test_initial_stop_then_will_exact_shortfall_and_no_loop(self):
        sim, runner = fixture(will=True)
        sim.turn(runner)
        self.assertTrue(runner['will_available'])
        self.assertEqual(runner['race_status'], 'STOPPED')
        sim.round = 2
        sim.start_round()
        self.assertIsNone(runner['pace'])
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'RUNNING')
        self.assertEqual((runner['will_available'], runner['energy']), (False, 0))
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'],
                         events(sim, 'PACE_PAYMENT')[0]['final'])
        self.assertIsNone(runner['pack_state'])

    def test_stopping_exits_pack_and_restart_never_rejoins_midround(self):
        sim, runner = fixture(hand=('TR-001',), will=True)
        runner['pack_state'] = 'old-pack'
        runner['pack_members_snapshot'] = ['P1', 'P2']
        sim.turn(runner)
        self.assertEqual((runner['pace'], runner['pack_state']), (None, None))
        self.assertEqual(len(events(sim, 'PACK_EXIT')), 1)
        sim.round = 2
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'RUNNING')
        self.assertIsNone(runner['pack_state'])
        self.assertNotIn('Pack', events(sim, 'PACE_PAYMENT')[0]['preservation_sources'])

    def test_refusal_dnf_after_exactly_one_attempt(self):
        sim, runner = fixture(player_count=2)
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'STOPPED')
        sim.round = 2
        sim.turn(runner, {'assistance_accept': False})
        self.assertEqual((runner['race_status'], runner['dnf_reason']),
                         ('DNF', 'energy_exhaustion'))
        self.assertEqual(len(events(sim, 'ASSISTANCE_REQUEST')), 1)

    def test_useful_exchange_grants_only_one_final_turn(self):
        sim, runner = fixture(hand=('EV-001', 'TR-001'), player_count=2)
        helper = sim.runners[1]
        helper['hand'] = [copy.deepcopy(CARDS['FU-002'])]
        sim.turn(runner)
        sim.round = 2
        sim.turn(runner, {'assistance_accept': True})
        self.assertEqual((runner['race_status'], runner['energy_recovery'], runner['pace']),
                         ('STOPPED', 'assisted_final', None))
        self.assertEqual(len(events(sim, 'ASSISTANCE_SWAP')), 1)
        self.assertEqual(len(helper['hand']), 1)
        sim.round = 3
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'RUNNING')
        self.assertEqual(len(events(sim, 'ASSISTANCE_REQUEST')), 1)

    def test_ai_helper_accepts_only_useful_competitive_exchange(self):
        sim, runner = fixture(hand=('EV-001', 'TR-001'), player_count=2)
        sim.runners[1]['hand'] = [copy.deepcopy(CARDS['FU-002'])]
        sim.turn(runner)
        sim.round = 2
        sim.turn(runner)
        selected = events(sim, 'ASSISTANCE_SWAP_EVALUATE')[0]['selected']
        self.assertTrue(selected['rescue'])
        self.assertLessEqual(selected['helper_competitive_loss'], 0)
        self.assertEqual(runner['energy_recovery'], 'assisted_final')

    def test_gut_recovery_does_not_consume_energy_stop_cycle(self):
        sim, runner = fixture()
        runner['quarter_mile_space'] = 40
        runner['distance_completed'] = 10
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0,
                               'recovery_turns_allowed': 4, 'failure_type': 'energy_only',
                               'prepared_effort': 3, 'energy': 0, 'exchange_used': False,
                               'assistance_used': False, 'fuel_used': False,
                               'will_used': False, 'arrival_round': 1, 'arrival_turn': 1}
        sim.turn(runner)
        self.assertEqual(runner['gut_stall']['recovery_turns_used'], 1)
        self.assertEqual((runner['race_status'], runner['energy_recovery']), ('RUNNING', None))
        self.assertFalse(events(sim, 'ENERGY_STOP'))

    def test_failed_final_assisted_turn_dnf_without_new_cycle(self):
        sim, runner = fixture(hand=('EV-001', 'TR-001'), player_count=2)
        sim.runners[1]['hand'] = [copy.deepcopy(CARDS['FU-002'])]
        sim.turn(runner)
        sim.round = 2
        sim.turn(runner, {'assistance_accept': True})
        self.assertEqual(runner['energy_recovery'], 'assisted_final')
        sim.round = 3
        sim.draw = [copy.deepcopy(CARDS['EV-021']), copy.deepcopy(CARDS['CO-012'])]
        sim.turn(runner)
        self.assertEqual((runner['race_status'], runner['dnf_reason']),
                         ('DNF', 'energy_exhaustion'))
        self.assertEqual(len(events(sim, 'ASSISTANCE_REQUEST')), 1)


if __name__ == '__main__':
    unittest.main()
