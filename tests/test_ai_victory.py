"""Victory-first complete-turn decisions; no full marathon is executed."""
import copy
import json
import statistics
import unittest
from pathlib import Path
from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
CFG = json.loads((ROOT / 'simulation/config.json').read_text())


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(profile='Balanced', difficulty=5, elevation='Flat'):
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.course[0].update({'difficulty': difficulty, 'elevation': elevation})
    runner = sim.new_runner(0, profile, [])
    sim.runners = [runner]
    sim.draw = []
    sim.discard = []
    runner['pace'] = 'Easy'
    sim.round = 1
    return sim, runner


class VictoryDirective(unittest.TestCase):
    def test_run03_style_effort_eight_setup_zero_vs_two_card_movement(self):
        sim, runner = fixture()
        runner['hand'] = [card('TR-008'), card('FU-014')]
        setup = {'card_id': 'TR-008', 'action': 'training', 'replace_id': None}
        prepared = sim.preview_preparation(runner, setup)
        self.assertEqual(sim.preview_movement(prepared, [prepared['hand'][0]])['quarter_miles'], 0)
        before, rng_state, event_count = copy.deepcopy(runner), sim.rng.getstate(), len(sim.events)
        plan = sim.choose_turn_plan(runner)
        self.assertEqual(plan, sim.choose_turn_plan(runner))
        self.assertEqual((runner, sim.rng.getstate(), len(sim.events)),
                         (before, rng_state, event_count))
        self.assertIsNone(plan['treat_prepare'])
        self.assertEqual(set(plan['movement_cards']), {'TR-008', 'FU-014'})
        self.assertGreater(plan['movement_quarters'], 0)
        sim.turn(runner)
        self.assertFalse(runner['active_training'])
        self.assertGreater(runner['quarter_mile_space'], 0)

    def test_positive_movement_beats_zero_setup_in_every_profile(self):
        for profile in ('Balanced', 'Aggressive', 'Energy Conservative', 'Course Planner',
                        'Pack Runner', 'Opportunist', 'Front Runner', 'Adaptive'):
            with self.subTest(profile=profile):
                sim, runner = fixture(profile)
                runner['hand'] = [card('TR-008'), card('FU-014')]
                choice = sim.choose_turn_plan(runner)
                self.assertIsNone(choice['treat_prepare'])
                self.assertGreater(choice['movement_quarters'], 0)

    def test_low_value_training_and_gear_swaps_lose_to_two_card_progress(self):
        for setup_id, action, old_id, zone in (
                ('TR-008', 'training', 'TR-019', 'active_training'),
                ('GE-016', 'gear', 'GE-010', 'equipped_gear')):
            with self.subTest(action=action):
                sim, runner = fixture()
                runner[zone] = [{'card': card(old_id), 'remaining_turns': None},
                                {'card': card('TR-003' if action == 'training' else 'GE-006'),
                                 'remaining_turns': None}]
                runner['hand'] = [card(setup_id), card('FU-014')]
                plan = sim.choose_turn_plan(runner)
                self.assertIsNone(plan['treat_prepare'])
                self.assertEqual(len(plan['movement_cards']), 2)
                self.assertIn({'card_id': setup_id, 'action': action, 'replace_id': old_id},
                              sim.treat_candidates(runner))

    def test_condition_treatment_may_win_at_equal_immediate_progress(self):
        sim, runner = fixture(difficulty=1)
        runner['pace'] = 'Race'
        runner['energy'] = 3
        runner['hand'] = [card('FU-019'), card('EV-023')]
        runner['active_conditions'] = [m.make_condition(card('CO-001'))]
        plan = sim.choose_turn_plan(runner)
        self.assertEqual(plan['treat_prepare'],
                         {'card_id': 'FU-019', 'action': 'fuel', 'choice': 'remedy'})
        self.assertIn({'card_id': 'FU-019', 'action': 'fuel', 'choice': 'remedy'},
                      sim.treat_candidates(runner))
        self.assertGreater(plan['movement_quarters'], 0)
        sim.turn(runner)
        self.assertIsNone(sim.condition_by_title(runner, 'Cramp'))
        self.assertGreater(runner['quarter_mile_space'], 0)

    def test_setup_rejected_when_second_movement_card_reaches_cap(self):
        sim, runner = fixture(difficulty=1, elevation='Incline')
        for segment in sim.course:
            segment['difficulty'] = 1
            segment['elevation'] = 'Incline'
        runner['pace'] = 'Push'
        runner['hand'] = [card('TR-009'), card('EV-023')]
        runner['equipped_gear'] = [{'card': card('GE-011'), 'remaining_turns': 3}]
        plan = sim.choose_turn_plan(runner)
        self.assertIsNone(plan['treat_prepare'])
        self.assertEqual(plan['movement_cards'], ['TR-009', 'EV-023'])
        self.assertEqual(plan['movement_quarters'], 8)
        sim.turn(runner)
        self.assertNotIn('Hill Repeats', sim.installed_titles(runner, 'training'))
        self.assertEqual(runner['quarter_mile_space'], 8)

    def test_late_setup_discount_favors_immediate_finish(self):
        sim, runner = fixture(difficulty=1, elevation='Incline')
        for segment in sim.course:
            segment['difficulty'] = 1
            segment['elevation'] = 'Incline'
        runner['quarter_mile_space'] = len(sim.course) * 4 - 2
        runner['pace'] = 'Push'
        runner['hand'] = [card('TR-009'), card('EV-023')]
        runner['equipped_gear'] = [{'card': card('GE-011'), 'remaining_turns': 3}]
        plan = sim.choose_turn_plan(runner)
        self.assertIsNone(plan['treat_prepare'])
        self.assertGreater(plan['movement_quarters'], 0)

    def test_profiles_differ_without_overriding_progress(self):
        a, ra = fixture('Aggressive', difficulty=1)
        b, rb = fixture('Energy Conservative', difficulty=1)
        for runner in (ra, rb):
            runner['hand'] = [card('FU-018'), card('TR-019')]
            runner['energy'] = 2
        options_a, pace_a = a.choose_pace(ra)
        options_b, pace_b = b.choose_pace(rb)
        self.assertIn(pace_a, m.PACE_ORDER)
        self.assertIn(pace_b, m.PACE_ORDER)
        self.assertNotEqual([x['score'] for x in options_a], [x['score'] for x in options_b])
        self.assertGreater(a.choose_turn_plan(ra)['movement_quarters'], 0)
        self.assertGreater(b.choose_turn_plan(rb)['movement_quarters'], 0)

    def test_relative_position_and_finish_discount(self):
        sim, runner = fixture(difficulty=5)
        opponent = sim.new_runner(1, 'Balanced', [])
        sim.runners.append(opponent)
        runner['hand'] = [card('TR-008'), card('FU-014')]
        baseline = sim.choose_turn_plan(runner)['score']
        opponent['quarter_mile_space'] = 28
        trailing = sim.choose_turn_plan(runner)['score']
        self.assertGreater(trailing, baseline)
        runner['quarter_mile_space'] = len(sim.course) * 4 - 2
        runner['hand'] = [card('TR-008'), card('FU-014')]
        near = sim.choose_turn_plan(runner)
        self.assertIsNone(near['treat_prepare'])
        self.assertGreater(near['movement_quarters'], 0)

    def test_legality_filter_precedes_scoring(self):
        sim, runner = fixture()
        runner['hand'] = [card('FU-019'), card('TR-001')]
        runner['active_conditions'] = [m.make_condition(card('CO-012')), m.make_condition(card('CO-001'))]
        plan = sim.choose_turn_plan(runner)
        self.assertNotEqual(plan['treat_prepare'], {'card_id': 'FU-019', 'action': 'fuel', 'choice': 'remedy'})
        self.assertTrue(sim.legal_treat_prepare(runner, plan['treat_prepare']))
        self.assertGreater(plan['movement_quarters'], 0)

    def test_other_target_uses_visible_race_position_and_lock(self):
        sim, source = fixture()
        middle = sim.new_runner(1, 'Balanced', [])
        leader = sim.new_runner(2, 'Balanced', [])
        sim.runners.extend([middle, leader])
        middle['quarter_mile_space'] = 8
        leader['quarter_mile_space'] = 16
        self.assertEqual(sim.event_target(source)['player_id'], 'P3')
        leader['staged_events'] = [{'card': card('EV-009'), 'target': 'P3',
                                    'source': 'P2', 'activate_round': 2}]
        self.assertEqual(sim.event_target(source)['player_id'], 'P2')

    def test_pre_race_exchange_keeps_cards_above_public_expected_value(self):
        cfg = copy.deepcopy(CFG)
        cfg['seed'] = 42
        sim = m.Sim(ROOT, cfg)
        sim.setup()  # Deal and exchange only; no race turn or round.
        expected = statistics.mean(sim.prevalue(c) for c in sim.cards if c['family'] != 'Condition')
        exchanges = [e for e in sim.events if e['type'] == 'DECK_EXCHANGE']
        self.assertTrue(exchanges)
        self.assertTrue(all(sim.prevalue(sim.card(e['payload']['surrendered'])) < expected
                            for e in exchanges))
        self.assertTrue(all(r['exchanges_used'] <= 3 for r in sim.runners))

    def test_course_event_preview_respects_new_rain_at_boundary(self):
        sim, runner = fixture(difficulty=1)
        sim.course[1]['difficulty'] = 1
        runner['hand'] = [card('EV-005'), card('FU-018')]
        paid = sim.preview_payment(runner)
        paid['energy'] -= m.movement_energy_cost(runner['hand'][1])
        predicted = sim.preview_movement(paid, [{**runner['hand'][0], 'use_mode': 'EFFECT'},
                                                {**runner['hand'][1], 'use_mode': 'MOVEMENT'}])
        sim.turn(runner, {'treat_prepare': None,
                          'movement_cards': ['EV-005', 'FU-018'],
                          'card_modes': ['EFFECT', 'MOVEMENT']})
        self.assertEqual(predicted['to_space'], runner['quarter_mile_space'])
        self.assertEqual(len(sim.course_events), 1)


if __name__ == '__main__':
    unittest.main()
