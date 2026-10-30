"""Stage 6A-R turn-record schema and capture regressions."""

import copy
import json
import unittest
from pathlib import Path

from engine.ai_rationale import describe_decision
from engine.simulate import Sim, diagnostics, make_condition


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {card['id']: card for card in json.loads((ROOT / 'data/race_cards.json').read_text())}
DIAGNOSTIC_FIELDS = ('movement_quarters', 'movement_result',
                     'converted_movement_quarters', 'finish_discarded_quarters',
                     'gut_movement_lost_quarters', 'boundaries', 'hand_size_at_decision',
                     'effort_count', 'energy_effect_count')


def card(card_id):
    return copy.deepcopy(CARDS[card_id])


def fixture(hand=(), energy=0, players=1, position=0):
    sim = Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.round = 1
    sim.runners = [sim.new_runner(i, 'Balanced', [card(cid) for cid in hand])
                   for i in range(players)]
    sim.draw = []
    sim.discard = []
    runner = sim.runners[0]
    runner.update(energy=energy, pace='Steady', will_available=False,
                  quarter_mile_space=position, distance_completed=position / 4)
    for segment in sim.course:
        segment['difficulty'] = 0
    return sim, runner


class TurnRecordSchema(unittest.TestCase):
    def test_stopped_and_recovery_records_have_explicit_zero_diagnostics(self):
        sim, runner = fixture(hand=('TR-001',))
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'STOPPED')
        sim.round = 2
        sim.turn(runner, {'assistance_accept': False})
        self.assertEqual(runner['race_status'], 'DNF')
        for record in sim.turn_records:
            for field in DIAGNOSTIC_FIELDS:
                self.assertIn(field, record)
            self.assertEqual(record['finish_discarded_quarters'], 0)
            self.assertEqual(record['gut_movement_lost_quarters'], 0)
        self.assertEqual(diagnostics(sim)['movement_discarded_at_finish_miles'], 0)

    def test_assisted_final_failure_has_complete_record(self):
        sim, runner = fixture(hand=('EV-001', 'TR-001'), players=2)
        sim.runners[1]['hand'] = [card('FU-002')]
        sim.turn(runner)
        sim.round = 2
        sim.turn(runner, {'assistance_accept': True})
        sim.round = 3
        sim.draw = [card('EV-021'), card('CO-012')]
        sim.turn(runner)
        self.assertEqual(runner['race_status'], 'DNF')
        self.assertEqual(sim.turn_records[-1]['energy_recovery_phase'], 'assisted_final')
        self.assertTrue(all(all(field in record for field in DIAGNOSTIC_FIELDS)
                            for record in sim.turn_records))
        diagnostics(sim)

    def test_gut_recovery_and_movement_finish_mixed(self):
        gut, runner = fixture(position=40)
        runner['gut_stall'] = {'mile': 10, 'recovery_turns_used': 0,
            'recovery_turns_allowed': 4, 'failure_type': 'energy_only',
            'prepared_effort': 0, 'energy': 0, 'exchange_used': False,
            'assistance_used': False, 'fuel_used': False, 'will_used': False,
            'arrival_round': 0, 'arrival_turn': 0}
        gut.turn(runner)
        self.assertTrue(gut.turn_records[-1]['gut_recovery_turn'])

        normal, moving = fixture(hand=('TR-001',), energy=20)
        normal.turn(moving, {'movement_cards': ['TR-001']})

        finish, finisher = fixture(hand=('EV-023', 'TR-019'), energy=20, position=100)
        finish.turn(finisher, {'movement_cards': ['EV-023', 'TR-019']})
        self.assertTrue(finisher['finish_pending'])
        self.assertGreater(finish.turn_records[-1]['finish_discarded_quarters'], 0)

        combined = normal
        combined.turn_records = gut.turn_records + normal.turn_records + finish.turn_records
        for record in combined.turn_records:
            for field in DIAGNOSTIC_FIELDS:
                self.assertIn(field, record)
        result = diagnostics(combined)
        self.assertEqual(result['turns'], 3)
        self.assertGreater(result['movement_discarded_at_finish_miles'], 0)


class Seed101Rationale(unittest.TestCase):
    def test_post_movement_gear_replacement_does_not_remove_payment_source_early(self):
        config = copy.deepcopy(CFG)
        config['seed'] = 101
        sim = Sim(ROOT, config)
        sim.build_course()
        sim.round = 11
        runner = sim.new_runner(4, 'Pack Runner', [card(cid) for cid in
            ('FU-007', 'TR-014', 'FU-008', 'GE-005', 'TR-013', 'TR-005')])
        runner.update(energy=0, pace='Steady', will_available=False, race_turn_number=11,
                      quarter_mile_space=37, pack_state='PACK-R11-1',
                      pack_members_snapshot=['P3', 'P6', 'P2', 'P7', 'P5'])
        runner['equipped_gear'] = [{'card': card('GE-004'), 'installed_turn': 8,
                                     'remaining_turns': None}]
        runner['active_conditions'] = [make_condition(card(cid)) for cid in
                                       ('CO-005', 'CO-006', 'CO-007', 'CO-009')]
        positions = {2: 38, 3: 39, 4: 36, 6: 39, 7: 38, 8: 39}
        sim.runners = [sim.new_runner(i - 1, 'Balanced', []) for i in positions] + [runner]
        for other in sim.runners[:-1]:
            other['quarter_mile_space'] = positions[int(other['player_id'][1:])]
        capture = {}
        selected = sim.choose_turn_plan(runner, capture)
        self.assertEqual((selected['movement_cards'], selected['treat_prepare']['card_id']),
                         (['TR-014'], 'TR-005'))
        post = next(row for row in capture['candidates'] if row['treat_timing'] == 'after'
                    and row['movement_cards'] == ['TR-014'] and row['treat_prepare']
                    and row['treat_prepare'].get('card_id') == 'GE-005'
                    and row['treat_prepare'].get('replace_id') == 'GE-004')
        self.assertEqual(post['movement_quarters'], 1)
        before = copy.deepcopy(runner)
        rationale = describe_decision(sim, runner, capture)
        self.assertEqual(runner, before)
        self.assertEqual(rationale['selected_plan']['projected_movement_quarters'], 1)


if __name__ == '__main__':
    unittest.main()
