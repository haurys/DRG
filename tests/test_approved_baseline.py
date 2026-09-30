"""Approved 2+2 slots, Fuel choice, and acquisition resistance in live race paths."""
import copy
import json
import unittest
from pathlib import Path
from engine import simulate as m

ROOT = Path(__file__).resolve().parents[1]
CARDS = {c['id']: c for c in json.loads((ROOT / 'data/race_cards.json').read_text())}
CFG = json.loads((ROOT / 'simulation/config.json').read_text())


def card(cid):
    return copy.deepcopy(CARDS[cid])


def fixture():
    sim = m.Sim(ROOT, copy.deepcopy(CFG))
    sim.build_course()
    sim.runners = [sim.new_runner(0, 'Fixture', [])]
    return sim, sim.runners[0]


def installed(cid):
    return {'card': card(cid), 'remaining_turns': None}


class ApprovedBaseline(unittest.TestCase):
    def test_two_slots_replace_and_recycle(self):
        sim, r = fixture()
        r['active_training'] = [installed('TR-001'), installed('TR-003')]
        r['hand'] = [card('TR-011')]
        invalid = {'action': 'training', 'card_id': 'TR-011'}
        self.assertFalse(sim.legal_treat_prepare(r, invalid))
        plan = {**invalid, 'replace_id': 'TR-001'}
        self.assertTrue(sim.legal_treat_prepare(r, plan))
        sim.resolve_treat_prepare(r, plan)
        self.assertEqual([e['card']['id'] for e in r['active_training']], ['TR-003', 'TR-011'])
        self.assertIn('TR-001', [c['id'] for c in sim.discard])
        r['equipped_gear'] = [installed('GE-006'), installed('GE-008')]
        r['hand'] = [card('GE-010')]
        bad = {'action': 'gear', 'card_id': 'GE-010'}
        self.assertFalse(sim.legal_treat_prepare(r, bad))
        sim.resolve_treat_prepare(r, {**bad, 'replace_id': 'GE-006'})
        self.assertEqual(len(r['equipped_gear']), 2)
        self.assertIn('GE-006', [c['id'] for c in sim.discard])
        self.assertEqual(sim.choose_treat_prepare(r), None)

    def test_attachment_outside_slots_and_footwear(self):
        sim, r = fixture()
        r['equipped_gear'] = [installed('GE-001'), installed('GE-006')]
        blister = m.make_condition(card('CO-005'))
        r['active_conditions'] = [blister]
        r['hand'] = [card('GE-003'), card('GE-005')]
        attach = {'action': 'attach', 'card_id': 'GE-003', 'condition_id': 'CO-005'}
        self.assertTrue(sim.legal_treat_prepare(r, attach))
        sim.resolve_treat_prepare(r, attach)
        self.assertEqual((len(r['equipped_gear']), len(r['attached_gear'])), (2, 1))
        self.assertFalse(sim.legal_treat_prepare(r, {'action': 'gear', 'card_id': 'GE-005'}))
        plan = {'action': 'gear', 'card_id': 'GE-005', 'replace_id': 'GE-001'}
        self.assertTrue(sim.legal_treat_prepare(r, plan))
        sim.resolve_treat_prepare(r, plan)
        self.assertEqual(sum(e['card']['title'] in m.FOOTWEAR for e in r['equipped_gear']), 1)
        self.assertIn('GE-001', [c['id'] for c in sim.discard])

    def test_fuel_all_titles_two_recovery_and_choices(self):
        for cid in [c['id'] for c in CARDS.values() if c['family'] == 'Fuel']:
            with self.subTest(cid=cid):
                sim, r = fixture()
                r['energy'] = 4
                c = card(cid)
                r['hand'] = [c]
                plan = {'action': 'fuel', 'card_id': cid,
                        'choice': 'energy' if c['title'] in ('Electrolytes', 'Salt Tabs', 'Banana', 'Water Bottle') else None}
                self.assertTrue(sim.legal_treat_prepare(r, plan))
                sim.resolve_treat_prepare(r, plan)
                self.assertEqual(r['energy'], 6)
                self.assertEqual(sim.discard[-1]['id'], cid)
        for cid, condition_id, title in [('FU-016', 'CO-010', 'Dehydrated'),
                                          ('FU-019', 'CO-001', 'Cramp')]:
            sim, r = fixture()
            r['energy'] = 4
            r['active_conditions'] = [m.make_condition(card(condition_id))]
            r['hand'] = [card(cid)]
            sim.resolve_treat_prepare(r, {'action': 'fuel', 'card_id': cid, 'choice': 'remedy'})
            self.assertEqual(r['energy'], 4)
            self.assertIsNone(sim.condition_by_title(r, title))

    def test_fuel_movement_and_conditions(self):
        sim, r = fixture()
        r['hand'] = [card('FU-001')]
        r['energy'] = 4
        sim.start_round({'P1': 'Easy'})
        sim.turn(r, {'treat_prepare': None, 'movement_cards': ['FU-001']})
        self.assertEqual(r['energy'], 4)
        self.assertEqual([e['payload']['card']['effort'] for e in sim.events if e['type'] == 'PLAY'], [3])
        sim, r = fixture()
        r['energy'] = 4
        r['hand'] = [card('FU-001')]
        r['active_conditions'] = [m.make_condition(card('CO-012'))]
        self.assertFalse(sim.legal_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-001'}))
        with self.assertRaisesRegex(ValueError, 'illegal Treat/Prepare'):
            sim.resolve_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-001'})
        r['hand'] = [card('FU-019')]
        r['active_conditions'] = [m.make_condition(card('CO-013'))]
        self.assertTrue(sim.legal_treat_prepare(r, {'action': 'fuel', 'card_id': 'FU-019', 'choice': 'energy'}))

    def test_acquisition_and_installation_reductions_floor_and_do_not_rebound(self):
        cases = [(['TR-001'], 'CO-004', 3), (['TR-003'], 'CO-004', 4),
                 (['TR-003'], 'CO-003', 2), (['TR-011'], 'CO-001', 3),
                 (['TR-011'], 'CO-003', 2), (['TR-013'], 'CO-014', 1),
                 (['TR-017'], 'CO-007', 1), (['TR-017'], 'CO-009', 3),
                 (['TR-001', 'TR-003'], 'CO-004', 2),
                 (['TR-003', 'TR-011'], 'CO-003', 1),
                 (['TR-013', 'TR-014'], 'CO-014', 0),
                 (['TR-019'], 'CO-004', 5)]
        for training_ids, condition_id, expected in cases:
            with self.subTest(training=training_ids, condition=condition_id):
                sim, r = fixture()
                r['active_training'] = [installed(cid) for cid in training_ids]
                sim.draw = [card('FU-002'), card(condition_id)]
                sim.draw_one(r)
                payload = next(e['payload'] for e in sim.events if e['type'] == 'CONDITION_APPLY')
                condition = r['active_conditions'][0] if r['active_conditions'] else payload
                self.assertEqual(condition['current_severity'], expected)
                if expected == 0 and not condition['persistent']:
                    self.assertIn(condition_id, [c['id'] for c in sim.discard])
                self.assertEqual(sum(x['amount'] for x in payload['training_resistance']),
                                 sum(m.TRAINING_RESISTANCE.get(CARDS[cid]['title'], {}).get(condition['title'], 0)
                                     for cid in training_ids))
                r['active_training'] = []
                self.assertEqual(condition['current_severity'], expected)
        sim, r = fixture()
        r['active_conditions'] = [m.make_condition(card('CO-004'))]
        sim.install_training(r, card('TR-001'))
        self.assertEqual(r['active_conditions'][0]['current_severity'], 3)
        self.assertTrue(any(e['type'] == 'CONDITION_SEVERITY_CHANGE' for e in sim.events))

    def test_ai_replacement_and_remedy_legality(self):
        sim, r = fixture()
        r['active_training'] = [installed('TR-001'), installed('TR-003')]
        r['hand'] = [card('TR-011')]
        self.assertIn({'card_id': 'TR-011', 'action': 'training', 'replace_id': 'TR-001'},
                      sim.treat_candidates(r))
        r['hand'] = [card('FU-016')]
        r['active_conditions'] = [m.make_condition(card('CO-010'))]
        self.assertIn({'card_id': 'FU-016', 'action': 'fuel', 'choice': 'remedy'},
                      sim.treat_candidates(r))
        r['active_conditions'] = []
        r['energy'] = 4
        self.assertIn({'card_id': 'FU-016', 'action': 'fuel', 'choice': 'energy'},
                      sim.treat_candidates(r))


if __name__ == '__main__':
    unittest.main()
