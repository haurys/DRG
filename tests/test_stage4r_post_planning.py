"""Known post-Movement transitions and concealed Event replacements."""

import copy
import json
import unittest
from pathlib import Path

from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {card['id']: card for card in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(card_id):
    return copy.deepcopy(CARDS[card_id])


def fixture(hand, energy=2, position=70, deck=()):
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.round = 1
    runner = sim.new_runner(0, 'Balanced', [card(cid) for cid in hand])
    sim.runners = [runner]
    runner.update(energy=energy, pace='Steady', quarter_mile_space=position,
                  race_turn_number=2)
    sim.draw = [card(cid) for cid in deck]
    sim.discard = []
    for side in sim.course:
        side['difficulty'] = 0
    return sim, runner


def events(sim, kind):
    return [event['payload'] for event in sim.events if event['type'] == kind]


HAND = ('EV-017', 'FU-001', 'FU-003', 'FU-004', 'EV-026', 'GE-008')


class PostMovementPlanning(unittest.TestCase):
    def test_autonomous_tough_decision_selects_surviving_fuel(self):
        sim, runner = fixture(HAND, deck=('TR-001', 'TR-002'))
        capture = {}
        selected = sim.choose_turn_plan(runner, capture)
        self.assertEqual((selected['movement_cards'], selected['card_modes'],
                          selected['treat_timing']), (['EV-017'], ['EFFECT'], 'after'))
        self.assertEqual(selected['treat_prepare']['card_id'], 'FU-004')
        self.assertFalse(any(row['movement_cards'] == ['EV-017'] and
                             row['card_modes'] == ['EFFECT'] and
                             row['treat_timing'] == 'after' and row['treat_prepare'] and
                             row['treat_prepare'].get('card_id') == 'FU-001'
                             for row in capture['candidates']))
        sim.turn(runner)
        self.assertEqual(events(sim, 'TOUGH_DECISION')[0]['cycled'], ['FU-001', 'FU-003'])
        self.assertEqual((events(sim, 'MOVE')[-1]['quarter_miles'], runner['energy']), (1, 3))
        self.assertEqual((runner['stats']['cards_played'], runner['stats']['treat_prepare_actions']),
                         (2, 1))
        self.assertEqual(events(sim, 'POST_MOVEMENT_TREAT_SKIP'), [])
        self.assertEqual([e['card'] for e in events(sim, 'FUEL_USE')], ['FU-004'])
        self.assertEqual(runner['race_status'], 'RUNNING')

    def test_former_candidate_is_invalid_in_planner_state(self):
        sim, runner = fixture(HAND, deck=('TR-001', 'TR-002'))
        chosen = next(cards for cards in sim.movement_candidates(runner, 1)
                      if [c['id'] for c in cards] == ['EV-017'] and
                      cards[0]['use_mode'] == 'EFFECT')
        after_cards = sim.preview_slot_sacrifice(runner, chosen)
        after_cards['hand'] = [c for c in after_cards['hand'] if c['id'] != 'EV-017']
        paid = sim.preview_payment(after_cards)
        resolved = sim.preview_gut_progress(paid, sim.preview_movement(paid, chosen), chosen)
        post = sim.preview_post_movement_state(paid, chosen, resolved)
        self.assertEqual(post['energy'], 1)
        self.assertNotIn('FU-001', [c['id'] for c in post['hand']])
        self.assertNotIn('FU-001', [plan['card_id'] for plan in sim.treat_candidates(post)
                                      if plan])
        plan = {'card_id': 'FU-004', 'action': 'fuel', 'choice': 'energy'}
        self.assertEqual(sim.preview_preparation(post, plan)['energy'], 3)

    def test_water_station_removes_post_treatment_target(self):
        sim, runner = fixture(('FU-002', 'FU-016'), energy=20, position=15)
        runner['active_conditions'] = [m.make_condition(card('CO-010'))]
        capture = {}
        sim.choose_turn_plan(runner, capture)
        self.assertFalse(any(row['treat_timing'] == 'after' and
                             row['treat_prepare'] == {'card_id': 'FU-016', 'action': 'fuel',
                                                      'choice': 'remedy'} and
                             row['movement_cards'] == ['FU-002']
                             for row in capture['candidates']))
        self.assertTrue(any(row['treat_timing'] == 'after' and
                            row['treat_prepare'] == {'card_id': 'FU-016', 'action': 'fuel',
                                                     'choice': 'energy'} and
                            row['movement_cards'] == ['FU-002']
                            for row in capture['candidates']))
        sim.turn(runner, {'movement_cards': ['FU-002']})
        self.assertFalse(runner['active_conditions'])
        self.assertEqual(runner['stats']['treat_prepare_actions'], 0)
        self.assertIn('FU-016', [c['id'] for c in runner['hand']])

    def test_unknown_replacement_condition_may_legally_skip_later_fuel(self):
        selections = []
        for deck, expected_energy, expected_skips in (
            (('TR-001', 'TR-002'), 3, 0),
            (('TR-001', 'TR-002', 'CO-012'), 1, 1),
        ):
            sim, runner = fixture(HAND, deck=deck)
            selections.append(sim.choose_turn_plan(runner))
            sim.turn(runner)
            self.assertEqual(runner['energy'], expected_energy)
            self.assertEqual(len(events(sim, 'POST_MOVEMENT_TREAT_SKIP')), expected_skips)
            self.assertEqual(runner['stats']['cards_played'], 2 - expected_skips)
            self.assertEqual(runner['stats']['treat_prepare_actions'], 1 - expected_skips)
            self.assertEqual(len(events(sim, 'FUEL_USE')), 1 - expected_skips)
            self.assertEqual(runner['race_status'], 'RUNNING')
            if expected_skips:
                self.assertIn('FU-004', [c['id'] for c in runner['hand']])
                self.assertIn('Nausea', [c['title'] for c in runner['active_conditions']])
        self.assertEqual(selections[0], selections[1])

    def test_known_event_energy_counts_at_gut_before_post_treatment(self):
        sim, runner = fixture(('EV-021', 'FU-002'), energy=1, position=39)
        sim.marathon_gut[10] = {'prepared_effort': 5, 'energy': 3}
        choice = next(cards for cards in sim.movement_candidates(runner, 1)
                      if [c['id'] for c in cards] == ['EV-021'] and
                      cards[0]['use_mode'] == 'EFFECT')
        projected = copy.deepcopy(runner)
        projected['hand'] = [card('FU-002')]
        paid = sim.preview_payment(projected)
        preview = sim.preview_gut_progress(paid, sim.preview_movement(paid, choice), choice)
        self.assertTrue(preview['gut_preview']['passed'])
        self.assertEqual(preview['gut_preview']['energy'], 3)
        sim.turn(runner, {'movement_cards': ['EV-021'], 'card_modes': ['EFFECT']})
        self.assertIsNone(runner['gut_stall'])
        self.assertEqual(runner['energy'], 3)

    def test_half_gut_penalty_is_known_before_post_treatment(self):
        sim, runner = fixture(('FU-001', 'FU-002'), energy=4, position=23)
        sim.cfg['race_format'] = 'half'
        selected = next(cards for cards in sim.movement_candidates(runner, 1)
                        if [c['id'] for c in cards] == ['FU-001'])
        paid_state = copy.deepcopy(runner)
        paid_state['hand'] = [card('FU-002')]
        paid = sim.preview_payment(paid_state)
        resolved = sim.preview_movement(paid, selected)
        projected = sim.preview_post_movement_state(paid, selected, resolved)
        self.assertEqual(projected['energy'], 1)
        sim.turn(runner, {'movement_cards': ['FU-001']})
        self.assertEqual(runner['energy'], 1)


if __name__ == '__main__':
    unittest.main()
