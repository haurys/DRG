"""Observation-only recorder for the one authorized seeded marathon.

The subclass delegates all game operations to the canonical Sim. It snapshots
emissions immediately because the engine's event state can contain live objects.
"""

import collections
import copy
import json
import statistics
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.simulate import Sim, load_json  # noqa: E402

DEST = ROOT / 'DRG-Marathon-Audit-Run-01.md'
ASSUMPTIONS = [
    'RR-11 — Gear relocation occupies Treat/Prepare, with zero new-card plays.',
    'RR-13 — AI consents to the nearest legal same-Pace group within 0.5 mile of its leader at Round Start; stable player ID breaks policy ties.',
    'RR-16 — AI prioritizes applicable named remedies; Electrolytes remedies Dehydrated, Salt Tabs remedies Cramp, otherwise scripted legal Energy choice may apply.',
    'RR-17 — a positive legal quarter-mile unit beyond the Course endpoint covers the 0.2-mile Finish extension; arriving with no remaining movement does not finish.',
    'Potholes target policy — lose 1 Energy when available, otherwise take −1 Movement.',
]


class BlockingAuditBug(Exception):
    pass


class RecordedSim(Sim):
    def __init__(self, root, cfg):
        super().__init__(root, cfg)
        self.audit_events = []
        self._recycle_input = None

    def deck_snapshot(self, full=False):
        excluded = self.in_play_ids()
        eligible = [card['id'] for card in self.discard if card['id'] not in excluded]
        row = {
            'draw_count': len(self.draw), 'discard_count': len(self.discard),
            'eligible_discard_count': len(eligible),
            'hands_count': sum(len(r['hand']) for r in self.runners),
            'training_count': sum(len(r['active_training']) for r in self.runners),
            'equipped_gear_count': sum(len(r['equipped_gear']) for r in self.runners),
            'attached_gear_count': sum(len(r['attached_gear']) for r in self.runners),
            'conditions_in_play_count': sum(len(r['active_conditions']) for r in self.runners),
            'staged_events_count': sum(len(r['staged_events']) for r in self.runners),
            'course_events_count': len(self.course_events),
            'global_events_count': len(self.global_events),
        }
        if full:
            row.update(draw_ids=[c['id'] for c in self.draw],
                       discard_ids=[c['id'] for c in self.discard],
                       eligible_discard_ids=eligible,
                       excluded_in_play_ids=sorted(excluded))
        return row

    def refill(self):
        if not self.draw:
            self._recycle_input = self.deck_snapshot(full=True)
        try:
            return super().refill()
        finally:
            self._recycle_input = None

    def runner_snapshot(self, runner):
        return {
            'position_quarters': runner['quarter_mile_space'],
            'position_miles': runner['quarter_mile_space'] / 4,
            'energy': runner['energy'], 'will_available': runner['will_available'],
            'pace': runner['pace'], 'pack': runner['pack_state'],
            'pack_members': list(runner['pack_members_snapshot']),
            'pack_leader': runner['pack_leader'],
            'hand': [{'id': c['id'], 'effort': c.get('effort'), 'family': c['family']}
                     for c in runner['hand']],
            'training': [{'id': e['card']['id'], 'duration': e['remaining_turns']}
                         for e in runner['active_training']],
            'gear': [{'id': e['card']['id'], 'duration': e['remaining_turns']}
                     for e in runner['equipped_gear']],
            'attached_gear': [{'id': e['card']['id'], 'condition': e['condition_id'],
                               'suppression': e['amount'], 'duration': e['remaining_turns']}
                              for e in runner['attached_gear']],
            'conditions': copy.deepcopy(runner['active_conditions']),
            'staged_events': [{'id': e['card']['id'], 'target': e['target'],
                               'activate_round': e['activate_round']}
                              for e in runner['staged_events']],
            'finished': runner['finished'], 'finish_pending': runner['finish_pending'],
        }

    def emit(self, event_type, player=None, payload=None, state=None):
        event = super().emit(event_type, player, payload, state)
        snapshot = {
            'event': copy.deepcopy(event),
            'runners': {r['player_id']: self.runner_snapshot(r) for r in self.runners},
            'deck': self.deck_snapshot(full=event_type in ('DECK_SHUFFLE', 'DRAW_FAILED')),
            'course_events': copy.deepcopy(self.course_events),
            'global_events': [{'id': e['card']['id'], 'activate_round': e['activate_round'],
                               'expiry_round': e['expiry_round']}
                              for e in self.global_events],
        }
        if self._recycle_input is not None and event_type in ('DECK_SHUFFLE', 'DRAW_FAILED'):
            snapshot['recycle_input'] = self._recycle_input
        self.audit_events.append(snapshot)
        if event_type == 'EVENT_NO_TARGET':
            raise BlockingAuditBug('OTHER Event played with no eligible target; mandatory effect cannot resolve')
        return event


def line_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def report(sim, error):
    events = sim.audit_events
    by_type = collections.defaultdict(list)
    for row in events:
        by_type[row['event']['type']].append(row)
    complete = error is None and len(sim.finish) == 8
    lines = [
        '# DRG Marathon Audit Run 01', '',
        f'**Seed:** `{sim.cfg["seed"]}`  ',
        f'**Status:** {"COMPLETED" if complete else "STOPPED — BUG"}  ',
        f'**Round reached:** {sim.round}  ',
        f'**Events recorded:** {len(events)}  ',
        '**Runs performed:** one; no alternate seed or batch  ',
        '**Engine/data/rules modifications during race:** none', '',
        '## PLAYTEST ASSUMPTIONS (simulator policy, not canonical rules)', '',
        *(f'- {item}' for item in ASSUMPTIONS), '',
        '## Race configuration and Course', '',
        f'- Runners: {sim.cfg["player_count"]}; format: {sim.cfg["race_format"]}; '
        'Course endpoint 26.0 miles; Finish threshold 26.2 miles.',
        '- Effort bonuses are fixed from the Movement starting segment; Effective Difficulty is '
        'recalculated at every boundary. Entering Trail grants Trail Effort only on the next Movement.',
        '',
        '### Physical Course-card selection and orientation', '',
    ]
    selects = {e['event']['payload']['position']: e['event']['payload']['course_card_id']
               for e in by_type['COURSE_SELECT']}
    for row in by_type['COURSE_ORIENT']:
        payload = row['event']['payload']
        lines.append(f'- Position {payload["position"]}: {selects[payload["position"]]}; '
                     f'outbound {payload["outbound_side"]}, return {payload["return_side"]}')
    lines += ['', '### All one-mile Course segments', '',
              '| Mile | Card-side | Setting | Difficulty | Elevation | Route | Surface | Milestones |',
              '|---:|---|---|---:|---|---|---|---|']
    for seg in sim.course:
        lines.append(f'| {seg["mile"]} | {seg["id"]} | {seg["setting"]} | {seg["difficulty"]} | '
                     f'{seg["elevation"]} | {seg["route"]} | {seg["surface"]} | '
                     f'{", ".join(seg.get("milestones", [])) or "—"} |')
    lines += ['', '## Pre-race hands and exchange record', '']
    for row in by_type['DEAL']:
        event = row['event']
        lines.append(f'- {event["player_id"]}: {line_json(event["payload"]["cards"])}')
    for row in by_type['DECK_EXCHANGE']:
        event = row['event']
        lines.append(f'- {event["player_id"]}: {line_json(event["payload"])}')
    for runner in sim.runners:
        first = next((r['runners'][runner['player_id']]['hand'] for r in by_type['ROUND_START']
                      if runner['player_id'] in r['runners']), [])
        lines.append(f'- {runner["player_id"]} pre-race final hand: {line_json(first)}; '
                     f'exchanges used {runner["exchanges_used"]}; '
                     f'remaining allowance {sim.cfg["exchange_limit"] - runner["exchanges_used"]}')

    if error:
        lines += ['', '## BUG — blocking state', '', '```text', error.rstrip(), '```', '',
                  '### Exact final state', '', '```json',
                  json.dumps({'round': sim.round, 'runners': {r['player_id']: sim.runner_snapshot(r)
                                for r in sim.runners}, 'deck': sim.deck_snapshot(full=True),
                              'course_events': sim.course_events, 'global_events': sim.global_events},
                             default=str, indent=2), '```']

    lines += ['', '## Chronological full turn and state-transition log', '',
              'Each numbered emission includes its original payload, a deep-copied state at emission, '
              'all runner hands and installed state, and deck counts. Recycle emissions additionally '
              'include exact eligible and excluded physical IDs. TURN_START and TURN_END delimit turns.', '']
    for row in events:
        event = row['event']
        if event['type'] == 'ROUND_START':
            lines += [f'## Round {event["round"]}', '']
        if event['type'] == 'TURN_START':
            lines += [f'### Round {event["round"]} — {event["player_id"]} turn '
                      f'{event["payload"]["turn"]}', '']
        lines.append(f'- **{event["event_id"]} {event["type"]}** '
                     f'({event["player_id"] or "race"}): `{line_json(event["payload"])}`')
        if event['state']:
            lines.append(f'  - Engine state: `{line_json(event["state"])}`')
        lines.append(f'  - Deck: `{line_json(row["deck"])}`')
        if 'recycle_input' in row:
            lines.append(f'  - Pre-recycle inventory: `{line_json(row["recycle_input"])}`')
        lines.append(f'  - Runner state: `{line_json(row["runners"])}`')
        if row['course_events'] or row['global_events']:
            lines.append(f'  - Active Course/Global Events: '
                         f'`{line_json({"course": row["course_events"], "global": row["global_events"]})}`')

    lines += ['', '## Post-race calculations', '']
    if not complete:
        lines.append('Race stopped; finish and aggregate outcome metrics are not reported as completed.')
    else:
        records = sim.turn_records
        moves = [r['movement_quarters'] / 4 for r in records]
        finishers = sorted(sim.runners, key=lambda r: (r['finish_order'], r['player_id']))
        lines += [f'- Total rounds: {sim.round}; runner-turns: {len(records)}; '
                  f'average movement: {statistics.mean(moves):.3f} miles.',
                  f'- Movement counts: 0={moves.count(0)}, 0.25={moves.count(.25)}, '
                  f'1.5+={sum(x >= 1.5 for x in moves)}, 2.0={moves.count(2)}.',
                  f'- Finishing spread: {max(r["finish_round"] for r in finishers) - min(r["finish_round"] for r in finishers)} rounds.',
                  '', '### Finish order and final resources', '']
        for r in finishers:
            lines.append(f'- Place {r["finish_order"]}: {r["player_id"]} ({r["profile"]}), '
                         f'round {r["finish_round"]}, Energy {r["energy"]}, '
                         f'Will {"unspent" if r["will_available"] else "spent"}, '
                         f'hand Effort {sum(c.get("effort") or 0 for c in r["hand"])}.')
        lines += ['', '### Gut Checks', '']
        for mile, threshold in ((10, 25), (18, 30), (23, 35)):
            checks = [e['event']['payload']['gut_check'] for e in by_type['MILESTONE']
                      if e['event']['payload'].get('kind') == 'Gut Check'
                      and e['event']['payload']['mile'] == mile]
            hands = [c['hand_effort'] for c in checks]
            lines.append(f'- Mile {mile} / {threshold}: {sum(c["passed"] for c in checks)} pass, '
                         f'{sum(not c["passed"] for c in checks)} fail; '
                         f'hand Effort average {statistics.mean(hands) if hands else "n/a"}, '
                         f'min {min(hands) if hands else "n/a"}, max {max(hands) if hands else "n/a"}; '
                         f'final-total average '
                         f'{statistics.mean(c["total"] for c in checks) if checks else "n/a"}.')
        lines += ['', '### Cards, Energy, Packs, Course, and deck', '']
        played = collections.Counter(e['event']['payload']['card']['family'] for e in by_type['PLAY'])
        treat_cards = [e['event']['payload'] for e in by_type['TREAT_PREPARE']
                       if e['event']['payload'].get('card')]
        for action, family in (('training', 'Training'), ('gear', 'Gear'), ('attach', 'Gear'),
                               ('fuel', 'Fuel')):
            played[family] += sum(p['action'] == action for p in treat_cards)
        played['Treat/Prepare treatment'] = sum(p['action'] == 'treat' for p in treat_cards)
        lines.append(f'- Cards played by family/action: {line_json(dict(played))}; '
                     f'Training installs {len(by_type["TRAINING_INSTALL"])}, '
                     f'Gear equips {len(by_type["GEAR_EQUIP"])}, '
                     f'Gear attaches {len(by_type["GEAR_ATTACH"])}, '
                     f'Fuel uses {len(by_type["FUEL_USE"])}, '
                     f'Events played {sum(e["event"]["payload"]["card"]["family"] == "Event" for e in by_type["PLAY"])}.')
        lines.append(f'- Conditions applied {len(by_type["CONDITION_APPLY"])}, '
                     f'Tough Decision {len(by_type["TOUGH_DECISION"])}, '
                     f'Helpful Runner transfers {len(by_type["HELPFUL_RUNNER_TRANSFER"])}.')
        payments = [e['event']['payload'] for e in by_type['PACE_PAYMENT']]
        energy_changes = [e['event']['payload'] for e in by_type['ENERGY_CHANGE']]
        lines.append(f'- Pace Energy paid {sum(p["paid"] for p in payments)}; '
                     f'preservation sources {dict(collections.Counter(s for p in payments for s in p["preservation_sources"]))}; '
                     f'Will uses {sum(p["will_used"] for p in payments)}; '
                     f'Fuel recovery {sum(p["energy_after"] - p["energy_before"] for p in (e["event"]["payload"] for e in by_type["FUEL_USE"]))}; '
                     f'other Energy changes gained {sum(max(0, p["delta"]) for p in energy_changes)}, '
                     f'lost {sum(max(0, -p["delta"]) for p in energy_changes)}.')
        zero = sorted({pid for e in events for pid, r in e['runners'].items() if r['energy'] == 0})
        lines.append(f'- Runners reaching zero Energy: {line_json(zero)}; '
                     f'Condition-attributed Energy loss: '
                     f'{sum(-p["delta"] for p in energy_changes if p["delta"] < 0 and "Condition" in p["source"])}.')
        pack_ids = {e['event']['payload']['to'] for e in by_type['PACK_ENTER']}
        pack_rounds = collections.Counter()
        pack_turns = 0
        for e in by_type['ROUND_START']:
            groups = {r['pack'] for r in e['runners'].values() if r['pack']}
            pack_rounds.update(groups)
        for e in by_type['TURN_START']:
            pack_turns += bool(e['runners'][e['event']['player_id']]['pack'])
        lines.append(f'- Packs formed {len(pack_ids)}; average duration '
                     f'{statistics.mean(pack_rounds.values()) if pack_rounds else 0:.2f} rounds; '
                     f'Pack runner-turn share {pack_turns / len(records):.1%}; '
                     f'Pack preservation occurrences '
                     f'{sum("Pack" in p["preservation_sources"] for p in payments)}.')
        recycle = [e for e in by_type['DECK_SHUFFLE']
                   if e['event']['payload'].get('reason') == 'eligible discard recycle']
        lines.append(f'- Reshuffles {len(recycle)}; first round '
                     f'{recycle[0]["event"]["round"] if recycle else "none"}; '
                     f'failed draws {len(by_type["DRAW_FAILED"])}; '
                     f'Course Events {len(by_type["COURSE_EVENT_APPLY"])}.')
        sources = collections.Counter(s for e in by_type['MOVE']
                                      for s in e['event']['payload']['installed_effort_sources'])
        lines.append(f'- Trail Training activations {sources["Trail Training"]}; '
                     f'Trail Shoes activations {sources["Trail Shoes"]}; '
                     f'boundary crossings {len(by_type["MOVE_BOUNDARY"])}; '
                     f'Sudden Rain plays {len(by_type["COURSE_EVENT_APPLY"])}; '
                     f'Good Line plays '
                     f'{sum(e["event"]["payload"]["card"]["id"] == "EV-014" for e in by_type["PLAY"])}.')
        lines += ['', '### Finding classifications', '',
                  '- PASS — One deterministic race completed with recorded state transitions.',
                  '- BALANCE WATCH — Compare observed pacing, Gut Checks, Packs, and deck pressure above against targets; no value changed.',
                  '- RULES REVIEW — RR-11, RR-13, RR-16, RR-17 remain noncanonical playtest assumptions.',
                  '- BUG — see chronological log for any nonblocking anomalies; none was patched.']
    DEST.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    cfg = load_json(ROOT / 'simulation/config.json')
    assert (cfg['seed'], cfg['player_count'], cfg['race_format']) == (20260924, 8, 'marathon')
    sim = RecordedSim(ROOT, cfg)
    error = None
    try:
        sim.run()
    except Exception:
        error = traceback.format_exc()
    report(sim, error)
    print(line_json({'seed': cfg['seed'], 'completed': error is None and len(sim.finish) == 8,
                     'round': sim.round, 'finish': sim.finish,
                     'error': error.splitlines()[-1] if error else None,
                     'events': len(sim.audit_events), 'audit_path': str(DEST),
                     'audit_bytes': DEST.stat().st_size}))


if __name__ == '__main__':
    main()
