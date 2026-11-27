"""Weather Gear variant: slotted weather Gear also prevents a matching Condition (data-driven)."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine.simulate import Sim
from tests.test_v14_candidate import CFG, ROOT, card

VARIANT = 'simulation/variants/race_cards-weather-gear.json'


def variant_fixture():
    subprocess.run([sys.executable, str(Path(ROOT) / 'simulation/variants/build_weather_gear.py')],
                   check=True, capture_output=True)
    cfg = copy.deepcopy(CFG)
    cfg.update(player_count=1, race_cards_path=VARIANT)
    sim = Sim(ROOT, cfg)
    sim.build_course()
    sim.runners = [sim.new_runner(0, 'Balanced', [])]
    sim.draw, sim.discard = [], []
    cards = {c['id']: c for c in json.loads((Path(ROOT) / VARIANT).read_text(encoding='utf-8'))}
    return sim, sim.runners[0], lambda cid: copy.deepcopy(cards[cid])


class WeatherGearPrevention(unittest.TestCase):
    def test_variant_gear_prevents_matching_condition(self):
        for gear, condition in (('GE-015', 'CO-016'), ('GE-006', 'CO-016'),
                                ('GE-008', 'CO-011'), ('GE-013', 'CO-011')):
            with self.subTest(gear=gear, condition=condition):
                sim, r, vcard = variant_fixture()
                sim.equip_gear(r, vcard(gear))
                sim.draw = [vcard('TR-001'), vcard(condition)]
                sim.draw_one(r)
                self.assertEqual(r['active_conditions'], [])
                prevent = [e for e in sim.events if e['type'] == 'CONDITION_PREVENT']
                self.assertEqual(prevent[-1]['payload']['condition'], condition)

    def test_printed_cards_do_not_prevent(self):
        from tests.test_v14_candidate import fixture
        sim, r = fixture()
        sim.equip_gear(r, card('GE-015'))
        sim.draw = [card('TR-001'), card('CO-016')]
        sim.draw_one(r)
        self.assertEqual([c['title'] for c in r['active_conditions']], ['Heat Exhaustion'])


if __name__ == '__main__':
    unittest.main()
