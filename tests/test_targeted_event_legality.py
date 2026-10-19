"""Target-required Event Effects must be legal in preview and live resolution."""
import copy
import json
import unittest
from pathlib import Path

from engine.simulate import Sim


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'simulation/config.json').read_text())
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
SIDES = {c['id']: c for c in json.loads((ROOT / 'data/course_cards.json').read_text())}


def fixture(count=2):
    sim = Sim(ROOT, copy.deepcopy(CONFIG))
    sim.course = [dict(copy.deepcopy(SIDES['C-22-B']), mile=1)]
    sim.runners = [sim.new_runner(i, 'Balanced', []) for i in range(count)]
    sim.draw = []
    sim.discard = []
    return sim


def modes(sim, source, card_id):
    source['hand'] = [copy.deepcopy(CARDS[card_id])]
    return {card['use_mode'] for pair in sim.movement_candidates(source, 2)
            for card in pair if card['id'] == card_id}


class TargetedEventLegality(unittest.TestCase):
    def test_crowd_support_active_target_and_preview_copy(self):
        sim = fixture(2)
        source, target = sim.runners
        self.assertEqual(modes(sim, source, 'EV-015'), {'MOVEMENT', 'EFFECT'})
        self.assertEqual(sim.eligible_event_target(copy.deepcopy(source), 'EV-015')['player_id'],
                         target['player_id'])
        self.assertIn('EFFECT', modes(sim, copy.deepcopy(source), 'EV-015'))

    def test_crowd_support_all_finished_ai_uses_movement_without_exception(self):
        sim = fixture(8)
        source = sim.runners[-1]  # P8, the only active runner in the failed round.
        for other in sim.runners[:-1]:
            other['finished'] = True
            other['race_status'] = 'FINISHED'
        self.assertEqual(modes(sim, source, 'EV-015'), {'MOVEMENT'})
        plan = sim.choose_turn_plan(source)
        self.assertNotIn(('EV-015', 'EFFECT'), zip(plan['movement_cards'], plan['card_modes']))
        sim.start_round({'P8': 'Easy'})
        sim.turn(source)
        plays = [e['payload'] for e in sim.events if e['type'] == 'PLAY']
        self.assertEqual([(p['card']['id'], p['mode']) for p in plays], [('EV-015', 'MOVEMENT')])

    def test_crowd_support_all_dnf(self):
        sim = fixture(3)
        for other in sim.runners[1:]:
            other['dnf'] = True
            other['race_status'] = 'DNF'
        self.assertEqual(modes(sim, sim.runners[0], 'EV-015'), {'MOVEMENT'})

    def test_crowd_support_mixed_finished_and_dnf(self):
        sim = fixture(3)
        sim.runners[1]['finished'] = True
        sim.runners[2]['dnf'] = True
        self.assertEqual(modes(sim, sim.runners[0], 'EV-015'), {'MOVEMENT'})

    def test_exactly_one_active_target(self):
        sim = fixture(4)
        sim.runners[1]['finished'] = True
        sim.runners[2]['dnf'] = True
        source = sim.runners[0]
        self.assertEqual(sim.eligible_event_target(copy.deepcopy(source), 'EV-015')['player_id'], 'P4')
        self.assertIn('EFFECT', modes(sim, source, 'EV-015'))

    def test_all_target_required_inventory_is_filtered_in_preview(self):
        sim = fixture(2)
        source, target = sim.runners
        for event_id in sorted(sim_target_ids()):
            with self.subTest(event=event_id):
                if event_id == 'EV-018':
                    sim.round_pack_snapshot = {'P1': ['P2'], 'P2': ['P1']}
                self.assertIn('EFFECT', modes(sim, copy.deepcopy(source), event_id))
                target['finished'] = True
                self.assertEqual(modes(sim, copy.deepcopy(source), event_id), {'MOVEMENT'})
                target['finished'] = False

    def test_high_five_requires_active_pack_partner(self):
        sim = fixture(2)
        source, target = sim.runners
        self.assertIn('EFFECT', modes(sim, source, 'EV-018'))  # Solo: any active other runner.
        sim.round_pack_snapshot = {'P1': ['P2']}
        self.assertIn('EFFECT', modes(sim, source, 'EV-018'))
        target['dnf'] = True
        self.assertEqual(modes(sim, source, 'EV-018'), {'MOVEMENT'})

    def test_high_five_solo_chooses_active_other_runner(self):
        sim = fixture(2)
        source, target = sim.runners
        source['energy'] = target['energy'] = 4
        source['hand'] = [copy.deepcopy(CARDS['EV-018'])]
        sim.start_round({'P1': 'Easy', 'P2': 'Race'})
        self.assertEqual(sim.round_pack_snapshot['P1'], [])
        sim.turn(source, {'movement_cards': ['EV-018'], 'card_modes': ['EFFECT']})
        self.assertEqual((source['energy'], target['energy']), (5, 5))

    def test_target_lock_filters_negative_effect_but_not_movement(self):
        sim = fixture(2)
        source, target = sim.runners
        self.assertIn('EFFECT', modes(sim, source, 'EV-001'))
        target['staged_events'] = [{'card': copy.deepcopy(CARDS['EV-002']),
                                    'target': 'P2', 'target_lock': True}]
        self.assertEqual(modes(sim, source, 'EV-001'), {'MOVEMENT'})

    def test_ai_candidate_generation_never_scores_no_target_effect(self):
        sim = fixture(2)
        source, target = sim.runners
        target['finished'] = True
        source['hand'] = [copy.deepcopy(CARDS['EV-015'])]
        capture = {}
        sim.choose_turn_plan(source, capture)
        self.assertTrue(capture['candidates'])
        self.assertFalse(any('EFFECT' in plan['card_modes'] for plan in capture['candidates']))

    def test_resolver_defends_direct_illegal_invocation_without_state_change(self):
        sim = fixture(2)
        source, target = sim.runners
        target['finished'] = True
        before = copy.deepcopy((source, target, sim.events))
        with self.assertRaisesRegex(ValueError, 'requires another Runner'):
            sim.resolve_event_play(source, copy.deepcopy(CARDS['EV-015']))
        self.assertEqual((source, target, sim.events), before)


def sim_target_ids():
    from engine.simulate import TARGET_REQUIRED_EVENTS
    return TARGET_REQUIRED_EVENTS


if __name__ == '__main__':
    unittest.main()
