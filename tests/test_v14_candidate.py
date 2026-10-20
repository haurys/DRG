"""Bounded v1.4 hand, zone, and Direct Slot Movement cases."""
import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(players=1):
    cfg = copy.deepcopy(CFG)
    cfg['player_count'] = players
    sim = Sim(ROOT, cfg)
    sim.build_course()
    sim.runners = [sim.new_runner(i, 'Balanced', []) for i in range(players)]
    sim.draw = []
    sim.discard = []
    return sim, sim.runners[0]


def events(sim, kind):
    return [e for e in sim.events if e['type'] == kind]


class HandAndDeck(unittest.TestCase):
    def test_start_six_and_three_exchanges(self):
        sim = Sim(ROOT, copy.deepcopy(CFG))
        sim.setup()
        self.assertTrue(all(len(r['hand']) == 6 for r in sim.runners))
        self.assertEqual(sim.cfg['exchange_limit'], 3)

    def test_one_draw_below_max_no_refill_and_zero_hand_legal(self):
        sim, r = fixture()
        sim.draw = [card('FU-001'), card('FU-002'), card('FU-003')]
        self.assertEqual(sim.replenish(r), 1)
        self.assertEqual(len(r['hand']), 1)
        self.assertEqual(sim.replenish(r), 1)
        self.assertEqual(len(r['hand']), 2)
        r['hand'] = [card('TR-001') for _ in range(6)]
        self.assertEqual(sim.replenish(r), 0)
        self.assertEqual(len(sim.draw), 1)
        r['hand'] = []
        sim.draw = []
        sim.discard = []
        self.assertEqual(sim.replenish(r), 0)
        self.assertEqual(r['hand'], [])
        self.assertTrue(events(sim, 'DRAW_FAILED'))

    def test_recycle_excludes_hands_slots_and_attachments(self):
        sim, r = fixture()
        r['hand'] = [card('FU-001')]
        r['active_training'] = [{'card': card('TR-001'), 'remaining_turns': None}]
        r['equipped_gear'] = [{'card': card('GE-001'), 'remaining_turns': None}]
        r['attached_gear'] = [{'card': card('GE-003'), 'condition_id': 'CO-005',
                               'amount': 2, 'remaining_turns': None}]
        sim.discard = [card(cid) for cid in ('FU-001', 'TR-001', 'GE-001', 'GE-003', 'FU-002')]
        self.assertEqual(sim.draw_one(r)['id'], 'FU-002')
        self.assertEqual({c['id'] for c in sim.discard}, {'FU-001', 'TR-001', 'GE-001', 'GE-003'})


class SlotMovement(unittest.TestCase):
    def test_commitment_install_turn_next_turn_and_third_turn(self):
        sim, r = fixture()
        r['race_turn_number'] = 10
        sim.install_training(r, card('TR-019'))
        for turn, eligible in ((10, False), (11, False), (12, True)):
            r['race_turn_number'] = turn
            with self.subTest(turn=turn):
                self.assertEqual(any(c.get('source') == 'active_training'
                                     for pair in sim.movement_candidates(r, 2) for c in pair), eligible)

    def test_hand_plus_slot_and_slot_plus_slot_and_budget(self):
        sim, r = fixture()
        r['race_turn_number'] = 3
        r['hand'] = [card('FU-001')]
        r['active_training'] = [{'card': card('TR-001'), 'remaining_turns': None,
                                 'installed_turn': 1}]
        r['equipped_gear'] = [{'card': card('GE-001'), 'remaining_turns': None,
                               'installed_turn': 1}]
        pairs = [pair for pair in sim.movement_candidates(r, 2) if len(pair) == 2]
        sources = {tuple(sorted(c['source'] for c in pair)) for pair in pairs}
        self.assertIn(('active_training', 'hand'), sources)
        self.assertIn(('active_training', 'equipped_gear'), sources)
        self.assertFalse(any(len(pair) > 2 for pair in sim.movement_candidates(r, 2)))
        self.assertFalse(any(len(pair) > 1 for pair in sim.movement_candidates(r, 1)))

    def test_slot_sacrifice_before_effect_and_payment_with_will(self):
        sim, r = fixture()
        sim.course[0].update(elevation='Incline', difficulty=4, surface='Asphalt')
        r['race_turn_number'] = 2
        r['energy'] = 0
        r['active_training'] = [{'card': card('TR-009'), 'remaining_turns': None,
                                 'installed_turn': 0}]
        self.assertEqual(sim.preview_movement(r, [{**card('TR-009'), 'use_mode': 'MOVEMENT'}])[
            'quarter_miles'], 3)
        sim.turn(r, {'movement_cards': ['TR-009']})
        self.assertFalse(r['active_training'])
        self.assertFalse(r['will_available'])
        self.assertEqual([e['payload']['card'] for e in events(sim, 'SLOT_SACRIFICE')], ['TR-009'])
        self.assertLess(events(sim, 'SLOT_SACRIFICE')[0]['sequence'], events(sim, 'PACE_PAYMENT')[0]['sequence'])
        self.assertEqual(events(sim, 'MOVE')[0]['payload']['starting_effective_difficulty'], 4)
        self.assertEqual(events(sim, 'PLAY')[0]['payload']['source'], 'active_training')
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['payload']['covered_by_will'], 2)
        self.assertIn('TR-009', [c['id'] for c in sim.discard])

    def test_sacrificed_energy_gear_cannot_grant_same_turn_energy(self):
        sim, r = fixture()
        sim.course[0].update(surface='Asphalt', difficulty=1)
        r['race_turn_number'] = 2
        r['energy'] = 0
        r['equipped_gear'] = [{'card': card('GE-001'), 'remaining_turns': None,
                               'installed_turn': 0}]
        sim.turn(r, {'movement_cards': ['GE-001']})
        self.assertEqual(r['energy'], 0)
        self.assertFalse(any(e['payload'].get('source') == 'Installed GE-001'
                             for e in events(sim, 'ENERGY_CHANGE')))

    def test_replacement_discards_and_resets_commitment(self):
        sim, r = fixture()
        r['race_turn_number'] = 9
        r['active_training'] = [{'card': card('TR-001'), 'remaining_turns': None,
                                 'installed_turn': 1}, {'card': card('TR-002'),
                                 'remaining_turns': None, 'installed_turn': 1}]
        sim.install_training(r, card('TR-003'), replace_id='TR-001')
        self.assertIn('TR-001', [c['id'] for c in sim.discard])
        self.assertEqual(next(i for i in r['active_training'] if i['card']['id'] == 'TR-003')[
            'installed_turn'], 9)
        self.assertNotIn('TR-003', [c['id'] for p in sim.movement_candidates(r, 2) for c in p
                                    if c.get('source') == 'active_training'])

    def test_slot_continuation_prevents_premature_dnf(self):
        sim, r = fixture()
        r['energy'] = 0
        r['will_available'] = True
        r['race_turn_number'] = 3
        r['active_training'] = [{'card': card('TR-019'), 'remaining_turns': None,
                                 'installed_turn': 1}]
        self.assertTrue(sim.continuation_paths(r)['viable'])

    def test_ai_can_select_slot_card_with_empty_hand_and_explain_source(self):
        sim, r = fixture()
        r['race_turn_number'] = 2
        r['active_training'] = [{'card': card('TR-019'), 'remaining_turns': None,
                                 'installed_turn': 0}]
        sim.turn(r)
        self.assertEqual(events(sim, 'PLAY')[0]['payload']['source'], 'active_training')
        self.assertEqual(sim.ai_decisions[-1]['selected_plan']['card_sources'], ['active_training'])

    def test_live_hand_plus_slot_and_slot_plus_slot_discard_each_card(self):
        for card_ids, sources in ((['FU-001', 'TR-019'], ['hand', 'active_training']),
                                  (['TR-019', 'GE-001'], ['active_training', 'equipped_gear'])):
            with self.subTest(sources=sources):
                sim, r = fixture()
                r['race_turn_number'] = 2
                r['hand'] = [card('FU-001')] if sources[0] == 'hand' else []
                r['active_training'] = [{'card': card('TR-019'), 'remaining_turns': None,
                                         'installed_turn': 0}]
                r['equipped_gear'] = [{'card': card('GE-001'), 'remaining_turns': None,
                                       'installed_turn': 0}] if 'equipped_gear' in sources else []
                sim.turn(r, {'movement_cards': card_ids, 'card_sources': sources})
                self.assertEqual([e['payload']['source'] for e in events(sim, 'PLAY')], sources)
                self.assertEqual(r['stats']['cards_played'], 2)
                self.assertTrue(set(card_ids).issubset({c['id'] for c in sim.discard}))
                self.assertFalse(r['active_training'])
                self.assertEqual(len(events(sim, 'SLOT_SACRIFICE')), sources.count('active_training') +
                                 sources.count('equipped_gear'))

    def test_preview_complete_remedy_releases_attached_card(self):
        from engine.simulate import make_condition
        sim, r = fixture()
        condition = make_condition(card('CO-010'))  # Dehydrated, nonpersistent.
        r['active_conditions'] = [condition]
        r['attached_gear'] = [{'card': card('GE-003'), 'condition_id': condition['id'],
                               'amount': 1, 'remaining_turns': None}]
        # Select the actual named remedy card rather than assuming an ID.
        remedy = next(c for c in CARDS.values() if c['title'] == 'Electrolytes')
        r['hand'] = [card(remedy['id'])]
        projected = sim.preview_preparation(r, {'action': 'fuel', 'card_id': remedy['id'],
                                                'choice': 'remedy'})
        self.assertEqual(projected['active_conditions'], [])
        self.assertEqual(projected['attached_gear'], [])
        self.assertEqual(len(r['attached_gear']), 1)


class Attachments(unittest.TestCase):
    def test_attachment_is_neither_hand_nor_slot_and_cannot_relocate(self):
        sim, r = fixture()
        condition = __import__('engine.simulate', fromlist=['make_condition']).make_condition(card('CO-005'))
        r['active_conditions'] = [condition]
        r['hand'] = [card('GE-003')]
        sim.resolve_treat_prepare(r, {'action': 'attach', 'card_id': 'GE-003',
                                      'condition_id': condition['id']})
        self.assertEqual(r['hand'], [])
        self.assertEqual(r['equipped_gear'], [])
        self.assertEqual([i['card']['id'] for i in r['attached_gear']], ['GE-003'])
        self.assertFalse(sim.movement_candidates(r, 2)[1:])
        with self.assertRaisesRegex(ValueError, 'cannot be reassigned'):
            sim.resolve_treat_prepare(r, {'action': 'relocate', 'card_id': 'GE-003'})

    def test_partial_remedy_keeps_attachment_full_remedy_discards(self):
        from engine.simulate import make_condition
        sim, r = fixture()
        condition = make_condition(card('CO-005'))
        r['active_conditions'] = [condition]
        sim.attach_gear(r, card('GE-003'), condition)
        sim.treat_condition(r, condition, 1)
        self.assertEqual(len(r['attached_gear']), 1)
        sim.treat_condition(r, condition, 10)
        self.assertEqual(len(r['attached_gear']), 1)  # Persistent Blister remains at zero.
        sim.discard_condition(r, condition, 'complete removal')
        self.assertEqual(len(r['attached_gear']), 0)
        self.assertIn('GE-003', [c['id'] for c in sim.discard])

    def test_station_removals_discard_attached_cards(self):
        from engine.simulate import make_condition
        for station, cid in (('Water', 'CO-010'), ('Aid', 'CO-013')):
            with self.subTest(station=station):
                sim, r = fixture()
                condition = make_condition(card(cid))
                r['active_conditions'] = [condition]
                r['attached_gear'] = [{'card': card('GE-003'), 'condition_id': cid,
                                       'amount': 1, 'remaining_turns': None}]
                sim.station_remedy(r, condition, station)
                self.assertEqual(r['attached_gear'], [])
                self.assertIn('GE-003', [c['id'] for c in sim.discard])


if __name__ == '__main__':
    unittest.main()
