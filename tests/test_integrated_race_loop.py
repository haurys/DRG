import copy, importlib.util, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('integrated', ROOT / 'engine/simulate.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
BASE_CFG = json.loads((ROOT / 'simulation/config.json').read_text())


def card(card_id):
    cards = json.loads((ROOT / 'data/race_cards.json').read_text())
    return copy.deepcopy(next(item for item in cards if item['id'] == card_id))


def make_sim(players=2):
    cfg = copy.deepcopy(BASE_CFG)
    cfg['player_count'] = players
    sim = m.Sim(ROOT, cfg)
    sim.build_course()
    sim.runners = [sim.new_runner(index, f'Fixture {index + 1}', []) for index in range(players)]
    sim.draw = []
    sim.discard = []
    return sim


def event_payloads(sim, event_type, player=None):
    return [event['payload'] for event in sim.events
            if event['type'] == event_type and (player is None or event['player_id'] == player)]


class IntegratedRaceLoop(unittest.TestCase):
    def test_replenish_draws_toward_seven_with_two_normal_limit_and_condition_chain(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        runner['hand'] = [card('TR-001'), card('TR-002'), card('TR-003'), card('TR-004')]
        sim.draw = [card('FU-001'), card('FU-002'), card('CO-014')]
        drawn = sim.replenish(runner)
        self.assertEqual(drawn, 2)
        self.assertEqual(len(runner['hand']), 6)
        self.assertEqual(runner['active_conditions'][0]['title'], 'Side Stitch')

    def test_turn_integrates_install_pack_will_event_boundary_and_direct_movement(self):
        sim = make_sim(2)
        sim.course[0].update({'difficulty': 1, 'elevation': 'Flat', 'surface': 'Asphalt'})
        sim.course[1].update({'difficulty': 4, 'elevation': 'Incline', 'surface': 'Asphalt'})
        first, second = sim.runners
        first['quarter_mile_space'] = second['quarter_mile_space'] = 3
        first['energy'] = 0
        first['hand'] = [card('TR-009'), card('EV-003')]
        second['hand'] = [card('TR-001')]
        sim.start_round({'P1': 'Push', 'P2': 'Push'})
        result = sim.turn(first, {'treat_prepare': {'card_id': 'TR-009', 'action': 'training'},
                                  'movement_cards': ['EV-003']})
        payment = event_payloads(sim, 'PACE_PAYMENT', 'P1')[-1]
        boundary = event_payloads(sim, 'MOVE_BOUNDARY', 'P1')[-1]
        self.assertIn('Pack', payment['preservation_sources'])
        self.assertTrue(payment['will_used'])
        self.assertFalse(first['will_available'])
        self.assertEqual(boundary['previous_difficulty'], 1)
        self.assertEqual(boundary['new_difficulty'], 2)
        self.assertEqual(result['direct_quarter_miles'], 1)
        self.assertIn('Hill Repeats', sim.installed_titles(first, 'training'))

    def test_pack_preservation_changes_live_pace_cost(self):
        sim = make_sim(3)
        sim.runners[0]['quarter_mile_space'] = sim.runners[1]['quarter_mile_space'] = 0
        sim.runners[2]['quarter_mile_space'] = 8
        sim.start_round({'P1': 'Push', 'P2': 'Push', 'P3': 'Push'})
        self.assertEqual(sim.pace_cost(sim.runners[0], 'Push')['final'], 1)
        self.assertEqual(sim.pace_cost(sim.runners[2], 'Push')['final'], 2)
        sim.runners[2]['energy'] = 1
        _, used = sim.pay_pace(sim.runners[2])
        self.assertTrue(used)
        self.assertEqual(sim.runners[2]['energy'], 0)

    def test_heat_and_water_gear_execute_in_live_paths(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        runner['equipped_gear'] = [{'card': card('GE-008'), 'remaining_turns': 4},
                                   {'card': card('GE-012'), 'remaining_turns': None}]
        sim.round = 2
        sim.global_events = [{'card': card('EV-006'), 'source': 'P1', 'staged_round': 1,
                              'activate_round': 2, 'expiry_round': 2}]
        cost = sim.pace_cost(runner, 'Push')
        self.assertEqual(cost['global_extra'], 1)
        self.assertEqual(cost['heat_preservation_sources'], ['Tech Shirt'])
        self.assertEqual(cost['final'], 2)
        runner['energy'] = 5
        sim.resolve_milestones(runner, 15, 16)
        self.assertEqual(runner['energy'], 6)

    def test_condition_suppression_zero_and_rebound_in_live_turn(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        blister = m.make_condition(card('CO-005'))
        blister['current_severity'] = 2
        m.update_effective_severity(blister)
        runner['active_conditions'] = [blister]
        runner['hand'] = [card('GE-003'), card('TR-001')]
        sim.start_round({'P1': 'Push'})
        sim.turn(runner, {'treat_prepare': {'card_id': 'GE-003', 'action': 'attach',
                                            'condition_id': 'CO-005'},
                          'movement_cards': ['TR-001']})
        payment = event_payloads(sim, 'PACE_PAYMENT', 'P1')[-1]
        self.assertEqual(blister['effective_severity'], 0)
        self.assertEqual(payment['condition_extra'], 0)
        attachment = runner['attached_gear'][0]
        sim.remove_gear(runner, attachment, 'fixture removal')
        self.assertEqual(blister['effective_severity'], 2)
        self.assertEqual(sim.pace_cost(runner, 'Push')['condition_extra'], 1)

    def test_gear_relocation_uses_treat_prepare_without_new_card_play(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        blister = m.make_condition(card('CO-005'))
        runner['active_conditions'] = [blister]
        gear = {'card': card('GE-003'), 'remaining_turns': None}
        runner['equipped_gear'] = [gear]
        used = sim.resolve_treat_prepare(runner, {'card_id': 'GE-003', 'action': 'relocate',
                                                  'condition_id': 'CO-005'})
        self.assertEqual(used, 0)
        self.assertFalse(runner['equipped_gear'])
        self.assertEqual(blister['effective_severity'], 1)
        self.assertEqual(event_payloads(sim, 'GEAR_RELOCATE', 'P1')[-1]['card_play_budget'], 0)

    def test_fuel_remedy_and_effort_treatment_execute_in_turn_path(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        dehydrated = m.make_condition(card('CO-010'))
        runner['active_conditions'] = [dehydrated]
        runner['energy'] = 5
        runner['hand'] = [card('FU-016'), card('TR-001')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'treat_prepare': {'card_id': 'FU-016', 'action': 'fuel', 'choice': 'remedy'},
                          'movement_cards': ['TR-001']})
        self.assertIsNone(sim.condition_by_title(runner, 'Dehydrated'))
        self.assertEqual(runner['energy'], 5)

        second = make_sim(1)
        target = second.runners[0]
        cramp = m.make_condition(card('CO-001'))
        target['active_conditions'] = [cramp]
        target['hand'] = [card('TR-011'), card('TR-001')]
        second.start_round({'P1': 'Race'})
        second.turn(target, {'treat_prepare': {'card_id': 'TR-011', 'action': 'treat',
                                               'condition_id': 'CO-001'},
                             'movement_cards': ['TR-001']})
        self.assertIsNone(second.condition_by_title(target, 'Cramp'))

    def test_gut_check_uses_live_hand_training_and_gear(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        sim.course[9]['difficulty'] = 0
        runner['quarter_mile_space'] = 39
        runner['active_training'] = [{'card': card('TR-019'), 'remaining_turns': None}]
        runner['equipped_gear'] = [{'card': card('GE-018'), 'remaining_turns': None}]
        runner['hand'] = [card('EV-003'), card('EV-022'), card('EV-025'), card('TR-011')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'treat_prepare': None, 'movement_cards': ['EV-003']})
        check = [payload['gut_check'] for payload in event_payloads(sim, 'MILESTONE', 'P1')
                 if payload['kind'] == 'Gut Check'][0]
        self.assertEqual(check['hand_effort'], 22)
        self.assertEqual(check['modifiers'], 3)
        self.assertEqual(check['total'], 25)
        self.assertTrue(check['passed'])

    def test_all_events_have_integrated_coverage_classification(self):
        self.assertEqual(set(m.EVENT_COVERAGE), {f'EV-{index:03d}' for index in range(1, 31)})
        sim = make_sim(1)
        runner = sim.runners[0]
        runner['pace'] = 'Race'
        self.assertEqual(sim.event_current_effects(runner, [card('EV-003')])[1], 1)
        self.assertEqual(sim.event_current_effects(runner, [card('EV-008')])[0], 1)
        self.assertEqual(sim.event_current_effects(runner, [card('EV-019')])[0], 1)
        self.assertTrue(sim.event_current_effects(runner, [card('EV-014')])[2])
        self.assertEqual(sim.event_current_effects(runner, [card('EV-026')])[3], 2)
        self.assertEqual(set(m.AFTER_ENERGY), {'EV-007', 'EV-015', 'EV-016', 'EV-021', 'EV-022',
                                               'EV-024', 'EV-028', 'EV-029'})

    def test_staged_course_global_after_and_transfer_events_execute(self):
        staged = make_sim(2)
        first, second = staged.runners
        first['hand'] = [card('EV-001')]
        second['hand'] = [card('TR-001')]
        staged.start_round({'P1': 'Easy', 'P2': 'Easy'})
        staged.turn(first, {'treat_prepare': None, 'movement_cards': ['EV-001'], 'event_target': 'P2'})
        self.assertEqual(second['staged_events'][0]['card']['id'], 'EV-001')
        staged.end_round()
        staged.start_round({'P1': 'Race', 'P2': 'Race'})
        staged.turn(second, {'treat_prepare': None, 'movement_cards': ['TR-001']})
        self.assertEqual(event_payloads(staged, 'MOVE', 'P2')[-1]['event_effort_bonus'], -1)
        self.assertFalse(second['staged_events'])

        course = make_sim(1)
        course.runners[0]['hand'] = [card('EV-005')]
        course.start_round({'P1': 'Easy'})
        course.turn(course.runners[0], {'treat_prepare': None, 'movement_cards': ['EV-005']})
        self.assertEqual(course.course_events[0]['remaining_duration'], 4)

        global_sim = make_sim(1)
        global_sim.runners[0]['hand'] = [card('EV-006')]
        global_sim.start_round({'P1': 'Easy'})
        global_sim.turn(global_sim.runners[0], {'treat_prepare': None, 'movement_cards': ['EV-006']})
        global_sim.end_round()
        global_sim.start_round({'P1': 'Push'})
        self.assertEqual(global_sim.pace_cost(global_sim.runners[0], 'Push')['global_extra'], 1)

        after = make_sim(2)
        after.runners[0]['energy'] = 5
        after.runners[0]['hand'] = [card('EV-007')]
        after.start_round({'P1': 'Easy', 'P2': 'Easy'})
        after.turn(after.runners[0], {'treat_prepare': None, 'movement_cards': ['EV-007']})
        self.assertEqual(after.runners[0]['energy'], 6)

        transfer = make_sim(2)
        transfer.runners[0]['energy'] = 5
        transfer.runners[0]['hand'] = [card('EV-020')]
        transfer.start_round({'P1': 'Easy', 'P2': 'Easy'})
        transfer.turn(transfer.runners[0], {'treat_prepare': None, 'movement_cards': ['EV-020']})
        received = next(item for item in transfer.runners[1]['hand'] if item['id'] == 'EV-020')
        self.assertEqual(received['earliest_replay_round'], 2)
        self.assertEqual(transfer.runners[0]['energy'], 6)

    def test_high_five_uses_pack_snapshot_and_round_end_award(self):
        sim = make_sim(2)
        for runner in sim.runners:
            runner['energy'] = 5
        sim.runners[0]['hand'] = [card('EV-018')]
        sim.start_round({'P1': 'Easy', 'P2': 'Easy'})
        sim.turn(sim.runners[0], {'treat_prepare': None, 'movement_cards': ['EV-018']})
        self.assertEqual([runner['energy'] for runner in sim.runners], [5, 5])
        sim.end_round()
        self.assertEqual([runner['energy'] for runner in sim.runners], [6, 6])

    def test_live_elevation_boundary_reductions(self):
        cases = [
            ('Hill Repeats', 'Flat', 1, 'Incline', 4, 1, 2),
            ('Hill Repeats', 'Incline', 4, 'Steep Incline', 5, 2, 4),
            ('Downhill Practice', 'Flat', 1, 'Descent', 4, 1, 2),
            ('Downhill Practice', 'Descent', 4, 'Steep Descent', 5, 2, 4),
        ]
        for title, old_elevation, old_printed, new_elevation, new_printed, old_effective, new_effective in cases:
            with self.subTest(title=title, transition=f'{old_elevation}->{new_elevation}'):
                sim = make_sim(1)
                runner = sim.runners[0]
                sim.course[0].update({'difficulty': old_printed, 'elevation': old_elevation})
                sim.course[1].update({'difficulty': new_printed, 'elevation': new_elevation})
                training_id = 'TR-009' if title == 'Hill Repeats' else 'TR-018'
                runner['active_training'] = [{'card': card(training_id), 'remaining_turns': None}]
                runner['quarter_mile_space'] = 3
                runner['hand'] = [card('EV-023')]
                sim.start_round({'P1': 'Easy'})
                sim.turn(runner, {'treat_prepare': None, 'movement_cards': ['EV-023']})
                boundary = event_payloads(sim, 'MOVE_BOUNDARY', 'P1')[0]
                self.assertEqual(boundary['previous_difficulty'], old_effective)
                self.assertEqual(boundary['new_difficulty'], new_effective)

    def test_live_deck_recycle_excludes_in_play_cards(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        runner['hand'] = [card('TR-001')] * 6
        blocked = card('TR-009')
        eligible = card('FU-001')
        runner['active_training'] = [{'card': blocked, 'remaining_turns': None}]
        sim.discard = [copy.deepcopy(blocked), eligible]
        sim.replenish(runner)
        self.assertIn('FU-001', [item['id'] for item in runner['hand']])
        self.assertEqual([item['id'] for item in sim.discard], ['TR-009'])
        self.assertEqual(sim.deck_audit[-1], {'eligible_count': 1, 'excluded_count': 1})

    def run_finish_case(self, first_leftover, second_leftover, energies=(5, 5), wills=(True, True)):
        sim = make_sim(2)
        endpoint = len(sim.course) * 4
        for index, runner in enumerate(sim.runners):
            runner['quarter_mile_space'] = endpoint
            runner['energy'] = energies[index]
            runner['will_available'] = wills[index]
        sim.runners[0]['hand'] = [card(item) for item in
                                  ['FU-010', first_leftover, 'TR-003', 'TR-005', 'TR-009', 'TR-011', 'TR-015']]
        sim.runners[1]['hand'] = [card(item) for item in
                                  ['FU-021', second_leftover, 'TR-006', 'TR-014', 'TR-010', 'TR-012', 'TR-016']]
        scripts = {
            'P1': {'treat_prepare': None, 'movement_cards': ['FU-010']},
            'P2': {'treat_prepare': None, 'movement_cards': ['FU-021']},
        }
        sim.run_round(scripts, {'P1': 'Easy', 'P2': 'Easy'})
        return sim

    def test_finish_requires_positive_movement_beyond_course_endpoint(self):
        sim = make_sim(1)
        runner = sim.runners[0]
        sim.course[-1]['difficulty'] = 0
        runner['quarter_mile_space'] = len(sim.course) * 4 - 1
        runner['hand'] = [card('FU-010')]
        sim.start_round({'P1': 'Easy'})
        sim.turn(runner, {'treat_prepare': None, 'movement_cards': ['FU-010']})
        self.assertEqual(runner['quarter_mile_space'], len(sim.course) * 4)
        self.assertFalse(runner['finish_pending'])

    def test_same_round_finish_tiebreak_by_hand_effort(self):
        sim = self.run_finish_case('TR-019', 'TR-001')
        self.assertEqual((sim.runners[0]['finish_order'], sim.runners[1]['finish_order']), (1, 2))

    def test_same_round_finish_tiebreak_by_energy(self):
        sim = self.run_finish_case('TR-001', 'TR-002', energies=(7, 5))
        self.assertEqual((sim.runners[0]['finish_order'], sim.runners[1]['finish_order']), (1, 2))

    def test_same_round_finish_tiebreak_by_will(self):
        sim = self.run_finish_case('TR-001', 'TR-002', energies=(5, 5), wills=(True, False))
        self.assertEqual((sim.runners[0]['finish_order'], sim.runners[1]['finish_order']), (1, 2))

    def test_same_round_finish_exact_tie_is_shared(self):
        sim = self.run_finish_case('TR-001', 'TR-002')
        self.assertEqual((sim.runners[0]['finish_order'], sim.runners[1]['finish_order']), (1, 1))
        finish_events = event_payloads(sim, 'FINISH')
        self.assertTrue(all(payload['shared'] for payload in finish_events))


if __name__ == '__main__':
    unittest.main()
