"""Bounded reproduction of Formal Run 06 v1.3 no-helper audit label."""
import copy
import json
import unittest
from pathlib import Path

from engine import simulate as m


ROOT = Path(__file__).resolve().parents[1]
HAND = ('FU-004', 'FU-011', 'FU-020', 'FU-003', 'FU-016', 'FU-018', 'FU-002')


def no_helper_fixture():
    config = json.loads((ROOT / 'simulation/config.json').read_text())
    config['seed'] = 20260930
    cards = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
    sim = m.Sim(ROOT, config)
    sim.build_course()
    requester = sim.new_runner(4, 'Pack Runner', [copy.deepcopy(cards[cid]) for cid in HAND])
    requester.update(quarter_mile_space=92, distance_completed=23.0,
                     energy=0, will_available=False, race_turn_number=50)
    requester['active_conditions'] = [m.make_condition(cards[cid]) for cid in ('CO-001', 'CO-012')]
    other = sim.new_runner(0, 'Balanced', [])
    other.update(finished=True, race_status='FINISHED', finish_order=1)
    sim.runners = [other, requester]
    sim.round = 50
    sim.draw = []
    sim.discard = []
    return sim, requester, other


class NoHelperReason(unittest.TestCase):
    def test_run06_p5_no_helper_reason_is_metadata_only(self):
        def execute():
            sim, requester, other = no_helper_fixture()
            before = copy.deepcopy((requester['hand'], requester['energy'],
                                    requester['quarter_mile_space'], requester['will_available'],
                                    requester['active_conditions'], other))
            self.assertEqual(sim.assistance_helper(requester), (None, 1, None))
            self.assertFalse(sim.request_assistance(requester))
            selected = [e for e in sim.events if e['type'] == 'ASSISTANCE_PARTNER_SELECT'][-1]
            self.assertEqual(selected['payload']['helper'], None)
            self.assertEqual(selected['payload']['reason'], 'no_eligible_active_helper')
            self.assertFalse(any(e['type'] == 'ASSISTANCE_SWAP' for e in sim.events))
            self.assertEqual(before, (requester['hand'], requester['energy'],
                                      requester['quarter_mile_space'], requester['will_available'],
                                      requester['active_conditions'], other))
            self.assertEqual(requester['stats']['treat_prepare_actions'], 1)
            self.assertTrue(sim.evaluate_dnf(requester, assistance_evaluated=True,
                                             treat_available=False))
            evaluation = [e for e in sim.events if e['type'] == 'DNF_EVALUATION'][-1]['payload']
            self.assertTrue(evaluation['assistance_evaluated'])
            self.assertEqual(evaluation['continuation']['kind'], 'exhausted_known_paths')
            self.assertEqual((requester['race_status'], requester['distance_completed'],
                              requester['energy'], requester['dnf_turn']), ('DNF', 23.0, 0, 50))
            return [e for e in sim.events if e['type'].startswith('ASSISTANCE')
                    or e['type'] in ('TREAT_PREPARE', 'DNF_EVALUATION', 'DNF')]

        self.assertEqual(execute(), execute())


if __name__ == '__main__':
    unittest.main()
