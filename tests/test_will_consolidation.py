"""Bounded Will accounting and closed Rules Review rulings."""

import copy
import json
import unittest
from pathlib import Path

from engine import simulate as m
from engine.ai_rationale import describe_decision

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(energy, pace, ids, position=0):
    cfg = copy.deepcopy(CFG)
    cfg['seed'] = 20260930
    sim = m.Sim(ROOT, cfg)
    sim.build_course()
    runner = sim.new_runner(0, 'Balanced', [card(cid) for cid in ids])
    sim.runners = [runner]
    sim.draw = []
    sim.round = 1
    runner.update(energy=energy, pace=pace, quarter_mile_space=position)
    return sim, runner


def events(sim, kind):
    return [e['payload'] for e in sim.events if e['type'] == kind]


class WillConsolidation(unittest.TestCase):
    def scripted(self, energy, pace, ids, position=0, **kwargs):
        sim, runner = fixture(energy, pace, ids, position)
        runner.update(kwargs)
        sim.turn(runner, {'movement_cards': list(ids)})
        self.assertTrue(events(sim, 'TURN_END'))
        self.assertGreaterEqual(runner['energy'], 0)
        self.assertLessEqual(runner['energy'], 15)
        return sim, runner

    def test_pace_only_shortfall(self):
        sim, r = self.scripted(0, 'Push', ('FU-001',))  # Effort 3 costs zero
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 2)
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['paid'], 0)
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['covered_by_will'], 0)
        self.assertEqual((r['energy'], r['will_available']), (0, False))

    def test_movement_only_shortfall(self):
        sim, r = self.scripted(0, 'Easy', ('TR-001',))
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 2)
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['covered_by_will'], 2)
        self.assertEqual((r['energy'], r['will_available']), (0, False))

    def test_combined_shortfall_and_multiple_card_costs(self):
        sim, r = self.scripted(1, 'Push', ('TR-001',))
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 3)
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['paid'], 1)
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['covered_by_will'], 2)
        self.assertEqual(r['stats']['energy_spent'], 1)
        sim2, r2 = self.scripted(1, 'Easy', ('TR-001', 'FU-005'))
        pays = events(sim2, 'MOVEMENT_ENERGY_PAYMENT')
        self.assertEqual([p['cost'] for p in pays], [2, 1])
        self.assertEqual([p['paid'] for p in pays], [1, 0])
        self.assertEqual([p['covered_by_will'] for p in pays], [1, 1])
        self.assertEqual(events(sim2, 'WILL_USE')[0]['shortfall'], 2)
        self.assertEqual(r2['energy'], 0)

    def test_exact_stored_payment_and_spent_will(self):
        sim, r = self.scripted(3, 'Steady', ('TR-001',))
        self.assertFalse(events(sim, 'WILL_USE'))
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['paid'], 1)
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['paid'], 2)
        self.assertEqual((r['energy'], r['will_available']), (0, True))
        sim2, r2 = fixture(0, 'Easy', ('TR-001',))
        r2['will_available'] = False
        with self.assertRaisesRegex(ValueError, 'Movement Energy unavailable'):
            sim2.turn(r2, {'movement_cards': ['TR-001']})

    def test_pack_training_gear_apply_before_shortfall(self):
        sim, r = fixture(0, 'Race', ('TR-001',))
        sim.course[0]['surface'] = 'Asphalt'
        r['pack_state'] = 'PACK-R1-1'
        r['active_training'] = [{'card': card('TR-001'), 'remaining_turns': None}]
        r['equipped_gear'] = [{'card': card('GE-002'), 'remaining_turns': None}]
        # Long Run preserves Race Pace; Running Shoes gains one stored Energy on Asphalt.
        r['active_training'][0]['card'] = card('TR-002')
        sim.turn(r, {'movement_cards': ['TR-001']})
        self.assertEqual(events(sim, 'PACE_PAYMENT')[0]['final'], 0)
        self.assertIn('Pack', events(sim, 'PACE_PAYMENT')[0]['preservation_sources'])
        self.assertIn('Long Run', events(sim, 'PACE_PAYMENT')[0]['preservation_sources'])
        self.assertEqual(events(sim, 'WILL_USE')[0]['shortfall'], 1)
        self.assertEqual(events(sim, 'MOVEMENT_ENERGY_PAYMENT')[0]['paid'], 1)
        self.assertEqual((r['energy'], r['will_available']), (0, False))

    def test_final_segment_will_and_repeatability(self):
        outputs = []
        for _ in range(2):
            sim, r = fixture(0, 'Easy', ('TR-001',), position=103)
            plan = sim.choose_turn_plan(r)
            sim.turn(r)
            sim.end_round()
            self.assertEqual((r['energy'], r['will_available'], r['finish_order']), (0, False, 1))
            outputs.append((plan, [(e['type'], e['payload']) for e in sim.events],
                            r['quarter_mile_space'], r['energy'], r['will_available']))
        self.assertEqual(outputs[0], outputs[1])

    def test_pace_movement_and_combined_replay_with_rationale(self):
        for energy, pace, ids in ((0, 'Push', ('FU-001',)),
                                  (0, 'Easy', ('TR-001',)),
                                  (1, 'Push', ('TR-001',))):
            outputs = []
            for _ in range(2):
                sim, r = fixture(energy, pace, ids)
                capture = {}
                plan = sim.choose_turn_plan(r, capture)
                rationale = describe_decision(sim, r, capture)
                sim.turn(r, {'movement_cards': list(ids)})
                outputs.append((plan, rationale, r['quarter_mile_space'], r['energy'],
                                r['will_available'], [(e['type'], e['payload']) for e in sim.events]))
            self.assertEqual(outputs[0], outputs[1])

    def test_pack_fixed_until_next_round_and_nearest_leader(self):
        sim, _ = fixture(15, 'Easy', ())
        sim.runners = [sim.new_runner(i, 'Balanced', []) for i in range(4)]
        for runner, pos in zip(sim.runners, (8, 7, 6, 3)):
            runner['quarter_mile_space'] = pos
        sim.start_round({r['player_id']: 'Steady' for r in sim.runners})
        self.assertEqual([r['pack_leader'] for r in sim.runners[:3]], ['P1'] * 3)
        self.assertIsNone(sim.runners[3]['pack_state'])
        original = sim.runners[1]['pack_state']
        sim.runners[1]['quarter_mile_space'] = 0
        sim.end_round()
        self.assertEqual(sim.runners[1]['pack_state'], original)
        sim.start_round({r['player_id']: 'Steady' for r in sim.runners})
        self.assertIsNone(sim.runners[1]['pack_state'])
        self.assertTrue(any(e['type'] == 'PACK_EXIT' and e['player_id'] == 'P2' for e in sim.events))

    def test_electrolytes_salt_tabs_exclusive_branches(self):
        for cid, condition_id in (('FU-016', 'CO-010'), ('FU-019', 'CO-001')):
            with self.subTest(card=cid):
                sim, r = fixture(5, 'Easy', (cid,))
                self.assertTrue(sim.legal_treat_prepare(r, {'card_id': cid, 'action': 'fuel',
                                                           'choice': 'energy'}))
                self.assertFalse(sim.legal_treat_prepare(r, {'card_id': cid, 'action': 'fuel',
                                                            'choice': 'remedy'}))
                r['active_conditions'] = [m.make_condition(card(condition_id))]
                self.assertTrue(sim.legal_treat_prepare(r, {'card_id': cid, 'action': 'fuel',
                                                           'choice': 'remedy'}))
                sim.use_fuel(r, card(cid), 'remedy')
                self.assertEqual(r['energy'], 5)
                self.assertEqual(events(sim, 'FUEL_USE')[-1]['recovery'], 0)

    def test_gear_relocation_occupies_action_but_allows_two_card_plays(self):
        sim, r = fixture(15, 'Easy', ('TR-001', 'FU-005'))
        r['equipped_gear'] = [{'card': card('GE-003'), 'remaining_turns': None}]
        r['active_conditions'] = [m.make_condition(card('CO-005'))]
        sim.turn(r, {'treat_prepare': {'action': 'relocate', 'card_id': 'GE-003',
                                      'condition_id': 'CO-005'},
                     'movement_cards': ['TR-001', 'FU-005']})
        self.assertEqual(len(events(sim, 'GEAR_RELOCATE')), 1)
        self.assertEqual(len(events(sim, 'PLAY')), 2)
        self.assertEqual(events(sim, 'GEAR_RELOCATE')[0]['card_play_budget'], 0)
        self.assertEqual(r['stats']['treat_prepare_actions'], 1)

    def test_exact_course_endpoint_needs_later_positive_movement(self):
        sim, r = fixture(0, 'Easy', ('EV-027',), position=103)
        sim.turn(r, {'movement_cards': [], 'card_modes': []})
        self.assertFalse(r['finish_pending'])
        r['quarter_mile_space'] = 104
        sim.round = 2
        r['hand'] = [card('TR-001')]
        sim.turn(r, {'movement_cards': ['TR-001']})
        self.assertTrue(r['finish_pending'])

    def test_half_marathon_exact_endpoint_needs_extra_unit(self):
        sim, r = fixture(2, 'Easy', ('TR-001',), position=52)
        sim.cfg['race_format'] = 'half'
        sim.course = sim.course[:13]
        sim.course[-1]['difficulty'] = 1
        sim.turn(r, {'movement_cards': []})
        self.assertFalse(r['finish_pending'])
        sim.round = 2
        sim.turn(r, {'movement_cards': ['TR-001']})
        self.assertTrue(r['finish_pending'])

    def test_canonical_rule_register_and_will_descriptor(self):
        canonical = (ROOT / 'DRG-Canonical-Playtest-Rules.md').read_text()
        review = (ROOT / 'DRG-Rules-Review.md').read_text()
        config = json.loads((ROOT / 'simulation/config.json').read_text())
        for marker in ('exact remaining shortfall', 'nearest leader',
                       'Relocating already-played Gear', 'Remedy Dehydrated',
                       'Course endpoint with no positive legal Movement left'):
            self.assertIn(marker, canonical)
        for identifier in ('RR-11', 'RR-13', 'RR-16', 'RR-17'):
            self.assertIn(identifier, review.split('## Closed / superseded register')[1])
        self.assertIn('Movement-card costs', config['will_resolution'])


if __name__ == '__main__':
    unittest.main()
