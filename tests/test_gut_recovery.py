"""Deterministic Marathon Gut checkpoint and recovery boundaries."""
import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim, make_condition, prepared_gut_check, set_suppression

ROOT = Path(__file__).resolve().parents[1]
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(players=1, effort=10, energy=2):
    cfg = json.loads((ROOT / 'simulation/config.json').read_text())
    cfg['player_count'] = players
    sim = Sim(ROOT, cfg)
    sim.build_course()
    sim.runners = [sim.new_runner(n, 'Balanced', []) for n in range(players)]
    sim.course[9]['difficulty'] = 0
    sim.course[10]['difficulty'] = 0
    sim.marathon_gut[10] = {'prepared_effort': effort, 'energy': energy}
    sim.draw = []
    sim.discard = []
    return sim


def events(sim, name):
    return [e['payload'] for e in sim.events if e['type'] == name]


class GutRecovery(unittest.TestCase):
    def test_counted_zones_failures_and_will(self):
        training = [{'card': card('TR-019')}]
        gear = [{'card': card('GE-018')}]
        baseline = prepared_gut_check([card('FU-001')], training, gear, 1, 20, 2)
        self.assertEqual(baseline['prepared_effort'], 3 + 9 + 6 + 3 + 2)
        self.assertEqual(baseline['failure_type'], 'energy_only')
        self.assertEqual(prepared_gut_check([], [], [], 0, 1, 2)['failure_type'], 'both')
        self.assertEqual(prepared_gut_check([card('TR-001')], [], [], 2, 10, 2)['failure_type'], 'effort_only')
        saved = prepared_gut_check([card('FU-001')], training, gear, 1, 20, 2, True)
        self.assertTrue(saved['passed'])
        self.assertEqual(saved['energy_shortfall'], 1)
        self.assertEqual(saved['energy'], 1)
        self.assertFalse(prepared_gut_check([], [], [], 1, 20, 2, True)['passed'])

    def test_crossing_stops_and_recovery_deadline(self):
        sim = fixture(effort=30, energy=2)
        runner = sim.runners[0]
        runner['quarter_mile_space'] = 39
        runner['hand'] = [card('TR-001')]
        sim.start_round({'P1': 'Easy'})
        result = sim.turn(runner, {'movement_cards': ['TR-001']})
        self.assertEqual(result['to_space'], 40)
        self.assertGreater(result['gut_movement_lost_quarters'], 0)
        self.assertEqual(runner['energy'], 13)
        self.assertEqual(runner['gut_stall']['recovery_turns_used'], 0)
        self.assertEqual(runner['gut_stall']['failure_type'], 'effort_only')
        self.assertFalse(events(sim, 'DNF'))
        for index in range(4):
            sim.end_round()
            sim.start_round({'P1': 'Easy'})
            sim.turn(runner, {'movement_cards': []})
            self.assertEqual(runner['gut_stall']['recovery_turns_used'], index + 1)
            self.assertEqual(runner['dnf'], index == 3)
        self.assertEqual(runner['dnf_reason'], 'failed_gut_check')
        self.assertEqual(len(events(sim, 'GUT_RECOVERY_END')), 4)
        self.assertEqual(len(events(sim, 'MILE_CROSS')), 1)

    def test_pass_cleared_and_remaining_movement(self):
        sim = fixture(effort=3, energy=2)
        runner = sim.runners[0]
        runner['quarter_mile_space'] = 39
        runner['hand'] = [card('TR-001'), card('FU-001')]
        sim.start_round({'P1': 'Easy'})
        result = sim.turn(runner, {'movement_cards': ['TR-001']})
        self.assertGreater(result['to_space'], 40)
        self.assertEqual(runner['gut_cleared'], [10])
        self.assertIsNone(runner['gut_stall'])
        sim.resolve_milestones(runner, 39, 40)
        self.assertEqual(len([e for e in events(sim, 'MILESTONE') if e['kind'] == 'Gut Check']), 1)

    def test_fuel_post_use_and_nausea(self):
        sim = fixture(effort=7, energy=2)
        runner = sim.runners[0]
        runner['energy'] = 0
        runner['hand'] = [card('TR-001'), card('FU-001')]
        projected = sim.preview_preparation(runner, {'action': 'fuel', 'card_id': 'FU-001', 'choice': 'energy'})
        self.assertEqual(sim.gut_state(projected, 10)['prepared_effort'], 7)
        self.assertTrue(sim.gut_state(projected, 10)['passed'])
        sim.marathon_gut[10]['prepared_effort'] = 8
        self.assertFalse(sim.gut_state(projected, 10)['passed'])
        runner['active_conditions'] = [make_condition(card('CO-012'))]
        self.assertFalse(sim.legal_treat_prepare(runner, {'action': 'fuel', 'card_id': 'FU-001', 'choice': 'energy'}))

    def test_first_recovery_exchange_is_one_card_only(self):
        sim = fixture(effort=35, energy=2)
        runner = sim.runners[0]
        runner['hand'] = [card(cid) for cid in ('FU-001', 'FU-002', 'FU-003', 'FU-004', 'FU-005', 'FU-006')]
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0, 'recovery_turns_allowed': 4,
              'failure_type': 'effort_only', 'prepared_effort': 20, 'energy': 5,
              'exchange_used': False, 'assistance_used': False, 'fuel_used': False,
              'will_used': False, 'arrival_round': 1, 'arrival_turn': 1}
        sim.draw = [card('EV-023')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'gut_exchange': 'FU-001', 'movement_cards': []})
        self.assertEqual(len(events(sim, 'GUT_EXCHANGE')), 1)
        self.assertTrue((runner['gut_stall'] or runner['gut_history'][-1])['exchange_used'])
        with self.assertRaises(ValueError):
            sim.gut_exchange(runner, 'FU-002')

    def test_recovery_pass_resumes_movement_and_will_exact(self):
        sim = fixture(effort=7, energy=2)
        runner = sim.runners[0]
        runner['quarter_mile_space'] = 40
        runner['energy'] = 1
        runner['hand'] = [card('TR-001'), card('FU-001')]
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0, 'recovery_turns_allowed': 4,
              'failure_type': 'energy_only', 'prepared_effort': 7, 'energy': 1,
              'exchange_used': False, 'assistance_used': False, 'fuel_used': False,
              'will_used': False, 'arrival_round': 1, 'arrival_turn': 1}
        sim.start_round({'P1': 'Easy'})
        result = sim.turn(runner, {'gut_treat_prepare': None, 'movement_cards': ['FU-001']})
        self.assertIsNone(runner['gut_stall'])
        self.assertFalse(runner['will_available'])
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 1)
        self.assertEqual(events(sim, 'WILL_USE')[0]['stored_energy_after'], 1)
        self.assertGreater(result['quarter_miles'], 0)

    def test_preview_live_parity_for_consumed_cards_slots_fuel_and_pace(self):
        shapes = [
            ('one', ['TR-001'], ['EV-023'], None, None, 'Easy', None),
            ('two', ['TR-001', 'FU-001'], ['EV-023'], None, None, 'Easy', None),
            ('hand_slot', ['TR-001'], ['EV-023'], 'TR-019', None, 'Easy', None),
            ('slot_sacrifice', ['TR-019'], ['EV-023'], 'TR-019', None, 'Easy', None),
            ('fuel_before', ['TR-001'], ['EV-023', 'FU-001'], None, None, 'Easy', 'FU-001'),
            ('pace', ['TR-001'], ['EV-023'], None, None, 'Push', None),
            ('specialist', ['TR-001'], ['EV-023'], 'TR-019', 'GE-018', 'Easy', None),
            ('attachment', ['TR-001'], ['EV-023'], None, 'GE-003', 'Easy', None),
        ]
        for name, played_ids, kept_ids, training_id, gear_id, pace, fuel_id in shapes:
            with self.subTest(name=name):
                sim = fixture(effort=20, energy=2)
                runner = sim.runners[0]
                runner['quarter_mile_space'] = 39
                runner['energy'] = 8
                runner['hand'] = [card(cid) for cid in kept_ids + played_ids
                                  if cid != training_id or name != 'slot_sacrifice']
                if training_id:
                    runner['active_training'] = [{'card': card(training_id),
                         'remaining_turns': None, 'installed_turn': -2}]
                if gear_id == 'GE-018':
                    runner['equipped_gear'] = [{'card': card(gear_id),
                         'remaining_turns': None, 'installed_turn': -2}]
                elif gear_id:
                    condition = make_condition(card('CO-005'))
                    runner['active_conditions'] = [condition]
                    runner['attached_gear'] = [{'card': card(gear_id),
                         'condition_id': condition['id'], 'amount': 2, 'remaining_turns': None}]
                    set_suppression(condition, 2)
                sim.start_round({'P1': pace})
                plan = {'action': 'fuel', 'card_id': fuel_id, 'choice': 'energy'} if fuel_id else None
                prepared = sim.preview_preparation(runner, plan)
                movement_cards = [{**(next((c for c in prepared['hand'] if c['id'] == cid), None)
                          or next(i['card'] for i in prepared['active_training'] if i['card']['id'] == cid)),
                          'source': 'active_training' if name == 'slot_sacrifice' else 'hand',
                          'use_mode': 'MOVEMENT'} for cid in played_ids]
                liquidated = sim.preview_slot_sacrifice(prepared, movement_cards)
                consumed = {c['id'] for c in movement_cards if c['source'] == 'hand'}
                liquidated['hand'] = [c for c in liquidated['hand'] if c['id'] not in consumed]
                paid = sim.preview_payment(liquidated, sum(c['movement_energy_cost'] for c in movement_cards))
                self.assertIsNotNone(paid)
                preview = sim.preview_gut_progress(paid, sim.preview_movement(paid, movement_cards))
                predicted = preview['gut_preview']
                script = {'treat_prepare': plan, 'movement_cards': played_ids}
                if name == 'slot_sacrifice':
                    script['card_sources'] = ['active_training']
                sim.turn(runner, script)
                live = [e['gut_check'] for e in events(sim, 'MILESTONE')
                        if e['kind'] == 'Gut Check'][0]
                for key in ('hand_effort', 'training_effort', 'gear_effort', 'bonus_effort',
                            'prepared_effort', 'energy', 'passed', 'will_used'):
                    self.assertEqual(predicted[key], live[key], (name, key))
                self.assertEqual(preview['to_space'], runner['quarter_mile_space'])

    def test_all_recovery_windows_and_no_premature_generic_dnf(self):
        for mile, allowed in ((10, 4), (18, 3), (23, 2)):
            with self.subTest(mile=mile):
                sim = fixture(effort=35, energy=4)
                sim.marathon_gut[mile] = {'prepared_effort': 50, 'energy': 4}
                runner = sim.runners[0]
                runner['quarter_mile_space'] = mile * 4
                runner['energy'] = 0
                runner['will_available'] = False
                runner['gut_stall'] = {'mile': mile, 'recovery_turns_used': 0,
                    'recovery_turns_allowed': allowed, 'failure_type': 'both',
                    'prepared_effort': 0, 'energy': 0, 'exchange_used': False,
                    'assistance_used': False, 'fuel_used': False, 'will_used': False,
                    'arrival_round': 1, 'arrival_turn': 1}
                for turn in range(allowed):
                    sim.start_round({'P1': 'Easy'})
                    sim.turn(runner, {'movement_cards': []})
                    self.assertEqual(runner['dnf'], turn == allowed - 1)
                    self.assertFalse(events(sim, 'DNF_EVALUATION'))
                    sim.end_round()

    def test_gut_assistance_is_one_for_one_and_improves_actual_state(self):
        sim = fixture(players=2, effort=18, energy=0)
        runner, helper = sim.runners
        runner['hand'] = [card('FU-001')]
        helper['hand'] = [card('TR-001')]
        helper['energy'] = 0
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0,
             'recovery_turns_allowed': 4, 'failure_type': 'effort_only',
             'prepared_effort': 3, 'energy': 0, 'exchange_used': False,
             'assistance_used': False, 'fuel_used': False, 'will_used': False,
             'arrival_round': 1, 'arrival_turn': 1}
        # A normal slot means the received 7-Effort card completes the check.
        runner['active_training'] = [{'card': card('TR-019'),
                                     'remaining_turns': None, 'installed_turn': -2}]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        before_ids = {c['id'] for c in runner['hand'] + helper['hand']}
        self.assertTrue(sim.request_gut_assistance(runner))
        self.assertEqual({c['id'] for c in runner['hand'] + helper['hand']}, before_ids)
        self.assertEqual(len(runner['hand']), len(helper['hand']))
        self.assertTrue(events(sim, 'GUT_ASSISTANCE_SWAP')[0]['passed_after'])

    def test_live_fuel_rescue_and_dangerous_fuel_tradeoff(self):
        for threshold, should_pass in ((7, True), (8, False)):
            with self.subTest(threshold=threshold):
                sim = fixture(effort=threshold, energy=2)
                runner = sim.runners[0]
                runner['quarter_mile_space'] = 40
                runner['energy'] = 0
                runner['will_available'] = False
                runner['hand'] = [card('TR-001'), card('FU-001')]
                runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0,
                    'recovery_turns_allowed': 4, 'failure_type': 'energy_only',
                    'prepared_effort': 10, 'energy': 0, 'exchange_used': False,
                    'assistance_used': False, 'fuel_used': False, 'will_used': False,
                    'arrival_round': 1, 'arrival_turn': 1}
                sim.start_round({'P1': 'Easy'})
                sim.turn(runner, {'gut_treat_prepare': {'action': 'fuel',
                         'card_id': 'FU-001', 'choice': 'energy'}, 'movement_cards': []})
                self.assertEqual(runner['energy'], 2)
                self.assertEqual(events(sim, 'FUEL_USE')[0]['card'], 'FU-001')
                self.assertEqual(runner['gut_stall'] is None, should_pass)
                self.assertEqual(events(sim, 'GUT_EVALUATION')[-1]['prepared_effort'], 7)

    def test_assistance_rescues_in_live_recovery_turn(self):
        sim = fixture(players=2, effort=18, energy=0)
        runner, helper = sim.runners
        runner['quarter_mile_space'] = 40
        runner['hand'] = [card('FU-001')]
        helper['hand'] = [card('TR-001')]
        helper['energy'] = 0
        runner['active_training'] = [{'card': card('TR-019'),
                                     'remaining_turns': None, 'installed_turn': -2}]
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0,
             'recovery_turns_allowed': 4, 'failure_type': 'effort_only',
             'prepared_effort': 15, 'energy': 0, 'exchange_used': False,
             'assistance_used': False, 'fuel_used': False, 'will_used': False,
             'arrival_round': 1, 'arrival_turn': 1}
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(runner, {'gut_treat_prepare': None, 'movement_cards': []})
        self.assertIsNone(runner['gut_stall'])
        self.assertEqual(runner['hand'][0]['id'], 'TR-001')
        self.assertTrue(events(sim, 'GUT_ASSISTANCE_SWAP'))

    def test_half_marathon_retains_hand_only_failure_penalty(self):
        cfg = json.loads((ROOT / 'simulation/config.json').read_text())
        cfg['race_format'] = 'half'
        cfg['player_count'] = 1
        sim = Sim(ROOT, cfg)
        sim.build_course()
        runner = sim.new_runner(0, 'Balanced', [])
        sim.runners = [runner]
        runner['energy'] = 5
        sim.resolve_milestones(runner, 23, 24)
        self.assertEqual(runner['energy'], 3)
        self.assertIsNone(runner['gut_stall'])

    def test_ai_preserves_a_visible_viable_checkpoint_line(self):
        sim = fixture(effort=10, energy=2)
        runner = sim.runners[0]
        runner['quarter_mile_space'] = 39
        runner['hand'] = [card('TR-001'), card('EV-023'), card('FU-001')]
        runner['energy'] = 10
        sim.start_round({'P1': 'Easy'})
        selection = sim.choose_turn_plan(runner)
        self.assertFalse({'TR-001', 'EV-023'} <= set(selection['movement_cards']))
        sim.turn(runner, {'treat_prepare': selection['treat_prepare'],
                         'movement_cards': selection['movement_cards'],
                         'card_modes': selection['card_modes'],
                         'card_sources': selection['card_sources']})
        self.assertTrue([e for e in events(sim, 'MILESTONE') if e['kind'] == 'Gut Check'])
        self.assertFalse(runner['gut_stall'])


if __name__ == '__main__':
    unittest.main()
