"""Observation-only Run 02 recorder. Executes the canonical Sim exactly once."""

import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import simulate as engine  # noqa: E402

spec = importlib.util.spec_from_file_location('run_01_recorder', ROOT / 'audit/run_01_recorder.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)

DEST = ROOT / 'DRG-Marathon-Audit-Run-02.md'
RUN_01 = ROOT / 'DRG-Marathon-Audit-Run-01.md'
RUN_01_HASH = '8fced76c0c5ea168981974b6c29c52b66bba76641e9cbaaeff2cb3cbe1843b71'


class Run02Sim(prior.RecordedSim):
    def __init__(self, root, cfg):
        super().__init__(root, cfg)
        self.legality_records = []

    def record_legality(self, runner, phase, selected, rejected, context=None):
        self.legality_records.append({
            'round': self.round, 'next_engine_event_sequence': self.seq + 1,
            'runner': runner['player_id'], 'phase': phase,
            'selected': selected, 'rejected': rejected,
            'context': context or {},
            'state': self.runner_snapshot(runner),
        })

    def choose_pace(self, runner):
        options, selected = super().choose_pace(runner)
        maximum = self.maximum_legal_pace(runner)
        rejected = [{'pace': pace, 'reason': f'Condition maximum {maximum}'}
                    for pace in engine.PACE_ORDER
                    if engine.PACE_ORDER.index(pace) > engine.PACE_ORDER.index(maximum)]
        self.record_legality(runner, 'Round Start Pace', selected, rejected,
                             {'scored_legal_options': options})
        return options, selected

    def choose_treat_prepare(self, runner):
        attempted = []
        for card in runner['hand']:
            if card['family'] == 'Fuel':
                if card['title'] == 'Electrolytes' and self.condition_by_title(runner, 'Dehydrated'):
                    attempted.append({'card_id': card['id'], 'action': 'fuel'})
                if card['title'] == 'Salt Tabs' and self.condition_by_title(runner, 'Cramp'):
                    attempted.append({'card_id': card['id'], 'action': 'fuel', 'choice': 'remedy'})
        for card in runner['hand']:
            if card['title'] in engine.ATTACHMENT:
                target = self.condition_by_title(runner, engine.ATTACHMENT[card['title']][0])
                if target:
                    attempted.append({'card_id': card['id'], 'action': 'attach',
                                      'condition_id': target['id']})
        for card in runner['hand']:
            if card['family'] == 'Training' and len(runner['active_training']) < 3:
                attempted.append({'card_id': card['id'], 'action': 'training'})
            if (card['family'] == 'Gear' and card['title'] not in engine.ATTACHMENT
                    and len(runner['equipped_gear']) < 3):
                attempted.append({'card_id': card['id'], 'action': 'gear'})
        if runner['energy'] <= 9:
            attempted.extend({'card_id': card['id'], 'action': 'fuel'}
                             for card in runner['hand']
                             if card['family'] == 'Fuel' and card.get('energy'))
        rejected = [{'plan': plan, 'reason': 'Fuel unavailable under active Stomach Trouble'
                     if plan['action'] == 'fuel' and not self.fuel_available(runner)
                     else 'Treat/Prepare legality check'}
                    for plan in attempted if not self.legal_treat_prepare(runner, plan)]
        selected = super().choose_treat_prepare(runner)
        self.record_legality(runner, 'Treat/Prepare', selected, rejected,
                             {'candidate_count': len(attempted), 'legal_candidate_count':
                              sum(self.legal_treat_prepare(runner, plan) for plan in attempted)})
        if selected is not None and not self.legal_treat_prepare(runner, selected):
            raise prior.BlockingAuditBug('AI selected illegal Treat/Prepare plan')
        return selected

    def choose_movement_cards(self, runner, available_plays):
        rejected = []
        for card in runner['hand']:
            if card.get('effort') is None:
                rejected.append({'card': card['id'], 'reason': 'no printed Movement Effort'})
            elif card['id'] == 'EV-020' and not engine.helpful_runner_playable(card, self.round):
                rejected.append({'card': card['id'], 'reason': 'Helpful Runner replay lock'})
            elif card['id'] in engine.OTHER_EVENTS and self.event_target(runner) is None:
                rejected.append({'card': card['id'], 'reason': 'no unlocked eligible OTHER target'})
        selected = super().choose_movement_cards(runner, available_plays)
        self.record_legality(runner, 'Movement cards', [c['id'] for c in selected], rejected,
                             {'card_play_allowance': available_plays,
                              'event_count': sum(c['family'] == 'Event' for c in selected)})
        if len(selected) > available_plays or sum(c['family'] == 'Event' for c in selected) > 1:
            raise prior.BlockingAuditBug('AI selected cards beyond play/Event limits')
        return selected

    def after_movement_events(self, runner, played, held_states):
        if any(card['id'] == 'EV-020' for card in played):
            eligible = [other['player_id'] for other in self.runners
                        if other is not runner and not other['finished'] and not other['finish_pending']
                        and len(other['hand']) < 7]
            rejected = [{'runner': other['player_id'], 'hand_size': len(other['hand']),
                         'reason': 'full hand or finished'}
                        for other in self.runners if other is not runner and other['player_id'] not in eligible]
            self.record_legality(runner, 'Helpful Runner recipient', eligible[0] if eligible else None,
                                 rejected, {'eligible': eligible})
        return super().after_movement_events(runner, played, held_states)


def render_legality(sim):
    lines = ['## AI legality-filter audit', '',
             'These are observation-only records of the canonical AI decisions. Rejected candidates '
             'were excluded before selection; each entry includes the contemporaneous runner state.', '']
    for row in sim.legality_records:
        lines.append(f'- Round {row["round"]}, {row["runner"]}, {row["phase"]} '
                     f'(before engine event {row["next_engine_event_sequence"]}): '
                     f'`{prior.line_json({"selected": row["selected"], "rejected": row["rejected"],
                                          "context": row["context"], "state": row["state"]})}`')
    return '\n'.join(lines) + '\n\n'


def save_report(sim, error):
    prior.DEST = DEST
    try:
        prior.report(sim, error)
        content = DEST.read_text(encoding='utf-8')
        content = content.replace('# DRG Marathon Audit Run 01', '# DRG Marathon Audit Run 02', 1)
        marker = '## Chronological full turn and state-transition log'
        content = content.replace(marker, render_legality(sim) + marker, 1)
        DEST.write_text(content, encoding='utf-8')
    except Exception:
        fallback = ['# DRG Marathon Audit Run 02 — recorder rendering failure', '',
                    '## Original race exception', '', '```text', error or 'none', '```',
                    '## Rendering exception', '', '```text', traceback.format_exc(), '```',
                    '## Exact state and chronological emissions', '']
        for event in sim.audit_events:
            fallback.append(prior.line_json(event))
        DEST.write_text('\n'.join(fallback) + '\n', encoding='utf-8')


def main():
    assert hashlib.sha256(RUN_01.read_bytes()).hexdigest() == RUN_01_HASH
    assert not DEST.exists(), 'Run 02 output already exists; refuse overwrite/re-execution'
    cfg = engine.load_json(ROOT / 'simulation/config.json')
    assert (cfg['seed'], cfg['player_count'], cfg['race_format']) == (20260924, 8, 'marathon')
    sim = Run02Sim(ROOT, cfg)
    error = None
    try:
        sim.run()
    except Exception:
        error = traceback.format_exc()
    save_report(sim, error)
    assert hashlib.sha256(RUN_01.read_bytes()).hexdigest() == RUN_01_HASH
    print(prior.line_json({'seed': cfg['seed'], 'completed': error is None and len(sim.finish) == 8,
                           'round': sim.round, 'finish': sim.finish,
                           'error': error.splitlines()[-1] if error else None,
                           'events': len(sim.audit_events), 'legality_records': len(sim.legality_records),
                           'audit_path': str(DEST), 'audit_bytes': DEST.stat().st_size}))


if __name__ == '__main__':
    main()
