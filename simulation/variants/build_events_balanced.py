"""Build race_cards-events-balanced.json: 13 good / 13 bad / 4 rival Events (playtest draft).

Good Events keep their printed Effects (engine logic by card id) at low Effort.
Bad Events hurt the player who plays them and carry high Effort; new ones use
data-driven `generic_effect` (self_move, self_energy, self_choice, field_energy).
Rival Events keep their printed attack and add a `self_cost` paid by the player.
Run from the repo root: python simulation/variants/build_events_balanced.py
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
cards = json.loads((ROOT / 'data/race_cards.json').read_text(encoding='utf-8'))

# Good (13): existing id -> new Effort.
GOOD = {'EV-003': 2, 'EV-004': 3, 'EV-008': 2, 'EV-013': 3, 'EV-023': 1, 'EV-014': 2,
        'EV-007': 2, 'EV-024': 1, 'EV-021': 1, 'EV-015': 2, 'EV-018': 3, 'EV-019': 2,
        'EV-027': 2}
# Rival (4): existing attack id -> (Effort, cost to the player, added effect text).
RIVAL = {'EV-001': (4, {'self_energy': -1}, 'You -⚡'),
         'EV-011': (4, {'self_energy': -1}, 'You -⚡'),
         'EV-025': (4, {'self_move': -1}, 'You -→'),
         'EV-030': (4, {'self_move': -1}, 'You -→')}
# Bad kept from the printed set: existing id -> new Effort.
BAD_KEPT = {'EV-006': 6, 'EV-010': 6, 'EV-005': 6, 'EV-009': 6}
# Bad new: replaced id -> (new id, title, Effort, effect text, generic effect)
BAD_NEW = {
    'EV-026': ('EV-101', 'Porta-Potty', 7, '-→→; +⚡', {'self_move': -2, 'self_energy': 1}),
    'EV-002': ('EV-103', 'Crosswind', 6, 'Everyone on your mile -⚡', {'field_energy': -1}),
    'EV-012': ('EV-104', 'Uneven Pavement', 5, '-→ or -⚡', {'self_choice': True}),
    'EV-022': ('EV-106', 'Wrong Turn', 8, '-→→', {'self_move': -2}),
    'EV-029': ('EV-107', 'Too Many Donuts', 6, '-⚡', {'self_energy': -1}),
    'EV-020': ('EV-108', 'Dropped Gel', 6, '-⚡', {'self_energy': -1}),
    'EV-016': ('EV-109', 'Crowd Surge', 5, '-→', {'self_move': -1}),
    'EV-028': ('EV-110', 'Distracting Sign', 6, '-→ or -⚡', {'self_choice': True}),
    'EV-017': ('EV-111', 'Shoe Malfunction', 8, '-→→', {'self_move': -2}),
}
out = []
for card in cards:
    cid = card['id']
    if card['family'] != 'Event':
        out.append(card)
    elif cid in GOOD:
        out.append({**card, 'effort': GOOD[cid], 'event_balance': 'good'})
    elif cid in RIVAL:
        effort, cost, text = RIVAL[cid]
        out.append({**card, 'effort': effort, 'self_cost': cost, 'event_balance': 'rival',
                    'effect_text': f"{card['effect_text']}; {text}"})
    elif cid in BAD_KEPT:
        out.append({**card, 'effort': BAD_KEPT[cid], 'event_balance': 'bad'})
    else:
        new_id, title, effort, text, effect = BAD_NEW[cid]
        new = copy.deepcopy(card)
        new.update(id=new_id, title=title, effort=effort, effect_text=text, effect_target='SELF',
                   effect_type='generic', effect_components=[], generic_effect=effect,
                   event_balance='bad', replaces=cid)
        out.append(new)
events = [c for c in out if c['family'] == 'Event']
balance = [c['event_balance'] for c in events]
assert len(events) == 30 and (balance.count('good'), balance.count('bad'), balance.count('rival')) == (13, 13, 4)
(ROOT / 'simulation/variants/race_cards-events-balanced.json').write_text(
    json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('wrote', len(out), 'cards')
