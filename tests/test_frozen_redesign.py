"""Bounded live-path checks for the frozen 108-card redesign; no marathon run."""
import copy
import json
import unittest
from collections import Counter
from pathlib import Path
from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text(encoding='utf-8'))}
CFG = json.loads((ROOT / 'simulation/config.json').read_text(encoding='utf-8'))


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture(count=1):
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.runners = [sim.new_runner(i, 'Balanced', []) for i in range(count)]
    sim.draw = []
    return sim, sim.runners[0]


def installed(cid):
    return {'card': card(cid), 'remaining_turns': m.GEAR_DURATION.get(CARDS[cid]['title'])}


class FrozenRedesign(unittest.TestCase):
    def test_inventory_swaps_icons_and_machine_fields(self):
        self.assertEqual(Counter(c['family'] for c in CARDS.values()),
                         Counter(Training=20, Gear=20, Fuel=22, Event=30, Condition=16))
        self.assertEqual((CARDS['GE-013']['title'], CARDS['EV-010']['title'],
                          CARDS['CO-011']['title'], CARDS['CO-013']['title']),
                         ('Running Jacket', 'Cold Snap', 'Cold Chills', 'Gashed Knee'))
        self.assertEqual(sum(c['title'] == 'Dehydrated' for c in CARDS.values()), 1)
        self.assertEqual(sum(c['title'] == 'Hydration Belt' for c in CARDS.values()), 1)
        for c in CARDS.values():
            self.assertIn('effect_components', c)
            if c['family'] == 'Condition':
                self.assertIsNone(c['effort'])
                self.assertIsNone(c['movement_energy_cost'])
                self.assertIsNone(c['movement_energy_icon'])
                self.assertIsInstance(c['severity'], int)
            else:
                self.assertEqual(c['movement_energy_cost'], m.movement_energy_cost(c))
                self.assertEqual(c['movement_energy_icon'], '⚡' * m.movement_energy_cost(c))

    def test_band_boundaries_and_two_live_card_payments(self):
        for effort, expected in ((1, 0), (3, 0), (4, 1), (6, 1), (7, 2), (10, 2)):
            self.assertEqual(m.movement_energy_cost({'effort': effort}), expected)
        sim, r = fixture()
        r['energy'] = 9
        r['hand'] = [card('FU-002'), card('EV-021')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'movement_cards': ['FU-002', 'EV-021']})
        payments = [e['payload']['cost'] for e in sim.events if e['type'] == 'MOVEMENT_ENERGY_PAYMENT']
        self.assertEqual(payments, [1, 2])
        self.assertEqual(r['energy'], 6)
        self.assertEqual([e['payload']['mode'] for e in sim.events if e['type'] == 'PLAY'],
                         ['MOVEMENT', 'MOVEMENT'])
        self.assertFalse(any(e['type'] == 'ENERGY_CHANGE' and e['payload']['source'] == 'Second Wind'
                             for e in sim.events))

    def test_effect_mode_zero_effort_and_no_card_energy(self):
        sim, r = fixture()
        r['energy'] = 5
        r['hand'] = [card('EV-021'), card('FU-001')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'movement_cards': ['EV-021', 'FU-001'],
                     'card_modes': ['EFFECT', 'MOVEMENT']})
        move = next(e['payload'] for e in sim.events if e['type'] == 'MOVE')
        self.assertEqual(move['total_effort'], 3)
        self.assertEqual(sum(e['payload']['cost'] for e in sim.events
                             if e['type'] == 'MOVEMENT_ENERGY_PAYMENT'), 0)
        self.assertEqual(r['energy'], 8)

    def test_will_qualifies_card_but_spent_will_rejects_unaffordable_card(self):
        sim, r = fixture()
        r['energy'] = 0
        r['hand'] = [card('TR-001'), card('EV-029')]
        sim.start_round({'P1': 'Easy'})
        self.assertIn('TR-001', sim.choose_turn_plan(r)['movement_cards'])
        sim.turn(r, {'movement_cards': ['TR-001']})
        self.assertFalse(r['will_available'])
        self.assertEqual(r['energy'], 0)
        sim, r = fixture()
        r['energy'] = 0
        r['will_available'] = False
        r['hand'] = [card('TR-001'), card('EV-029')]
        sim.start_round({'P1': 'Easy'})
        self.assertEqual(sim.choose_turn_plan(r)['movement_cards'], ['EV-029'])
        with self.assertRaisesRegex(ValueError, 'Movement Energy unavailable'):
            sim.turn(r, {'movement_cards': ['TR-001']})

    def test_fuel_two_energy_and_alternative_severity(self):
        sim, r = fixture()
        r['energy'] = 5
        r['hand'] = [card('FU-006'), card('FU-010')]
        r['active_conditions'] = [m.make_condition(card('CO-003')),
                                  m.make_condition(card('CO-016'))]
        sim.resolve_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-006', 'choice': 'severity'})
        self.assertEqual((r['energy'], r['active_conditions'][0]['current_severity']), (5, 1))
        sim.resolve_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-010', 'choice': 'energy'})
        self.assertEqual(r['energy'], 7)
        r['active_conditions'].append(m.make_condition(card('CO-012')))
        r['hand'] = [card('FU-002')]
        self.assertFalse(sim.legal_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-002', 'choice': 'energy'}))
        r['energy'] = 5
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'movement_cards': ['FU-002']})
        self.assertTrue(any(e['type'] == 'PLAY' and e['payload']['mode'] == 'MOVEMENT'
                            for e in sim.events))

    def test_conditions_direct_difficulty_caps_and_aid(self):
        self.assertEqual(m.condition_effects(m.make_condition(card('CO-004')), 'Race')['direct_movement'], -1)
        self.assertEqual(m.condition_effects(m.make_condition(card('CO-013')), 'Easy')['direct_movement'], -1)
        self.assertEqual(m.condition_effects(m.make_condition(card('CO-009')), surface='Concrete')['difficulty_penalty'], 2)
        self.assertEqual(m.condition_effects(m.make_condition(card('CO-011')), 'Push')['extra_energy'], 1)
        twist = m.make_condition(card('CO-015'))
        m.apply_remedy(twist, 'Aid')
        self.assertEqual(twist['current_severity'], 4)
        heat = m.make_condition(card('CO-016'))
        m.apply_remedy(heat, 'Aid')
        self.assertEqual(heat['current_severity'], 4)
        nausea = m.make_condition(card('CO-012'))
        self.assertIsNone(m.apply_remedy(nausea, 'Aid'))

    def test_gut_modifiers_and_weather_swaps(self):
        check = m.gut_check([], ['Strength Training', 'Mental Toughness'], ['Pace Band'])
        self.assertEqual(check['modifiers'], 6)
        self.assertEqual([entry['value'] for entry in check['modifier_sources']], [1, 3, 2])
        self.assertEqual(m.gut_check([], ['Strength Training', 'Strength Training'])['modifiers'], 2)
        sim, r = fixture()
        sim.round = 1
        r['energy'] = 5
        r['equipped_gear'] = [installed('GE-008'), installed('GE-013')]
        sim.global_events = [{'card': card('EV-006'), 'activate_round': 2, 'source': 'P1'},
                             {'card': card('EV-010'), 'activate_round': 2, 'source': 'P1'}]
        sim.start_round({'P1': 'Easy'})
        p = sim.pace_cost(r, 'Easy')
        self.assertEqual(p['final'], 0)
        self.assertEqual(r['energy'], 5)
        self.assertEqual([e['payload']['actual_loss'] for e in sim.events
                          if e['type'] == 'GLOBAL_WEATHER'], [0, 0])

    def test_installed_energy_route_duration_and_preview_match(self):
        sim, r = fixture()
        sim.course[0]['route'] = 'Trail'
        r['active_training'] = [installed('TR-015')]
        r['equipped_gear'] = [installed('GE-005'), installed('GE-016')]
        r['energy'] = 4
        sim.round = 1
        self.assertEqual(sum(v for _, v in sim.installed_energy(r)), 4)
        projected = sim.preview_payment(r)
        sim.apply_installed_energy(r)
        self.assertEqual(r['energy'], projected['energy'])
        self.assertEqual(r['energy'], 8)
        sim.expire_temporary(r)
        self.assertEqual(r['equipped_gear'][-1]['remaining_turns'], 1)
        sim.expire_temporary(r)
        self.assertNotIn('GE-016', [i['card']['id'] for i in r['equipped_gear']])

    def test_event_effect_direct_and_no_effect_on_movement_use(self):
        sim, r = fixture()
        r['hand'] = [card('EV-023'), card('FU-001')]
        r['energy'] = 9
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'movement_cards': ['FU-001', 'EV-023'], 'card_modes': ['MOVEMENT', 'EFFECT']})
        move = next(e['payload'] for e in sim.events if e['type'] == 'MOVE')
        self.assertEqual(move['total_effort'], 3)
        self.assertEqual(move['direct_requested'], 2)
        self.assertEqual(r['energy'], 9)

    def test_gps_watch_two_distinct_runner_turn_ticks_then_expiry(self):
        sim, r = fixture()
        r['energy'] = 4
        r['hand'] = [card('GE-016'), card('FU-001')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'treat_prepare': {'action': 'gear', 'card_id': 'GE-016'},
                     'movement_cards': ['FU-001']})
        self.assertEqual(r['energy'], 5)
        sim.end_round()
        r['hand'] = [card('FU-001')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'treat_prepare': None, 'movement_cards': ['FU-001']})
        self.assertEqual(r['energy'], 6)
        self.assertFalse(r['equipped_gear'])
        sim.end_round()
        r['hand'] = [card('FU-001')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'treat_prepare': None, 'movement_cards': ['FU-001']})
        self.assertEqual(r['energy'], 6)
        gains = [e for e in sim.events if e['type'] == 'ENERGY_CHANGE'
                 and e['payload']['source'] == 'Installed GE-016']
        self.assertEqual([e['payload']['delta'] for e in gains], [1, 1])
        self.assertEqual(len([e for e in sim.events if e['type'] == 'GPS_WATCH_TICK']), 2)

    def test_event_target_energy_direct_and_global_effects(self):
        sim, first = fixture(2)
        second = sim.runners[1]
        first['energy'], second['energy'] = 4, 4
        first['hand'] = [card('EV-015')]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(first, {'movement_cards': ['EV-015'], 'card_modes': ['EFFECT']})
        self.assertEqual((first['energy'], second['energy']), (5, 5))
        self.assertEqual(first['quarter_mile_space'], 0)  # E5 is ignored.

        sim, first = fixture(2)
        second = sim.runners[1]
        first['energy'], second['energy'] = 4, 4
        first['hand'] = [card('EV-019')]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(first, {'movement_cards': ['EV-019'], 'card_modes': ['EFFECT']})
        self.assertEqual(first['quarter_mile_space'], 1)
        self.assertEqual(second['staged_events'][0]['card']['id'], 'EV-019')
        sim.end_round()
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        second['hand'] = [card('FU-001')]
        sim.turn(second, {'movement_cards': ['FU-001']})
        self.assertEqual(next(e['payload']['direct_requested'] for e in sim.events
                              if e['type'] == 'MOVE' and e['player_id'] == 'P2'), 1)

        cold, r = fixture()
        r['energy'] = 4
        r['hand'] = [card('EV-010')]
        cold.start_round({'P1': 'Easy'})
        cold.turn(r, {'movement_cards': ['EV-010'], 'card_modes': ['EFFECT']})
        self.assertEqual(cold.global_events[0]['activate_round'], cold.round + 1)
        cold.end_round()
        cold.start_round({'P1': 'Easy'})
        self.assertEqual(r['energy'], 3)
        self.assertEqual(cold.pace_cost(r, 'Easy')['final'], 0)
        heat, actor = fixture(2)
        other = heat.runners[1]
        actor['energy'] = other['energy'] = 5
        actor['hand'] = [card('EV-006')]
        heat.start_round({'P1': 'Easy', 'P2': 'Easy'})
        heat.turn(actor, {'movement_cards': ['EV-006'], 'card_modes': ['EFFECT']})
        heat.end_round()
        heat.start_round({'P1': 'Easy', 'P2': 'Easy'})
        self.assertEqual((actor['energy'], other['energy']), (4, 5))

    def test_other_target_and_card_mode_remain_exclusive(self):
        sim, first = fixture(2)
        second = sim.runners[1]
        first['energy'] = second['energy'] = 6
        first['hand'] = [card('EV-011')]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(first, {'movement_cards': ['EV-011'], 'card_modes': ['EFFECT']})
        self.assertEqual(second['energy'], 5)
        self.assertFalse(second['staged_events'])
        self.assertEqual(first['energy'], 6)
        self.assertEqual(first['quarter_mile_space'], 0)
        self.assertFalse(any(e['type'] == 'MOVEMENT_ENERGY_PAYMENT' for e in sim.events))
        sim.end_round()
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        second['hand'] = [card('FU-001')]
        sim.turn(second, {'movement_cards': ['FU-001']})
        self.assertEqual(second['energy'], 5)  # The immediate choice is not charged again.
        forced, attacker = fixture(2)
        victim = forced.runners[1]
        victim['energy'] = 0
        attacker['hand'] = [card('EV-025')]
        forced.start_round({'P1': 'Easy', 'P2': 'Easy'})
        forced.turn(attacker, {'movement_cards': ['EV-025'], 'card_modes': ['EFFECT']})
        self.assertEqual(victim['staged_events'][0]['card']['id'], 'EV-025')
        forced.end_round()
        victim['hand'] = [card('FU-001')]
        forced.start_round({'P1': 'Easy', 'P2': 'Easy'})
        forced.turn(victim, {'movement_cards': ['FU-001']})
        self.assertEqual([e['payload']['direct_requested'] for e in forced.events
                          if e['type'] == 'MOVE' and e['player_id'] == 'P2'][-1], -1)

    def test_high_five_chooses_one_packmate_in_three_runner_pack(self):
        sim, actor = fixture(3)
        for runner in sim.runners:
            runner['energy'] = 5
        actor['hand'] = [card('EV-018')]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy', 'P3': 'Easy'})
        sim.turn(actor, {'movement_cards': ['EV-018'], 'card_modes': ['EFFECT']})
        self.assertEqual([runner['energy'] for runner in sim.runners], [6, 6, 5])
        self.assertEqual(next(e['payload']['beneficiaries'] for e in sim.events
                              if e['type'] == 'HIGH_FIVE'), ['P1', 'P2'])

    def test_weather_protection_and_direct_penalties_at_zero_severity(self):
        sim, r = fixture()
        r['energy'] = 5
        r['equipped_gear'] = [installed('GE-013')]
        sim.round = 1
        sim.global_events = [{'card': card('EV-010'), 'activate_round': 2, 'source': 'P1'}]
        sim.start_round({'P1': 'Easy'})
        self.assertEqual(sim.pace_cost(r, 'Easy')['final'], 0)
        self.assertEqual(r['energy'], 5)
        self.assertEqual(next(e['payload']['protected_by'] for e in sim.events
                              if e['type'] == 'GLOBAL_WEATHER'), 'Running Jacket')
        knee = m.make_condition(card('CO-013'))
        self.assertEqual(m.condition_effects(knee, 'Easy')['direct_movement'], -1)
        knee['current_severity'] = 0
        m.update_effective_severity(knee)
        self.assertEqual(m.condition_effects(knee, 'Easy')['direct_movement'], 0)

    def test_training_installation_reduces_one_active_condition_and_preview_matches(self):
        sim, r = fixture()
        r['active_conditions'] = [m.make_condition(card('CO-004')),
                                  m.make_condition(card('CO-003'))]
        r['hand'] = [card('TR-003')]
        plan = {'action': 'training', 'card_id': 'TR-003'}
        projected = sim.preview_preparation(r, plan)
        sim.resolve_treat_prepare(r, plan)
        self.assertEqual([(c['id'], c['current_severity']) for c in r['active_conditions']],
                         [('CO-004', 4), ('CO-003', 3)])
        self.assertEqual([(c['id'], c['current_severity']) for c in projected['active_conditions']],
                         [(c['id'], c['current_severity']) for c in r['active_conditions']])

    def test_hydration_belt_only_pays_at_water_and_preview_counts_crossing(self):
        sim, r = fixture()
        r['equipped_gear'] = [installed('GE-012')]
        r['energy'] = 5
        r['quarter_mile_space'] = 15
        r['pace'] = 'Easy'
        self.assertEqual(sim.installed_energy(r), [])
        r['hand'] = [card('TR-001'), card('EV-023')]
        sim.round = 1
        preview = sim.preview_movement(r, [{**item, 'use_mode': 'MOVEMENT'} for item in r['hand']])
        self.assertGreaterEqual(preview['to_space'], 16)
        self.assertEqual(preview['milestone_energy_gain'], 1)
        sim.turn(r, {'movement_cards': ['TR-001', 'EV-023']})
        self.assertEqual(len([e for e in sim.events if e['type'] == 'ENERGY_CHANGE'
                              and e['payload']['source'] == 'Hydration Belt at Water']), 1)

    def test_all_thirty_frozen_event_effect_modes_execute_in_bounded_live_turn(self):
        for index in range(1, 31):
            cid = f'EV-{index:03d}'
            with self.subTest(card=cid):
                sim, runner = fixture(2)
                runner['energy'] = sim.runners[1]['energy'] = 8
                runner['hand'] = [card(cid)]
                sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
                sim.turn(runner, {'movement_cards': [cid], 'card_modes': ['EFFECT']})
                play = next(e['payload'] for e in sim.events if e['type'] == 'PLAY')
                self.assertEqual((play['mode'], play['effect_active'],
                                  play['movement_energy_cost']), ('EFFECT', True, 0))
                self.assertEqual(runner['stats']['total_effort_used'], 0)

    def test_seeded_setup_and_one_round_remain_deterministic(self):
        cfg = copy.deepcopy(CFG)
        cfg.update(seed=424242, player_count=2)
        runs = []
        for _ in range(2):
            sim = m.Sim(ROOT, copy.deepcopy(cfg))
            sim.setup()
            sim.run_round()
            runs.append((sim.events, sim.ai_decisions, sim.draw, sim.discard))
        self.assertEqual(runs[0], runs[1])

    def test_future_visible_terrain_and_staged_weather_enter_setup_value(self):
        sim, r = fixture()
        r['energy'] = 5
        r['pace'] = 'Easy'
        r['hand'] = [card('GE-005'), card('FU-001')]
        sim.round = 1
        for side in sim.course[:6]:
            side['route'] = 'Trail'
        prepared = sim.preview_preparation(r, {'action': 'gear', 'card_id': 'GE-005'})
        self.assertEqual(sum(v for _, v in sim.energy_gains_on_side(prepared, sim.course[1])), 2)
        self.assertEqual(sum(v for _, v in sim.energy_gains_on_side(r, sim.course[1])), 0)
        r['hand'] = [card('GE-013'), card('FU-001')]
        prep = {'action': 'gear', 'card_id': 'GE-013'}
        paid = sim.preview_payment(sim.preview_preparation(r, prep))
        movement_cards = [{**card('FU-001'), 'use_mode': 'MOVEMENT'}]
        projection = sim.preview_movement(paid, movement_cards)
        no_weather, _ = sim.plan_score(r, sim.preview_preparation(r, prep), paid,
                                        prep, movement_cards, projection)
        sim.global_events = [{'card': card('EV-010'), 'activate_round': 2, 'source': 'P1'}]
        visible_weather, _ = sim.plan_score(r, sim.preview_preparation(r, prep), paid,
                                             prep, movement_cards, projection)
        self.assertGreater(visible_weather, no_weather)

    def test_icon_serialization_round_trip(self):
        symbols = '→ ▷ ▶ ▶▶ ▶▶▶ ⚡ ⚡⚡'
        self.assertEqual(json.loads(json.dumps({'icons': symbols}, ensure_ascii=False))['icons'], symbols)
        for name in ('DRG-Race-Cards.md', 'DRG-Training.md', 'DRG-Events.md'):
            content = (ROOT / name).read_text(encoding='utf-8')
            self.assertIn('→' if name.endswith('Events.md') else '⚡', content)


if __name__ == '__main__':
    unittest.main()
