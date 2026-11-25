"""Run a multi-seed batch of DRG races at several player counts and summarize race length.

Usage (from the repo root):
    python tools/run_baseline.py --players 4 6 8 --seeds 50 --output output/baseline

Each race uses simulation/config.json unchanged except for in-memory player_count and seed.
The same seed list is used for every player count so later rule changes can be compared
race-for-race. Results: races.jsonl (one row per race), summary.json and Baseline-Summary.md.
"""
import argparse
import collections
import json
import statistics
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.simulate import Sim, load_json  # noqa: E402

FIRST_SEED = 1001


def card_id(payload):
    card = payload.get('card')
    if isinstance(card, dict):
        return card.get('id')
    return None


def run_race(args):
    player_count, seed, config_path, overrides = args
    cfg = load_json(ROOT / config_path)
    cfg.update(overrides)
    cfg['player_count'] = player_count
    cfg['seed'] = seed
    started = time.time()
    sim = Sim(ROOT, cfg)
    sim.ai_rationale_enabled = True
    try:
        sim.run()
        error = None
    except Exception as exc:  # record and keep the batch going
        error = {'type': type(exc).__name__, 'message': str(exc),
                 'traceback': traceback.format_exc(limit=4)}
    counts = collections.Counter(event['type'] for event in sim.events)
    card_plays = collections.Counter()
    for event in sim.events:
        if event['type'] in ('PLAY', 'FUEL_USE', 'TRAINING_INSTALL', 'GEAR_EQUIP', 'GEAR_ATTACH'):
            cid = card_id(event.get('payload') or {})
            if cid:
                card_plays[cid] += 1
    finishers = [r for r in sim.runners if r['finished'] or r.get('finish_round')]
    finish_rounds = sorted(r['finish_round'] for r in finishers if r.get('finish_round'))
    dnfs = [r for r in sim.runners if r.get('dnf')]
    records = sim.turn_records
    moves = [rec['movement_quarters'] for rec in records]
    runner_turns = len(records)
    return {
        'players': player_count, 'seed': seed, 'error': error,
        'rounds': sim.round,
        'first_finish_round': finish_rounds[0] if finish_rounds else None,
        'last_finish_round': finish_rounds[-1] if finish_rounds else None,
        'finishers': len(finish_rounds), 'dnfs': len(dnfs),
        'dnf_reasons': dict(collections.Counter(r['dnf_reason'] for r in dnfs)),
        'dnf_distances': [r['distance_completed'] for r in dnfs],
        'runner_turns': runner_turns,
        'avg_quarters_per_turn': statistics.mean(moves) if moves else 0,
        'zero_move_turns': sum(1 for m in moves if m == 0),
        'deck_reshuffles': max(counts['DECK_SHUFFLE'] - 1, 0),
        'energy_stops': counts['ENERGY_STOP'],
        'gut_stops': counts['GUT_MOVEMENT_STOP'],
        'gut_recoveries': counts['GUT_RECOVERY_START'],
        'will_uses': counts['WILL_USE'],
        'pack_entries': counts['PACK_ENTER'],
        'events': len(sim.events),
        'card_plays': dict(card_plays),
        'pace_counts': dict(collections.Counter(e['payload'].get('selected_pace') for e in sim.events
                                                if e['type'] == 'PACE_PAYMENT')),
        'winner_profile': next((r['profile'] for r in sim.runners if r.get('finish_order') == 1), None),
        'seconds': round(time.time() - started, 2),
    }


def pct(values, q):
    values = sorted(values)
    if not values:
        return None
    k = (len(values) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def summarize(rows, all_card_ids):
    out = {}
    for players in sorted({r['players'] for r in rows}):
        group = [r for r in rows if r['players'] == players]
        ok = [r for r in group if not r['error']]

        def stat(key):
            vals = [r[key] for r in ok if r[key] is not None]
            if not vals:
                return None
            return {'mean': round(statistics.mean(vals), 2), 'median': pct(vals, 0.5),
                    'p10': pct(vals, 0.1), 'p90': pct(vals, 0.9), 'min': min(vals), 'max': max(vals)}

        gaps = [r['last_finish_round'] - r['first_finish_round'] for r in ok
                if r['first_finish_round'] is not None]
        total_runners = sum(players for _ in ok)
        reasons = collections.Counter()
        for r in ok:
            reasons.update(r['dnf_reasons'])
        plays = collections.Counter()
        for r in ok:
            plays.update(r['card_plays'])
        paces = collections.Counter()
        for r in ok:
            paces.update(r.get('pace_counts', {}))
        pace_total = sum(paces.values()) or 1
        per_runner = lambda key: round(sum(r[key] for r in ok) / total_runners, 2) if total_runners else None
        out[players] = {
            'races': len(group), 'errors': len(group) - len(ok),
            'error_messages': sorted({r['error']['message'] for r in group if r['error']})[:5],
            'rounds_to_first_finish': stat('first_finish_round'),
            'rounds_to_last_finish': stat('last_finish_round'),
            'total_rounds': stat('rounds'),
            'finish_gap_rounds': {'mean': round(statistics.mean(gaps), 2), 'median': pct(gaps, 0.5),
                                  'max': max(gaps)} if gaps else None,
            'finish_rate': round(sum(r['finishers'] for r in ok) / total_runners, 3) if total_runners else None,
            'races_with_no_finisher': sum(1 for r in ok if r['finishers'] == 0),
            'dnf_reasons': dict(reasons),
            'avg_miles_per_turn': round(statistics.mean(r['avg_quarters_per_turn'] for r in ok) / 4, 3) if ok else None,
            'zero_move_turn_share': round(sum(r['zero_move_turns'] for r in ok) /
                                          max(sum(r['runner_turns'] for r in ok), 1), 3),
            'deck_reshuffles_per_race': round(statistics.mean(r['deck_reshuffles'] for r in ok), 2) if ok else None,
            'energy_stops_per_runner': per_runner('energy_stops'),
            'gut_stops_per_runner': per_runner('gut_stops'),
            'will_uses_per_runner': per_runner('will_uses'),
            'pace_share': {k: round(v / pace_total, 3) for k, v in sorted(paces.items(), key=lambda kv: -kv[1])},
            'winner_profiles': dict(collections.Counter(r['winner_profile'] for r in ok)),
            'never_played_cards': sorted(set(all_card_ids) - set(plays)),
            'most_played_cards': plays.most_common(5),
        }
    return out


def render(summary, seeds, config_path):
    lines = ['# DRG Baseline Simulation Summary', '',
             f'Config: `{config_path}`; player_count and seed set in memory. '
             f'Seeds {FIRST_SEED}–{FIRST_SEED + seeds - 1} at every player count.', '']
    header = '| Metric | ' + ' | '.join(f'{p} players' for p in summary) + ' |'
    lines += [header, '|---|' + '---|' * len(summary)]

    def row(label, fn):
        cells = []
        for s in summary.values():
            try:
                cells.append(fn(s))
            except Exception:
                cells.append('—')
        lines.append(f'| {label} | ' + ' | '.join(cells) + ' |')

    fmt = lambda d: f"{d['median']:.0f} (p10 {d['p10']:.0f}, p90 {d['p90']:.0f})" if d else '—'
    row('Races completed / errors', lambda s: f"{s['races'] - s['errors']} / {s['errors']}")
    row('Round of first finish, median', lambda s: fmt(s['rounds_to_first_finish']))
    row('Round of last finish, median', lambda s: fmt(s['rounds_to_last_finish']))
    row('Total rounds (all finished or DNF), median', lambda s: fmt(s['total_rounds']))
    row('Gap first→last finisher, mean rounds', lambda s: f"{s['finish_gap_rounds']['mean']:.1f}")
    row('Finish rate', lambda s: f"{s['finish_rate']:.0%}")
    row('Races with no finisher', lambda s: str(s['races_with_no_finisher']))
    row('DNF reasons', lambda s: ', '.join(f'{k} {v}' for k, v in s['dnf_reasons'].items()) or 'none')
    row('Average miles per turn', lambda s: f"{s['avg_miles_per_turn']:.2f}")
    row('Turns with zero movement', lambda s: f"{s['zero_move_turn_share']:.0%}")
    row('Deck reshuffles per race', lambda s: f"{s['deck_reshuffles_per_race']:.1f}")
    row('Energy stops per runner', lambda s: f"{s['energy_stops_per_runner']:.2f}")
    row('Gut Check stops per runner', lambda s: f"{s['gut_stops_per_runner']:.2f}")
    row('Will uses per runner', lambda s: f"{s['will_uses_per_runner']:.2f}")
    row('Pace choices', lambda s: ', '.join(f'{k} {v:.0%}' for k, v in s['pace_share'].items()))
    row('Cards never played', lambda s: str(len(s['never_played_cards'])))
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, nargs='+', default=[4, 6, 8])
    parser.add_argument('--seeds', type=int, default=50)
    parser.add_argument('--config', default='simulation/config.json')
    parser.add_argument('--output', default='output/baseline')
    parser.add_argument('--workers', type=int, default=None)
    parser.add_argument('--set', action='append', default=[], metavar='KEY=JSON',
                        help='override a top-level config value, e.g. --set quarters_per_space=2')
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    overrides = {}
    for item in args.set:
        key, _, value = item.partition('=')
        overrides[key] = json.loads(value)
    jobs = [(p, FIRST_SEED + i, args.config, overrides) for p in args.players for i in range(args.seeds)]
    rows = []
    started = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as pool, open(out / 'races.jsonl', 'w') as stream:
        for row in pool.map(run_race, jobs):
            rows.append(row)
            stream.write(json.dumps(row) + '\n')
            stream.flush()
            done = len(rows)
            if done % 10 == 0 or row['error']:
                flag = f" ERROR {row['error']['message']}" if row['error'] else ''
                print(f'{done}/{len(jobs)} done ({time.time() - started:.0f}s){flag}', flush=True)
    # Condition cards are drawn and applied, never played, so they are left out of "never played".
    cards_path = overrides.get('race_cards_path') or load_json(ROOT / args.config).get(
        'race_cards_path', 'data/race_cards.json')
    all_ids = [card['id'] for card in load_json(ROOT / cards_path)
               if card.get('family') != 'Condition']
    summary = summarize(rows, all_ids)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    label = args.config + (' with ' + ', '.join(args.set) if args.set else '')
    (out / 'Baseline-Summary.md').write_text(render(summary, args.seeds, label), encoding='utf-8')
    print(render(summary, args.seeds, label))


if __name__ == '__main__':
    main()
