"""Bounded regression fixtures for the interrupted Run 06 and Victory Directive."""

import copy
import json
import unittest
from pathlib import Path

from audit.run_output import final_state_json
from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
PLAN_KEYS = {'treat_prepare', 'movement_cards', 'card_modes', 'movement_energy_cost',
             'movement_quarters', 'score', 'expected_turns_remaining'}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(energy=15, hand=(), pace='Easy', position=0, profile='Balanced'):
    cfg = copy.deepcopy(CFG)
    cfg['seed'] = 20260930
    sim = m.Sim(ROOT, cfg)
    sim.build_course()  # only Course generation; never run a marathon
    runner = sim.new_runner(0, profile, [card(cid) for cid in hand])
    sim.runners = [runner]
    sim.draw = []
    sim.round = 1
    runner.update(energy=energy, pace=pace, quarter_mile_space=position,
                  distance_completed=position / 4)
    return sim, runner


def p4_fixture():
    """Compact state copied from Run 06 snapshot EV-002927, round 18 P4."""
    sim, runner = fixture(energy=0, position=38, hand=(
        'GE-008', 'FU-005', 'FU-016', 'FU-017', 'FU-004', 'FU-007', 'GE-018'),
        profile='Course Planner')
    sim.round = 18
    runner['race_turn_number'] = 17
    runner['active_conditions'] = [m.make_condition(card(cid)) for cid in
                                   ('CO-012', 'CO-011', 'CO-004', 'CO-001', 'CO-013')]
    runner['active_conditions'][3]['current_severity'] = 2
    m.update_effective_severity(runner['active_conditions'][3])
    runner['active_training'] = [{'card': card(cid), 'remaining_turns': None}
                                 for cid in ('TR-011', 'TR-014')]
    runner['equipped_gear'] = [{'card': card('GE-002'), 'remaining_turns': None}]
    runner['will_available'] = True
    return sim, runner


def scored(sim, runner, quarters, energy_after, finish=False):
    position = runner['quarter_mile_space'] + quarters
    result = {'quarter_miles': quarters, 'to_space': position,
              'positive_finish_movement': finish, 'staged_energy_cost': 0,
              'milestone_energy_gain': 0}
    return sim.plan_score(runner, runner, {**runner, 'energy': energy_after},
                          None, [], result)[0]


class Run06Repair(unittest.TestCase):
    def test_p4_will_makes_movement_candidate_legal(self):
        sim, runner = p4_fixture()
        self.assertEqual(sim.maximum_legal_pace(runner), 'Race')
        preparations = sim.treat_candidates(runner)
        self.assertEqual({p['card_id'] for p in preparations if p}, {'GE-008', 'GE-018'})
        # Gear remains an option, but Will also makes Movement affordable.
        self.assertFalse(sim.fuel_available(runner))
        self.assertTrue(all(m.movement_energy_cost(c) > 0 for c in runner['hand']))
        self.assertIsNone(runner['pack_state'])
        self.assertTrue(runner['will_available'])
        capture = {}
        plan = sim.choose_turn_plan(runner, capture)
        self.assertTrue(capture['candidates'])
        self.assertEqual(set(plan), PLAN_KEYS)
        self.assertTrue(plan['movement_cards'])
        self.assertEqual(plan['card_modes'], ['MOVEMENT'] * len(plan['movement_cards']))
        self.assertGreater(plan['movement_energy_cost'], 0)
        before = copy.deepcopy(runner)
        sim.turn(runner)
        self.assertGreater(runner['quarter_mile_space'], before['quarter_mile_space'])
        self.assertEqual(runner['energy'], 0)
        self.assertFalse(runner['will_available'])
        self.assertEqual([e['type'] for e in sim.events if e['type'] == 'TURN_END'], ['TURN_END'])
        self.assertEqual([e['payload']['card_modes'] for e in sim.events
                          if e['type'] == 'AI_TURN_PLAN'], [plan['card_modes']])
        self.assertEqual(sum(e['payload']['covered_by_will'] for e in sim.events
                             if e['type'] == 'MOVEMENT_ENERGY_PAYMENT'), plan['movement_energy_cost'])

    def test_true_fallback_when_will_spent(self):
        sim, runner = p4_fixture()
        runner['will_available'] = False
        capture = {}
        plan = sim.choose_turn_plan(runner, capture)
        self.assertEqual(capture['candidates'], [])
        self.assertEqual(set(plan), PLAN_KEYS)
        self.assertEqual((plan['movement_cards'], plan['card_modes'], plan['movement_energy_cost']),
                         ([], [], 0))
        sim.turn(runner)
        self.assertEqual(runner['energy'], 0)
        self.assertEqual(runner['quarter_mile_space'], 38)
        self.assertTrue(any(e['type'] == 'TURN_END' for e in sim.events))

    def test_schema_and_legal_candidates_survive_filtering(self):
        for energy, hand, conditions in (
                (0, ('FU-001',), ()),
                (0, ('FU-001',), ('CO-012',)),
                (1, ('TR-001', 'EV-029'), ()),
                (15, ('TR-001', 'EV-029'), ())):
            with self.subTest(energy=energy, hand=hand, conditions=conditions):
                sim, runner = fixture(energy, hand)
                runner['active_conditions'] = [m.make_condition(card(cid)) for cid in conditions]
                capture = {}
                plan = sim.choose_turn_plan(runner, capture)
                self.assertEqual(set(plan), PLAN_KEYS)
                self.assertEqual(len(plan['movement_cards']), len(plan['card_modes']))
                if capture['candidates']:
                    self.assertIn(plan, capture['candidates'])
                    self.assertGreater(plan['score'], -1000)
                else:
                    self.assertEqual(plan['movement_cards'], [])
        sim, runner = fixture(0, ('FU-001',))
        self.assertTrue(any(p and p['action'] == 'fuel' for p in sim.treat_candidates(runner)))
        self.assertTrue(sim.choose_turn_plan(runner)['treat_prepare'])

    def test_fallback_and_low_energy_are_repeatable_without_race(self):
        def no_will():
            sim, runner = p4_fixture()
            runner['will_available'] = False
            return sim, runner
        for maker in (p4_fixture, no_will, lambda: fixture(0, ('FU-001', 'TR-001'))):
            outputs = []
            for _ in range(2):
                sim, runner = maker()
                plan = copy.deepcopy(sim.choose_turn_plan(runner))
                sim.turn(runner)
                outputs.append((plan, runner['quarter_mile_space'], runner['energy'],
                                [(e['type'], e['payload']) for e in sim.events if e['player_id']]))
            self.assertEqual(outputs[0], outputs[1])

    def test_audit_export_sorts_locked_ids_without_mutating_state(self):
        sim, runner = fixture(hand=('TR-001',))
        runner['locked_ids'] = {'TR-003', 'TR-001', 'TR-002'}
        before = copy.deepcopy(runner)
        a = final_state_json(sim)
        self.assertEqual(a, final_state_json(sim))
        self.assertEqual(json.loads(a)['runners'][0]['locked_ids'],
                         ['TR-001', 'TR-002', 'TR-003'])
        self.assertEqual(runner, before)

    def test_clear_speed_beats_energy_reserve_and_urgency_near_finish(self):
        sim, runner = fixture(position=16)
        self.assertGreater(scored(sim, runner, 5, 0), scored(sim, runner, 4, 8))
        near = len(sim.course) * 4 - 8
        runner['quarter_mile_space'] = near
        self.assertGreater(scored(sim, runner, 5, 0), scored(sim, runner, 4, 8))
        self.assertGreater(scored(sim, runner, 8, 0, finish=True),
                           scored(sim, runner, 7, 15))

    def test_zero_energy_finish_is_legal_and_equivalent_energy_is_secondary(self):
        outputs = []
        for _ in range(2):
            sim, runner = fixture(energy=2, hand=('TR-001',), position=103)
            plan = sim.choose_turn_plan(runner)
            self.assertEqual(plan['movement_cards'], ['TR-001'])
            sim.turn(runner)
            self.assertEqual(runner['energy'], 0)
            self.assertTrue(runner['finish_pending'])
            sim.end_round()
            self.assertEqual(runner['finish_order'], 1)
            outputs.append((plan, runner['quarter_mile_space'], runner['energy'],
                            [(e['type'], e['payload']) for e in sim.events if e['player_id']]))
        self.assertEqual(outputs[0], outputs[1])
        sim2, r2 = fixture(position=16)
        self.assertGreater(scored(sim2, r2, 4, 5), scored(sim2, r2, 4, 0))

    def test_fuel_requires_progress_benefit_and_setup_pays_opportunity_cost(self):
        sim, runner = fixture(0, ('FU-001', 'TR-001'))
        runner['will_available'] = False
        plan = sim.choose_turn_plan(runner)
        self.assertEqual(plan['treat_prepare']['action'], 'fuel')
        self.assertGreater(plan['movement_quarters'], 0)
        sim2, r2 = fixture(15, ('FU-001', 'TR-001'))
        self.assertIsNone(sim2.choose_turn_plan(r2)['treat_prepare'])
        sim3, r3 = fixture(15, ('TR-008', 'FU-014'))
        self.assertIsNone(sim3.choose_turn_plan(r3)['treat_prepare'])

    def test_pace_choice_is_speed_sensitive_not_easy_by_default(self):
        sim, runner = fixture(15, ('TR-019', 'FU-022'))
        options, pace = sim.choose_pace(runner)
        self.assertEqual(pace, max(options, key=lambda x: (x['score'],
                         -m.PACE_ORDER.index(x['pace'])))['pace'])
        self.assertNotEqual(pace, 'Easy')

    def test_run06_p1_round_one_aggressive_selection_unchanged(self):
        cfg = copy.deepcopy(CFG)
        cfg['seed'] = 20260930
        sim = m.Sim(ROOT, cfg)
        sim.setup()
        sim.start_round()
        sim.turn(sim.runners[0])  # one bounded turn; no marathon
        plan = next(e['payload'] for e in sim.events if e['type'] == 'AI_TURN_PLAN')
        rationale = next(e['payload'] for e in sim.events if e['type'] == 'AI_TURN_RATIONALE')
        self.assertEqual(plan['movement_cards'], ['GE-016', 'TR-019'])
        self.assertEqual(plan['card_modes'], ['MOVEMENT', 'MOVEMENT'])
        self.assertEqual(plan['movement_energy_cost'], 4)
        self.assertEqual(plan['predicted_movement_quarters'], 8)
        self.assertEqual(rationale['reason_code'], 'WIN_SPEED')


if __name__ == '__main__':
    unittest.main()
