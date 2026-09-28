"""Observability-only checks using bounded live turns, never a marathon."""
import copy
import hashlib
import unittest
from pathlib import Path
from engine.ai_rationale import REASON_CODES, rationale_metrics
from tests.test_ai_victory import fixture, card, ROOT

HISTORICAL = {
    'DRG-Marathon-Audit-Run-01.md': '8fced76c0c5ea168981974b6c29c52b66bba76641e9cbaaeff2cb3cbe1843b71',
    'DRG-Marathon-Audit-Run-02.md': 'b70a8f0a483ca76d2d01078185d36577b47e7da34f048fab5dab061d509bcae8',
    'DRG-Marathon-Audit-Run-03.md': '4cfbd9258b8b8cf62ca476cdbe7d5cf2650201ed25f55fa003f3a10c84d5829c',
}


class Rationale(unittest.TestCase):
    def live(self, cards=('TR-008', 'FU-014'), difficulty=5, energy=8):
        sim, runner = fixture(difficulty=difficulty)
        runner['hand'] = [card(cid) for cid in cards]
        runner['energy'] = energy
        sim.turn(runner)
        return sim, runner, sim.ai_decisions[0]

    def test_every_ai_turn_has_selected_plan_and_rejected_alternative(self):
        sim, _, decision = self.live()
        self.assertEqual(len([e for e in sim.events if e['type'] == 'AI_TURN_RATIONALE']), 1)
        self.assertEqual(len([e for e in sim.events if e['type'] == 'AI_TURN_OUTCOME']), 1)
        self.assertEqual(decision['selected_plan']['movement_cards'], ['TR-008', 'FU-014'])
        self.assertTrue(decision['rejected_alternatives'])
        self.assertGreater(decision['legal_plan_set']['count'], 1)
        self.assertIn('Training install/replace + Move', decision['legal_plan_set']['class_counts'])

    def test_projection_energy_and_justification(self):
        _, _, d = self.live()
        p = d['selected_plan']
        self.assertEqual(p['projected_movement_miles'], 1.0)
        self.assertIsInstance(p['projected_energy_cost'], int)
        self.assertIn('Projected Pace cost', d['reason'])
        self.assertIn('estimated turns-to-finish', d['reason'])
        self.assertIn('total_plan_score', p)

    def test_zero_movement_records_positive_alternative_status(self):
        sim, _, d = self.live(cards=('FU-014',), difficulty=12)
        self.assertEqual(d['outcome']['actual_movement_quarters'], 0)
        self.assertFalse(d['outcome']['legal_positive_alternative_existed'])
        metrics = rationale_metrics(sim.ai_decisions)
        self.assertEqual(metrics['total_zero_movement_turns'], 1)
        self.assertEqual(metrics['zero_movement_with_no_positive_alternative'], 1)

    def test_setup_records_opportunity_cost_and_rejection(self):
        sim, _, d = self.live()
        setup = next(x for x in d['rejected_alternatives'] if x['plan_type'] ==
                     'Training install/replace + Move' and x['projected_movement_quarters'] == 0)
        self.assertGreater(setup['immediate_movement_opportunity_cost_quarters'], 0)
        self.assertIsNotNone(setup['remaining_distance_discount'])
        self.assertIsNotNone(setup['estimated_turns_to_recover_setup'])
        self.assertEqual(rationale_metrics(sim.ai_decisions)['turns_with_setup_rejected_for_opportunity_cost'], 1)

    def test_pace_and_position_inputs(self):
        sim, runner = fixture()
        runner['hand'] = [card('FU-014'), card('TR-008')]
        opponent = sim.new_runner(1, 'Balanced', [])
        opponent['quarter_mile_space'] = 8
        sim.runners.append(opponent)
        sim.start_round()
        sim.turn(runner)
        d = sim.ai_decisions[0]
        self.assertEqual(d['race_position']['place'], 2)
        self.assertEqual(d['race_position']['gap_to_leader_miles'], 2)
        self.assertTrue(d['pace_rationale']['legal_options_at_round_start'])
        self.assertIn('projected_selected_cost', d['pace_rationale'])
        self.assertIn('maximum_legal', d['pace_rationale'])

    def test_reason_code_and_final_phase(self):
        sim, runner = fixture(difficulty=1)
        runner['quarter_mile_space'] = len(sim.course) * 4 - 2
        runner['hand'] = [card('FU-014'), card('TR-008')]
        sim.turn(runner)
        d = sim.ai_decisions[0]
        self.assertIn(d['reason_code'], REASON_CODES)
        self.assertTrue(d['finish_phase']['within_final_three_miles'])

    def test_logging_disabled_preserves_action_and_state(self):
        on, runner_on = fixture()
        off, runner_off = fixture()
        for r in (runner_on, runner_off):
            r['hand'] = [card('TR-008'), card('FU-014')]
        off.ai_rationale_enabled = False
        on.turn(runner_on)
        off.turn(runner_off)
        self.assertEqual(runner_on, runner_off)
        self.assertEqual(on.rng.getstate(), off.rng.getstate())
        self.assertEqual([(e['type'], e['payload']) for e in on.events
                          if e['type'] not in ('AI_TURN_RATIONALE', 'AI_TURN_OUTCOME')],
                         [(e['type'], e['payload']) for e in off.events])
        self.assertEqual(len(off.ai_decisions), 0)

    def test_no_mutation_during_capture(self):
        sim, runner = fixture()
        runner['hand'] = [card('TR-008'), card('FU-014')]
        prior = copy.deepcopy(runner), sim.rng.getstate(), len(sim.events)
        capture = {}
        plan = sim.choose_turn_plan(runner, capture)
        self.assertEqual(plan, sim.choose_turn_plan(runner))
        self.assertEqual((runner, sim.rng.getstate(), len(sim.events)), prior)

    def test_historical_audit_hashes(self):
        for filename, expected in HISTORICAL.items():
            with self.subTest(filename=filename):
                self.assertEqual(hashlib.sha256((ROOT / filename).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
