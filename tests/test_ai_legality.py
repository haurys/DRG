import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai_legality', ROOT / 'engine/simulate.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
CONFIG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {card['id']: card for card in json.loads((ROOT / 'data/race_cards.json').read_text())}
SIDES = {side['id']: side for side in json.loads((ROOT / 'data/course_cards.json').read_text())}


def card(card_id):
    return copy.deepcopy(CARDS[card_id])


def fixture(players=1):
    sim = engine.Sim(ROOT, copy.deepcopy(CONFIG))
    sim.course = [dict(copy.deepcopy(SIDES[side_id]), mile=mile)
                  for mile, side_id in enumerate(('C-22-B', 'C-05-A', 'C-09-A', 'C-01-B'), 1)]
    sim.runners = [sim.new_runner(index, 'Balanced', []) for index in range(players)]
    sim.draw = []
    sim.discard = []
    return sim


def condition(card_id):
    return engine.make_condition(card(card_id))


class AILegalityRegression(unittest.TestCase):
    def test_round_three_stopping_state_falls_back_and_completes_live_turn(self):
        sim = fixture(2)
        runner, opponent = sim.runners
        runner['quarter_mile_space'] = 7
        runner['energy'] = 13
        runner['hand'] = [card(id_) for id_ in ('EV-010', 'FU-008', 'GE-006', 'GE-014',
                                               'GE-013', 'FU-010', 'FU-019')]
        runner['equipped_gear'] = [{'card': card('GE-016'), 'remaining_turns': None},
                                   {'card': card('GE-002'), 'remaining_turns': None}]
        runner['active_conditions'] = [condition('CO-013'), condition('CO-002'),
                                       condition('CO-012')]
        opponent['hand'] = [card('TR-001')]
        sim.start_round({'P1': 'Race', 'P2': 'Easy'})
        selected = sim.choose_treat_prepare(runner)
        self.assertTrue(sim.legal_treat_prepare(runner, selected))
        self.assertFalse(sim.legal_treat_prepare(runner, {'card_id': 'FU-019', 'action': 'fuel',
                                                         'choice': 'remedy'}))
        result = sim.turn(runner)
        self.assertIsNotNone(result)
        types = [event['type'] for event in sim.events if event['player_id'] == 'P1']
        self.assertIn('PACE_PAYMENT', types)
        self.assertIn('MOVE', types)
        self.assertIn('TURN_END', types)
        self.assertFalse(any(event['type'] == 'FUEL_USE' for event in sim.events))

    def test_stomach_trouble_filters_every_fuel_treat_prepare_candidate(self):
        sim = fixture()
        runner = sim.runners[0]
        runner['energy'] = 5
        runner['active_conditions'] = [condition('CO-013'), condition('CO-002'),
                                       condition('CO-010')]
        for fuel in (c for c in CARDS.values() if c['family'] == 'Fuel'):
            with self.subTest(card=fuel['id']):
                runner['hand'] = [card(fuel['id'])]
                self.assertFalse(sim.legal_treat_prepare(runner, {'card_id': fuel['id'],
                                                                  'action': 'fuel'}))
                self.assertIsNone(sim.choose_treat_prepare(runner))

    def test_fuel_remedy_restored_when_stomach_trouble_removed_or_zero(self):
        sim = fixture()
        runner = sim.runners[0]
        stomach = condition('CO-013')
        runner['active_conditions'] = [stomach, condition('CO-002')]
        runner['hand'] = [card('FU-019')]
        self.assertIsNone(sim.choose_treat_prepare(runner))
        stomach['current_severity'] = 0
        engine.update_effective_severity(stomach)
        expected = {'card_id': 'FU-019', 'action': 'fuel', 'choice': 'remedy'}
        self.assertIn(expected, sim.treat_candidates(runner))
        stomach['current_severity'] = 5
        engine.update_effective_severity(stomach)
        runner['active_conditions'].remove(stomach)
        self.assertIn(expected, sim.treat_candidates(runner))

    def test_stomach_trouble_skips_treat_prepare_when_only_fuel_is_held(self):
        sim = fixture()
        runner = sim.runners[0]
        runner['active_conditions'] = [condition('CO-013'), condition('CO-002')]
        runner['hand'] = [card('FU-019')]
        sim.start_round({'P1': 'Race'})
        sim.turn(runner)
        self.assertEqual([event['payload']['action'] for event in sim.events
                          if event['type'] == 'TREAT_PREPARE'], ['none'])
        self.assertTrue(any(event['type'] == 'MOVE' for event in sim.events))

    def test_condition_pace_caps_filter_before_scoring(self):
        for condition_id, maximum in (('CO-015', 'Steady'), ('CO-016', 'Easy'),
                                      ('CO-001', 'Race')):
            with self.subTest(condition=condition_id):
                sim = fixture()
                runner = sim.runners[0]
                runner['active_conditions'] = [condition(condition_id)]
                options, selected = sim.choose_pace(runner)
                self.assertTrue(all(engine.PACE_ORDER.index(option['pace'])
                                    <= engine.PACE_ORDER.index(maximum) for option in options))
                self.assertLessEqual(engine.PACE_ORDER.index(selected),
                                     engine.PACE_ORDER.index(maximum))

    def test_target_lock_filters_other_event_before_ai_card_scoring(self):
        sim = fixture(2)
        source, target = sim.runners
        source['hand'] = [card('EV-002'), card('TR-001')]
        target['staged_events'] = [{'card': card('EV-009'), 'source': 'P1',
                                    'target': 'P2', 'staged_round': 1, 'activate_round': 2}]
        self.assertIsNone(sim.event_target(source))
        self.assertEqual([c['id'] for c in sim.choose_movement_cards(source, 2)], ['TR-001'])
        target['staged_events'] = []
        self.assertEqual([c['id'] for c in sim.choose_movement_cards(source, 2)],
                         ['EV-002', 'TR-001'])

    def test_attachment_slots_footwear_and_card_limits(self):
        sim = fixture()
        runner = sim.runners[0]
        runner['hand'] = [card('GE-003'), card('GE-005'), card('TR-015')]
        runner['active_conditions'] = [condition('CO-002')]
        runner['active_training'] = [{'card': card(id_), 'remaining_turns': None}
                                     for id_ in ('TR-001', 'TR-002', 'TR-003')]
        runner['equipped_gear'] = [{'card': card(id_), 'remaining_turns': None}
                                   for id_ in ('GE-001', 'GE-006', 'GE-008')]
        self.assertFalse(sim.legal_treat_prepare(runner, {'card_id': 'GE-003', 'action': 'attach',
                                                         'condition_id': 'CO-002'}))
        self.assertTrue(sim.legal_treat_prepare(runner, {'card_id': 'GE-005', 'action': 'gear',
                                                         'replace_id': 'GE-001'}))
        self.assertIn({'card_id': 'GE-005', 'action': 'gear', 'replace_id': 'GE-001'},
                      sim.treat_candidates(runner))
        self.assertEqual(len(sim.choose_movement_cards(runner, 2)), 2)
        self.assertFalse(any(c['family'] == 'Event' for c in sim.choose_movement_cards(runner, 2)))

    def test_event_budget_and_helpful_runner_full_hand_fallback(self):
        sim = fixture(2)
        giver, recipient = sim.runners
        giver['hand'] = [card('EV-020'), card('EV-022'), card('TR-001')]
        recipient['hand'] = [card(id_) for id_ in ('TR-002', 'TR-003', 'TR-004',
                                                  'TR-005', 'TR-006', 'TR-007', 'TR-008')]
        selected = sim.choose_movement_cards(giver, 2)
        self.assertLessEqual(len(selected), 2)
        self.assertLessEqual(sum(c['family'] == 'Event' for c in selected), 1)
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(giver, {'treat_prepare': None, 'movement_cards': ['EV-020']})
        self.assertEqual(len(recipient['hand']), 7)
        self.assertFalse(any(e['type'] == 'HELPFUL_RUNNER_TRANSFER' for e in sim.events))
        self.assertTrue(any(e['type'] == 'DISCARD' and e['payload']['card'] == 'EV-020'
                            for e in sim.events))


if __name__ == '__main__':
    unittest.main()
