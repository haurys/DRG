"""Post-Movement eligibility is determined when Treat/Prepare resolves."""

import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim, make_condition


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'simulation/config.json').read_text())


def events(sim, name):
    return [event for event in sim.events if event['type'] == name]


def fixture(position=63, hand=('FU-008', 'FU-016', 'GE-010', 'GE-002'),
            conditions=('CO-002', 'CO-012', 'CO-013'), draw=('FU-019', 'EV-023')):
    config = copy.deepcopy(CONFIG)
    config['seed'] = 303
    sim = Sim(ROOT, config)
    sim.build_course()
    sim.round = 30
    card = lambda cid: copy.deepcopy(sim.card(cid))
    runner = sim.new_runner(7, 'Adaptive', [card(cid) for cid in hand])
    runner.update(energy=0, pace='Steady', round_start_pace='Steady', will_available=False,
                  race_turn_number=29, quarter_mile_space=position,
                  distance_completed=position / 4, exchanges_used=3)
    runner['gut_cleared'] = {10}
    runner['active_training'] = [
        {'card': card('TR-005'), 'installed_turn': 11, 'remaining_turns': None},
        {'card': card('TR-001'), 'installed_turn': 29, 'remaining_turns': None}]
    runner['active_conditions'] = [make_condition(card(cid)) for cid in conditions]
    profiles = ('Balanced', 'Aggressive', 'Energy Conservative', 'Course Planner',
                'Pack Runner', 'Opportunist', 'Front Runner')
    sim.runners = [sim.new_runner(i, profile, []) for i, profile in enumerate(profiles)] + [runner]
    for other, space in zip(sim.runners[:-1], (104, 80, 47, 99, 92, 32, 51)):
        other['quarter_mile_space'] = space
    for index in (2, 5, 6):
        sim.runners[index].update(dnf=True, race_status='DNF')
    sim.runners[0]['finish_pending'] = True
    sim.draw = [card(cid) for cid in reversed(draw)]
    sim.discard = []
    return sim, runner


class PostMovementLegality(unittest.TestCase):
    def test_seed303_autonomous_post_aid_salt_tabs_remedy(self):
        sim, runner = fixture()
        self.assertFalse(sim.fuel_available(runner))
        resolved = sim.turn(runner)
        plan = events(sim, 'AI_TURN_PLAN')[-1]['payload']
        self.assertEqual((plan['movement_cards'], plan['card_modes'], plan['treat_timing'],
                          plan['treat_prepare']),
                         (['EV-023'], ['EFFECT'], 'after',
                          {'action': 'fuel', 'card_id': 'FU-019', 'choice': 'remedy'}))
        self.assertEqual((resolved['from_space'], resolved['to_space'], resolved['quarter_miles']),
                         (63, 64, 1))
        self.assertEqual({condition['title'] for condition in runner['active_conditions']}, set())
        self.assertEqual(runner['energy'], 0)
        self.assertEqual(runner['race_status'], 'RUNNING')
        self.assertEqual(len(events(sim, 'POST_MOVEMENT_TREAT')), 1)
        self.assertEqual(len(events(sim, 'FUEL_USE')), 1)
        self.assertEqual(len(events(sim, 'PLAY')), 1)
        self.assertEqual(sim.turn_records[-1]['cards_played'], 2)
        self.assertEqual(runner['stats']['treat_prepare_actions'], 1)
        aid = [e['sequence'] for e in events(sim, 'MILESTONE')
               if e['payload']['kind'] == 'Aid/Fuel' and e['payload']['mile'] == 16]
        self.assertEqual(len(aid), 1)
        self.assertLess(aid[0], events(sim, 'FUEL_USE')[-1]['sequence'])
        self.assertFalse(any(c['id'] == 'FU-019' for c in runner['hand']))

    def test_nausea_still_blocks_fuel_when_aid_is_not_crossed(self):
        sim, runner = fixture(position=60)
        action = {'action': 'fuel', 'card_id': 'FU-019', 'choice': 'remedy'}
        with self.assertRaisesRegex(ValueError, 'post-Movement Treat/Prepare'):
            sim.turn(runner, {'movement_cards': ['EV-023'], 'card_modes': ['EFFECT'],
                              'treat_prepare': action, 'treat_timing': 'after'})
        self.assertLess(runner['quarter_mile_space'], 64)
        self.assertIn('Nausea', [c['title'] for c in runner['active_conditions']])
        self.assertIn('Cramp', [c['title'] for c in runner['active_conditions']])
        self.assertTrue(any(c['id'] == 'FU-019' for c in runner['hand']))
        self.assertEqual(runner['stats']['treat_prepare_actions'], 0)
        self.assertEqual(events(sim, 'FUEL_USE'), [])

    def test_known_water_remedy_obsoletes_post_treatment_target(self):
        sim, runner = fixture(hand=('FU-016', 'EV-023'), conditions=('CO-010',), draw=())
        runner['energy'] = 2
        sim.ai_rationale_enabled = False
        original_choose = sim.choose_turn_plan
        selected = {
            'treat_prepare': {'action': 'fuel', 'card_id': 'FU-016', 'choice': 'remedy'},
            'treat_timing': 'after', 'movement_cards': ['EV-023'], 'card_modes': ['EFFECT'],
            'card_sources': ['hand'], 'movement_energy_cost': 0, 'movement_quarters': 1,
            'score': 0, 'expected_turns_remaining': 0}
        sim.choose_turn_plan = lambda *args, **kwargs: (original_choose(*args, **kwargs)
            if len(args) > 1 and args[1] is not None or kwargs.get('capture') is not None
            else selected)
        sim.turn(runner)
        self.assertEqual(len(events(sim, 'POST_MOVEMENT_TREAT_SKIP')), 1)
        self.assertEqual(events(sim, 'FUEL_USE'), [])
        self.assertTrue(any(c['id'] == 'FU-016' for c in runner['hand']))
        self.assertEqual(runner['stats']['treat_prepare_actions'], 0)

    def test_fuel_before_movement_can_pay_pace(self):
        sim, runner = fixture(hand=('FU-008', 'EV-023'), conditions=(), draw=())
        sim.turn(runner, {'movement_cards': ['EV-023'], 'card_modes': ['EFFECT'],
                          'treat_prepare': {'action': 'fuel', 'card_id': 'FU-008', 'choice': 'energy'},
                          'treat_timing': 'before'})
        self.assertEqual(runner['energy'], 2)  # Fuel +2, installed +1, Steady costs 1.
        self.assertEqual(len(events(sim, 'FUEL_USE')), 1)
        self.assertLess(events(sim, 'FUEL_USE')[0]['sequence'], events(sim, 'PLAY')[0]['sequence'])

    def test_post_fuel_cannot_pay_for_earlier_movement(self):
        sim, runner = fixture(hand=('FU-008', 'TR-001'), conditions=(), draw=())
        runner['active_training'] = []
        sim.turn(runner, {'movement_cards': ['TR-001'],
                          'treat_prepare': {'action': 'fuel', 'card_id': 'FU-008',
                                            'choice': 'energy'}, 'treat_timing': 'after'})
        self.assertEqual(runner['race_status'], 'STOPPED')
        self.assertEqual(runner['quarter_mile_space'], 63)
        self.assertEqual(events(sim, 'FUEL_USE'), [])
        self.assertTrue(any(c['id'] == 'FU-008' for c in runner['hand']))

    def test_two_movement_cards_leave_no_post_treatment_budget(self):
        sim, runner = fixture(hand=('FU-008', 'EV-023', 'GE-002'), conditions=(), draw=())
        with self.assertRaisesRegex(ValueError, 'card-play budget exceeded'):
            sim.turn(runner, {'movement_cards': ['EV-023', 'GE-002'],
                              'card_modes': ['EFFECT', 'MOVEMENT'],
                              'treat_prepare': {'action': 'fuel', 'card_id': 'FU-008',
                                                'choice': 'energy'}, 'treat_timing': 'after'})
        self.assertEqual(events(sim, 'PLAY'), [])
        self.assertEqual(events(sim, 'FUEL_USE'), [])

    def test_finish_interrupts_post_movement_fuel(self):
        sim, runner = fixture(position=103, hand=('FU-008', 'EV-023'),
                              conditions=(), draw=())
        sim.turn(runner, {'movement_cards': ['EV-023'], 'card_modes': ['EFFECT'],
                          'treat_prepare': {'action': 'fuel', 'card_id': 'FU-008',
                                            'choice': 'energy'}, 'treat_timing': 'after'})
        self.assertTrue(runner['finish_pending'])
        self.assertEqual(events(sim, 'POST_MOVEMENT_TREAT'), [])
        self.assertEqual(events(sim, 'FUEL_USE'), [])
        self.assertTrue(any(c['id'] == 'FU-008' for c in runner['hand']))

    def test_failed_gut_arrival_interrupts_post_movement_fuel(self):
        sim, runner = fixture(position=39, hand=('FU-008', 'EV-023'),
                              conditions=(), draw=())
        runner['gut_cleared'] = set()
        sim.turn(runner, {'movement_cards': ['EV-023'], 'card_modes': ['EFFECT'],
                          'treat_prepare': {'action': 'fuel', 'card_id': 'FU-008',
                                            'choice': 'energy'}, 'treat_timing': 'after'})
        self.assertEqual(runner['quarter_mile_space'], 40)
        self.assertIsNotNone(runner['gut_stall'])
        self.assertEqual(runner['gut_stall']['mile'], 10)
        self.assertEqual(events(sim, 'POST_MOVEMENT_TREAT'), [])
        self.assertEqual(events(sim, 'FUEL_USE'), [])
        self.assertTrue(any(c['id'] == 'FU-008' for c in runner['hand']))


if __name__ == '__main__':
    unittest.main()
