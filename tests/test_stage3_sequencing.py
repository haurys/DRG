"""Bounded Draw 2 and order-of-play regressions; no race-scale simulation."""

import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim, make_condition

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(hand=(), energy=20):
    sim = Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.round = 1
    runner = sim.new_runner(0, 'Balanced', [card(cid) for cid in hand])
    sim.runners = [runner]
    sim.draw = []
    sim.discard = []
    runner.update(energy=energy, pace='Steady', race_turn_number=2)
    return sim, runner


def payloads(sim, kind):
    return [e['payload'] for e in sim.events if e['type'] == kind]


class DrawTwo(unittest.TestCase):
    def test_each_hand_size_and_available_count(self):
        for size in range(7):
            with self.subTest(size=size):
                sim, runner = fixture(('FU-001',) * size)
                sim.draw = [card('TR-001'), card('TR-002')]
                expected = min(2, 6 - size)
                self.assertEqual(sim.replenish(runner), expected)
                self.assertEqual(len(runner['hand']), size + expected)
        sim, runner = fixture()
        sim.draw = [card('TR-001')]
        self.assertEqual(sim.replenish(runner), 1)
        self.assertEqual(sim.replenish(runner), 0)

    def test_conditions_replace_without_using_normal_opportunities(self):
        sim, runner = fixture(('FU-001',) * 4)
        sim.draw = [card('TR-001'), card('CO-005'), card('CO-014'), card('TR-002')]
        self.assertEqual(sim.replenish(runner), 2)
        self.assertEqual(len(runner['hand']), 6)
        self.assertEqual({c['title'] for c in runner['active_conditions']}, {'Blister', 'Side Stitch'})
        self.assertEqual(len(payloads(sim, 'REPLACEMENT_DRAW')), 2)
        self.assertEqual(len(payloads(sim, 'DRAW')), 2)

    def test_recycle_excludes_all_live_zones(self):
        sim, runner = fixture(('FU-001',))
        runner['active_training'] = [{'card': card('TR-001'), 'installed_turn': 0, 'remaining_turns': None}]
        runner['equipped_gear'] = [{'card': card('GE-001'), 'installed_turn': 0, 'remaining_turns': None}]
        runner['attached_gear'] = [{'card': card('GE-008'), 'condition_id': 'CO-005', 'amount': 1}]
        runner['staged_events'] = [{'card': card('EV-029'), 'activate_round': 2}]
        sim.discard = [card(cid) for cid in ('FU-001', 'TR-001', 'GE-001', 'GE-008', 'EV-029', 'TR-002')]
        self.assertEqual(sim.replenish(runner), 1)
        self.assertEqual(runner['hand'][-1]['id'], 'TR-002')
        self.assertEqual(len(sim.draw), 0)


class Sequencing(unittest.TestCase):
    def test_all_five_movement_zone_combinations(self):
        combinations = [('hand',), ('active_training',), ('hand', 'hand'),
                        ('hand', 'active_training'), ('active_training', 'equipped_gear')]
        for sources in combinations:
            with self.subTest(sources=sources):
                sim, runner = fixture(('FU-001', 'FU-002', 'GE-018', 'GE-008', 'TR-019', 'TR-002'))
                runner['active_training'] = [{'card': card('TR-001'), 'installed_turn': 0,
                                              'remaining_turns': None}]
                runner['equipped_gear'] = [{'card': card('GE-001'), 'installed_turn': 0,
                                            'remaining_turns': None}]
                ids = [('FU-001' if i == 0 else 'FU-002') if source == 'hand' else
                       ('TR-001' if source == 'active_training' else 'GE-001')
                       for i, source in enumerate(sources)]
                start = len(runner['hand'])
                sim.turn(runner, {'movement_cards': ids, 'card_sources': list(sources)})
                self.assertEqual(len(payloads(sim, 'PLAY')), len(ids))
                self.assertEqual(len(runner['hand']), start - sources.count('hand'))
                self.assertEqual(len(payloads(sim, 'SLOT_SACRIFICE')), len(ids) - sources.count('hand'))
                self.assertEqual(payloads(sim, 'MOVE')[-1]['total_effort'],
                                 sum(CARDS[cid]['effort'] for cid in ids))

    def test_treat_before_and_after_hand_or_slot_movement(self):
        for timing in ('before', 'after'):
            for source in ('hand', 'active_training'):
                with self.subTest(timing=timing, source=source):
                    sim, runner = fixture(('FU-001', 'FU-002'))
                    runner['active_training'] = [{'card': card('TR-001'), 'installed_turn': 0,
                                                  'remaining_turns': None}]
                    mid = 'FU-002' if source == 'hand' else 'TR-001'
                    sim.turn(runner, {'movement_cards': [mid], 'card_sources': [source],
                                      'treat_prepare': {'action': 'fuel', 'card_id': 'FU-001'},
                                      'treat_timing': timing})
                    changes = payloads(sim, 'FUEL_USE')
                    self.assertEqual(len(changes), 1)
                    self.assertEqual(len(payloads(sim, 'PLAY')), 1)
                    events = [e['type'] for e in sim.events]
                    self.assertLess(events.index('FUEL_USE'), events.index('MOVE')) if timing == 'before' else (
                        self.assertGreater(events.index('FUEL_USE'), events.index('MOVE')))

    def test_post_fuel_cannot_finance_movement(self):
        sim, runner = fixture(('FU-001', 'FU-002'), energy=0)
        runner['will_available'] = False
        with self.assertRaisesRegex(ValueError, 'Movement Energy unavailable'):
            sim.turn(runner, {'movement_cards': ['FU-002'],
                              'treat_prepare': {'action': 'fuel', 'card_id': 'FU-001'},
                              'treat_timing': 'after'})
        self.assertEqual(payloads(sim, 'FUEL_USE'), [])

    def test_slot_sacrifice_then_replacement_has_no_retroactive_effect(self):
        sim, runner = fixture(('GE-018', 'FU-001'))
        runner['equipped_gear'] = [{'card': card('GE-001'), 'installed_turn': 0,
                                    'remaining_turns': None},
                                   {'card': card('GE-008'), 'installed_turn': 0,
                                    'remaining_turns': None}]
        result = sim.turn(runner, {'movement_cards': ['GE-008'],
                                  'card_sources': ['equipped_gear'],
                                  'treat_prepare': {'action': 'gear', 'card_id': 'GE-018'},
                                  'treat_timing': 'after'})
        self.assertIsNotNone(result)
        self.assertEqual({i['card']['id'] for i in runner['equipped_gear']}, {'GE-001', 'GE-018'})
        self.assertEqual(len(runner['hand']), 1)
        self.assertEqual(next(i for i in runner['equipped_gear'] if i['card']['id'] == 'GE-018')
                         ['installed_turn'], runner['race_turn_number'])
        self.assertNotIn('GE-018', [p['card'] for p in payloads(sim, 'SLOT_SACRIFICE')])

    def test_training_gear_and_condition_changes_wait_until_after_movement(self):
        for setup, plan in (
            ('TR-003', {'action': 'training', 'card_id': 'TR-003'}),
            ('GE-001', {'action': 'gear', 'card_id': 'GE-001'}),
            ('FU-016', {'action': 'fuel', 'card_id': 'FU-016', 'choice': 'remedy'}),
        ):
            with self.subTest(setup=setup):
                results = {}
                for timing in ('before', 'after'):
                    sim, runner = fixture(('FU-002', setup))
                    sim.course[0].update(difficulty=0, surface='Asphalt')
                    if setup == 'FU-016':
                        runner['active_conditions'] = [make_condition(card('CO-010'))]
                    sim.turn(runner, {'movement_cards': ['FU-002'], 'treat_prepare': plan,
                                      'treat_timing': timing})
                    results[timing] = (payloads(sim, 'MOVE')[-1], runner, sim)
                before, after = results['before'], results['after']
                if setup == 'TR-003':
                    self.assertEqual(before[1]['energy'], after[1]['energy'] + 1)
                elif setup == 'GE-001':
                    self.assertEqual(before[1]['energy'], after[1]['energy'] + 1)
                else:
                    self.assertGreater(payloads(after[2], 'PACE_PAYMENT')[-1]['final'],
                                       payloads(before[2], 'PACE_PAYMENT')[-1]['final'])
                    self.assertEqual(after[1]['active_conditions'], [])
                self.assertTrue(payloads(after[2], 'POST_MOVEMENT_TREAT'))

    def test_post_treat_rejected_after_finish_or_failed_gut(self):
        for finish in (True, False):
            with self.subTest(finish=finish):
                sim, runner = fixture(('FU-001', 'FU-002'))
                for side in sim.course:
                    side['difficulty'] = 0
                runner['quarter_mile_space'] = len(sim.course) * 4 if finish else 39
                if not finish:
                    sim.marathon_gut[10]['prepared_effort'] = 100
                sim.turn(runner, {'movement_cards': ['FU-002'],
                                  'treat_prepare': {'action': 'fuel', 'card_id': 'FU-001'},
                                  'treat_timing': 'after'})
                self.assertEqual(payloads(sim, 'FUEL_USE'), [])
                self.assertIn('FU-001', [c['id'] for c in runner['hand']])
                self.assertEqual(bool(runner['finish_pending']), finish)
                self.assertEqual(bool(runner['gut_stall']), not finish)

    def test_budget_and_ai_preview_payment(self):
        sim, runner = fixture(('TR-001', 'TR-002', 'FU-001'))
        with self.assertRaisesRegex(ValueError, 'budget exceeded'):
            sim.turn(runner, {'movement_cards': ['TR-001', 'TR-002'],
                              'treat_prepare': {'action': 'fuel', 'card_id': 'FU-001'},
                              'treat_timing': 'after'})
        plan = sim.choose_turn_plan(runner)
        self.assertEqual(plan['treat_timing'] in ('before', 'after'), True)
        self.assertTrue(plan['movement_cards'])
        self.assertEqual(len(plan['card_sources']), len(plan['movement_cards']))


if __name__ == '__main__':
    unittest.main()
