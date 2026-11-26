"""Race Day Forecast playtest option: weather Energy loss at Water stations, Gear and Pack protection."""
import copy
import unittest

from engine.simulate import Sim
from engine.simulate import make_condition
from tests.test_v14_candidate import CFG, ROOT, card


def fixture(forecast):
    cfg = copy.deepcopy(CFG)
    cfg.update(player_count=1, forecast=forecast)
    sim = Sim(ROOT, cfg)
    sim.build_course()
    sim.runners = [sim.new_runner(0, 'Balanced', [])]
    sim.draw, sim.discard = [], []
    runner = sim.runners[0]
    runner['energy'] = 10
    return sim, runner


class Forecast(unittest.TestCase):
    def test_no_forecast_by_default(self):
        cfg = copy.deepcopy(CFG)
        self.assertIsNone(Sim(ROOT, cfg).forecast)

    def test_weather_costs_energy_at_water(self):
        sim, r = fixture('FC-04')
        sim.resolve_milestones(r, 15, 16)  # crosses mile 4 Water
        self.assertEqual(r['energy'], 9)

    def test_matching_gear_protects(self):
        sim, r = fixture('FC-04')
        sim.equip_gear(r, card('GE-015'))  # Singlet: Heat
        sim.resolve_milestones(r, 15, 16)
        self.assertEqual(r['energy'], 10)
        event = [e for e in sim.events if e['type'] == 'FORECAST_WEATHER'][-1]
        self.assertEqual(event['payload']['protected_by'], 'Singlet')

    def test_glare_shades_block_sun(self):
        sim, r = fixture('FC-03')
        sim.equip_gear(r, card('GE-010'))
        sim.resolve_milestones(r, 15, 16)
        self.assertEqual(r['energy'], 10)

    def test_mile_window(self):
        sim, r = fixture('FC-05')  # Heat from mile 13
        sim.resolve_milestones(r, 47, 48)  # mile 12 Water
        self.assertEqual(r['energy'], 10)
        sim.resolve_milestones(r, 63, 64)  # mile 16 Water
        self.assertEqual(r['energy'], 9)

    def test_pack_shelters_from_wind(self):
        sim, r = fixture('FC-08')
        r['pack_state'] = 'PACK-1'
        sim.resolve_milestones(r, 15, 16)
        self.assertEqual(r['energy'], 10)

    def test_severity_bonus_on_draw(self):
        sim, r = fixture('FC-06')  # Cold Chills +1
        sim.draw = [card('TR-001'), card('CO-011')]
        sim.draw_one(r)
        chills = next(c for c in r['active_conditions'] if c['title'] == 'Cold Chills')
        self.assertEqual(chills['current_severity'], make_condition(card('CO-011'))['current_severity'] + 1)


if __name__ == '__main__':
    unittest.main()
