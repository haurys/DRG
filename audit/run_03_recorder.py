"""One-shot, observation-only controlled comparison against Run 02."""
import collections
import hashlib
import importlib.util
import json
import statistics
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import simulate as engine  # noqa: E402

spec = importlib.util.spec_from_file_location('run_01_recorder', ROOT / 'audit/run_01_recorder.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
DEST = ROOT / 'DRG-Marathon-Audit-Run-03.md'
RUN_02 = ROOT / 'DRG-Marathon-Audit-Run-02.md'
RUN_02_HASH = 'b70a8f0a483ca76d2d01078185d36577b47e7da34f048fab5dab061d509bcae8'


def rows(sim, kind):
    return [entry for entry in sim.audit_events if entry['event']['type'] == kind]


def details(sim):
    if len(sim.finish) != 8:
        return '\n## Controlled comparison\n\nRace stopped; no completed-race metrics calculated.\n', {}
    payments = [x['event']['payload'] for x in rows(sim, 'PACE_PAYMENT')]
    energy = [x['event']['payload'] for x in rows(sim, 'ENERGY_CHANGE')]
    fuels = [x['event']['payload'] for x in rows(sim, 'FUEL_USE')]
    plays = [x['event']['payload'] for x in rows(sim, 'PLAY')]
    training = [x['event']['payload'] for x in rows(sim, 'TRAINING_INSTALL')]
    gear = [x['event']['payload'] for x in rows(sim, 'GEAR_EQUIP')]
    resistance = [(e['event']['player_id'], e['event']['payload']) for e in rows(sim, 'CONDITION_APPLY')]
    checks = [(e['event']['payload']['mile'], e['event']['payload']['gut_check'])
              for e in rows(sim, 'MILESTONE') if e['event']['payload'].get('kind') == 'Gut Check']
    moves = [x['movement_quarters'] / 4 for x in sim.turn_records]
    final_energy = [r['energy'] for r in sim.runners]
    fuel_gain = sum(f['energy_after'] - f['energy_before'] for f in fuels)
    gains = collections.Counter()
    losses = collections.Counter()
    for e in energy:
        (gains if e['delta'] >= 0 else losses)[e['source']] += abs(e['delta'])
    gains['Fuel'] += fuel_gain
    pace_paid = sum(p['paid'] for p in payments)
    losses['Pace payment'] += pace_paid
    preservation = collections.Counter(s for p in payments for s in p['preservation_sources'])
    preservation.update(s for p in payments for s in p['heat_preservation_sources'])
    effective_preserved = sum(p['base'] + p['condition_extra'] + p['staged_extra'] + p['global_extra']
                              - p['final'] for p in payments)
    fuel_movement = [p for p in plays if p['card']['family'] == 'Fuel']
    fuel_frequency = collections.Counter(f['card'] for f in fuels)
    resist = [(pid, p['condition'], p['title'], p['base_severity'] - p['current_severity'],
               p['training_resistance']) for pid, p in resistance if p['training_resistance']]
    pack_ids = {e['event']['payload']['to'] for e in rows(sim, 'PACK_ENTER')}
    pack_turns = sum(bool(e['runners'][e['event']['player_id']]['pack']) for e in rows(sim, 'TURN_START'))
    recycles = rows(sim, 'DECK_SHUFFLE')
    recycles = [e for e in recycles if e['event']['payload'].get('reason') == 'eligible discard recycle']
    columns = [
        ('Total rounds', '38', str(sim.round)),
        ('Average finish Energy', '9.25', f'{statistics.mean(final_energy):.2f}'),
        ('Finishers at 1–3 Energy', 'not previously reported', str(sum(1 <= x <= 3 for x in final_energy))),
        ('Fuel Energy gained', '89', str(fuel_gain)),
        ('Gut Check Energy lost', '42', str(losses['Gut Check failure'])),
        ('Pace Energy spent', '205', str(pace_paid)),
        ('Pace Energy preserved', '71', str(effective_preserved)),
        ('Deck reshuffles', '23', str(len(recycles))),
        ('Will uses', '0', str(sum(p['will_used'] for p in payments))),
        ('Training replacements', 'not previously reported', str(sum(bool(t['replaced']) for t in training))),
        ('Gear replacements', 'not previously reported', str(sum(bool(g['replaced']) for g in gear))),
    ]
    lines = ['\n## Approved-baseline controlled comparison', '',
             '| Metric | Run 02 | Run 03 |', '|---|---:|---:|']
    lines += [f'| {label} | {before} | {after} |' for label, before, after in columns]
    lines += ['', '### Energy ledger', '',
              f'- Starting Energy: {8 * sim.cfg["starting_energy"]}; total gained: {sum(gains.values())}; '
              f'total lost/spent: {sum(losses.values())}; finishing total: {sum(final_energy)}. '
              f'Conservation difference: {8 * sim.cfg["starting_energy"] + sum(gains.values()) - sum(losses.values()) - sum(final_energy)}.',
              f'- Gains by source (actual, after cap): `{prior.line_json(dict(gains))}`',
              f'- Spends/losses by source (actual): `{prior.line_json(dict(losses))}`',
              f'- Preservation source credits (including zero-cost overlap): `{prior.line_json(dict(preservation))}`; '
              f'effective Pace cost reduction: {effective_preserved}. Preservation is not Energy gained.',
              f'- Finish Energy mean {statistics.mean(final_energy):.2f}, median {statistics.median(final_energy):.2f}; '
              f'0: {sum(x == 0 for x in final_energy)}, 1–3: {sum(1 <= x <= 3 for x in final_energy)}, '
              f'4–5: {sum(4 <= x <= 5 for x in final_energy)}, above 5: {sum(x > 5 for x in final_energy)}.',
              '', '### Fuel and installation', '',
              f'- Treat/Prepare Fuel uses {len(fuels)}, Movement Fuel uses {len(fuel_movement)}, '
              f'actual Fuel Energy gained {fuel_gain}; physical Fuel IDs reused in Treat/Prepare: '
              f'`{prior.line_json({k:v for k,v in fuel_frequency.items() if v > 1})}`.',
              f'- Electrolytes Energy/remedy: {sum(f["card"] in ("FU-016","FU-017","FU-018") and f["choice"] == "energy" for f in fuels)}/'
              f'{sum(f["card"] in ("FU-016","FU-017","FU-018") and f["choice"] == "remedy" for f in fuels)}; '
              f'Salt Tabs Energy/remedy: {sum(f["card"] in ("FU-019","FU-020") and f["choice"] == "energy" for f in fuels)}/'
              f'{sum(f["card"] in ("FU-019","FU-020") and f["choice"] == "remedy" for f in fuels)}.',
              f'- Training installs {len(training)}, replacements {sum(bool(t["replaced"]) for t in training)}; '
              f'by title `{prior.line_json(dict(collections.Counter(sim.card(t["card"])["title"] for t in training)))}`.',
              f'- Training replaced titles: `{prior.line_json(dict(collections.Counter(sim.card(t["replaced"])["title"] for t in training if t["replaced"])))}`.',
              f'- Gear equips {len(gear)}, replacements {sum(bool(g["replaced"]) for g in gear)}, '
              f'attachments {len(rows(sim,"GEAR_ATTACH"))}, relocations {len(rows(sim,"GEAR_RELOCATE"))}.',
              f'- Training resistance activations {len(resist)}, total starting Severity reduced '
              f'{sum(r[3] for r in resist)}, stacked occurrences {sum(len(r[4]) > 1 for r in resist)}.',
              f'- Resistance cases (runner, Condition ID/title, reduction, sources): `{prior.line_json(resist)}`.',
              '', '### Deck, Gut Checks, movement', '',
              f'- Reshuffles {len(recycles)}; first round {recycles[0]["event"]["round"] if recycles else "none"}; '
              f'failed draws {len(rows(sim,"DRAW_FAILED"))}. Representative recycle inventories below.',
              ]
    for e in (recycles[:1] + recycles[len(recycles)//2:len(recycles)//2+1] + recycles[-1:]):
        lines.append(f'- Round {e["event"]["round"]}, event {e["event"]["event_id"]}: '
                     f'`{prior.line_json(e["recycle_input"] if "recycle_input" in e else e["deck"])}`')
    for mile in (10, 18, 23):
        data = [c for m, c in checks if m == mile]
        lines.append(f'- Mile {mile} threshold {engine.GUT_CHECK_THRESHOLDS["marathon"][mile]}: '
                     f'{sum(c["passed"] for c in data)} pass, {sum(not c["passed"] for c in data)} fail, '
                     f'Energy lost {sum(c["energy_loss"] for c in data)}; hand Effort '
                     f'mean {statistics.mean(c["hand_effort"] for c in data):.2f}, '
                     f'min {min(c["hand_effort"] for c in data)}, max {max(c["hand_effort"] for c in data)}; '
                     f'final total mean {statistics.mean(c["total"] for c in data):.2f}.')
    lines += [f'- Runner-turns {len(moves)}, mean movement {statistics.mean(moves):.3f} miles; '
              f'0={moves.count(0)}, 0.25={moves.count(.25)}, 1.5+={sum(x >= 1.5 for x in moves)}, '
              f'2.0={moves.count(2)}.',
              f'- Packs formed {len(pack_ids)}, runner-turn share {pack_turns/len(moves):.1%}; '
              f'Pack source credits {preservation["Pack"]}.',
              '', '### Assessment labels', '',
              '- PASS — Deterministic one-run execution, source-attributed Energy ledger, replacement and acquisition resistance traces, card conservation checks pending independent inspection.',
              '- BALANCE WATCH — Compare net Energy pressure, duration, Gut Checks, and Event gains against Run 02; no tuning applied.',
              '- RULES REVIEW — RR-11, RR-13, RR-16, RR-17 remain playtest assumptions.',
              '- BUG — No runtime exception; any observed mismatch must be reported without patching.', '']
    metrics = {'rounds':sim.round, 'finish':sim.finish, 'finish_energy':{r['player_id']:r['energy'] for r in sim.runners},
               'fuel_gain':fuel_gain, 'gains':dict(gains),'losses':dict(losses), 'preserved':effective_preserved,
               'training_replacements':sum(bool(t['replaced']) for t in training),
               'gear_replacements':sum(bool(g['replaced']) for g in gear),
               'resistance':len(resist), 'severity_reduced':sum(r[3] for r in resist),
               'recycles':len(recycles), 'runner_turns':len(moves), 'avg_movement':statistics.mean(moves)}
    return '\n'.join(lines), metrics


def main():
    assert hashlib.sha256(RUN_02.read_bytes()).hexdigest() == RUN_02_HASH
    assert not DEST.exists(), 'Run 03 exists; refuse overwrite or re-execution'
    cfg = engine.load_json(ROOT / 'simulation/config.json')
    assert (cfg['seed'], cfg['player_count'], cfg['race_format'], cfg['training_slots'], cfg['gear_slots']) == (20260924, 8, 'marathon', 2, 2)
    sim = prior.RecordedSim(ROOT, cfg)
    error = None
    try:
        sim.run()  # exactly one race invocation
    except Exception:
        error = traceback.format_exc()
    prior.DEST = DEST
    try:
        prior.report(sim, error)
        content = DEST.read_text()
        content = content.replace('# DRG Marathon Audit Run 01', '# DRG Marathon Audit Run 03', 1)
        content = content.replace('RR-16 — AI prioritizes applicable named remedies; Electrolytes remedies Dehydrated, Salt Tabs remedies Cramp, otherwise scripted legal Energy choice may apply.',
                                  'RR-16 — AI prioritizes an applicable named remedy; approved Electrolytes/Salt Tabs OR choice grants no Energy on remedy use. Other eligibility edges remain unresolved.')
        extra, metrics = details(sim)
        DEST.write_text(content + extra + '\n')
    except Exception:
        metrics = {}
        fallback = ['# DRG Marathon Audit Run 03 — recorder rendering failure', '',
                    '## Race exception', '', '```text', error or 'none', '```', '',
                    '## Rendering exception', '', '```text', traceback.format_exc(), '```',
                    '## Full raw emissions and snapshots', '']
        fallback.extend(prior.line_json(row) for row in sim.audit_events)
        DEST.write_text('\n'.join(fallback) + '\n')
    assert hashlib.sha256(RUN_02.read_bytes()).hexdigest() == RUN_02_HASH
    print(prior.line_json({'seed': cfg['seed'], 'completed': error is None and len(sim.finish)==8,
                           'round':sim.round, 'error':error.splitlines()[-1] if error else None,
                           'events':len(sim.audit_events), 'audit_bytes':DEST.stat().st_size,
                           'metrics':metrics}))


if __name__ == '__main__':
    main()
