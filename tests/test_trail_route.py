import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('trail_route_sim', ROOT / 'engine/simulate.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
CONFIG = json.loads((ROOT / 'simulation/config.json').read_text())
SIDES = {side['id']: side for side in json.loads((ROOT / 'data/course_cards.json').read_text())}
CARDS = {card['id']: card for card in json.loads((ROOT / 'data/race_cards.json').read_text())}


def fixture(*side_ids):
    sim = engine.Sim(ROOT, copy.deepcopy(CONFIG))
    sim.course = [dict(copy.deepcopy(SIDES[side_id]), mile=index + 1)
                  for index, side_id in enumerate(side_ids)]
    sim.runners = [sim.new_runner(0, 'Trail fixture', [])]
    sim.draw = []
    sim.discard = []
    return sim, sim.runners[0]


def installed(card_id):
    return {'card': copy.deepcopy(CARDS[card_id]), 'remaining_turns': None}


def move_payload(sim):
    return next(event['payload'] for event in reversed(sim.events) if event['type'] == 'MOVE')


class TrailRouteRegression(unittest.TestCase):
    def test_canonical_course_represents_trail_as_route(self):
        sides = list(SIDES.values())
        self.assertEqual(sum(side['route'] == 'Trail' for side in sides), 10)
        self.assertNotIn('Dirt Trail', {side['surface'] for side in sides})
        self.assertEqual({side['surface'] for side in sides if side['route'] == 'Trail'},
                         {'Dirt', 'Grass', 'Gravel'})

    def test_live_training_install_activates_on_grass_trail(self):
        sim, runner = fixture('C-12-A', 'C-11-A')
        runner['hand'] = [copy.deepcopy(CARDS['TR-015']), copy.deepcopy(CARDS['TR-001'])]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'treat_prepare': {'card_id': 'TR-015', 'action': 'training'},
                          'movement_cards': ['TR-001']})
        self.assertEqual(move_payload(sim)['installed_effort_bonus'], 1)
        self.assertEqual(move_payload(sim)['installed_effort_sources'], ['Trail Training'])

    def test_live_shoes_equip_activates_on_gravel_trail(self):
        sim, runner = fixture('C-26-B', 'C-11-A')
        runner['hand'] = [copy.deepcopy(CARDS['GE-005']), copy.deepcopy(CARDS['TR-001'])]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'treat_prepare': {'card_id': 'GE-005', 'action': 'gear'},
                          'movement_cards': ['TR-001']})
        self.assertEqual(move_payload(sim)['installed_effort_bonus'], 2)
        self.assertEqual(move_payload(sim)['installed_effort_sources'], ['Trail Shoes'])

    def test_trail_effects_follow_route_not_surface(self):
        for side_id in ('C-08-B', 'C-11-B', 'C-26-B'):
            with self.subTest(side_id=side_id):
                sim, runner = fixture(side_id)
                runner['active_training'] = [installed('TR-015')]
                runner['equipped_gear'] = [installed('GE-005')]
                self.assertEqual(sim.movement_effort_bonus(runner, sim.course[0]),
                                 (3, ['Trail Training', 'Trail Shoes']))
        sim, runner = fixture('C-11-A', 'C-12-B', 'C-10-A')
        runner['active_training'] = [installed('TR-015')]
        runner['equipped_gear'] = [installed('GE-005')]
        for side in sim.course:
            self.assertEqual(sim.movement_effort_bonus(runner, side), (0, []))
        self.assertNotIn("'Dirt Trail'", (ROOT / 'engine/simulate.py').read_text())

    def test_route_transition_changes_bonus_on_next_movement(self):
        for card_id, category, bonus in (('TR-015', 'active_training', 1),
                                         ('GE-005', 'equipped_gear', 2)):
            for first, second in (('C-11-A', 'C-12-A'), ('C-12-A', 'C-11-A')):
                with self.subTest(card=card_id, first=first, second=second):
                    sim, runner = fixture(first, second)
                    runner[category] = [installed(card_id)]
                    runner['quarter_mile_space'] = 3
                    runner['hand'] = [copy.deepcopy(CARDS['TR-001']),
                                      copy.deepcopy(CARDS['TR-002'])]
                    sim.start_round({'P1': 'Easy'})
                    sim.turn(runner, {'treat_prepare': None, 'movement_cards': ['TR-001']})
                    first_move = move_payload(sim)
                    self.assertGreaterEqual(runner['quarter_mile_space'], 4)
                    self.assertEqual(first_move['installed_effort_bonus'],
                                     bonus if SIDES[first]['route'] == 'Trail' else 0)
                    self.assertTrue(any(event['type'] == 'MOVE_BOUNDARY' for event in sim.events))
                    sim.end_round()
                    sim.start_round({'P1': 'Easy'})
                    sim.turn(runner, {'treat_prepare': None, 'movement_cards': ['TR-002']})
                    self.assertEqual(move_payload(sim)['installed_effort_bonus'],
                                     bonus if SIDES[second]['route'] == 'Trail' else 0)

    def test_unrelated_surface_bonuses_still_use_surface(self):
        sim, runner = fixture('C-01-A', 'C-10-A')
        runner['equipped_gear'] = [installed('GE-001')]
        self.assertEqual(sim.movement_effort_bonus(runner, sim.course[0])[0], 1)
        self.assertEqual(sim.movement_effort_bonus(runner, sim.course[1])[0], 0)
        concrete, runner = fixture('C-05-A', 'C-01-A')
        runner['equipped_gear'] = [installed('GE-020')]
        self.assertEqual(concrete.movement_effort_bonus(runner, concrete.course[0])[0], 1)
        self.assertEqual(concrete.movement_effort_bonus(runner, concrete.course[1])[0], 0)


if __name__ == '__main__':
    unittest.main()
