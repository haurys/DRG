"""Build race_cards-weather-gear.json: weather Gear gets a Condition job, plus second copies.

Playtest draft for the Race Day Forecast. Slotted weather Gear also prevents a matching
Condition when it is drawn (condition_prevention components, read by the engine):
  Singlet, All-Weather Cap -> Heat Exhaustion;  Tech Shirt, Weather Shell -> Cold Chills.
With --copies, Glare Shades, Singlet and Weather Shell get a second copy (deck 108 -> 111).
Run from the repo root: python simulation/variants/build_weather_gear.py [--copies]
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
cards = json.loads((ROOT / 'data/race_cards.json').read_text(encoding='utf-8'))

PREVENTS = {'Singlet': ('Heat Exhaustion', 'Prevent Heat Exhaustion'),
            'All-Weather Cap': ('Heat Exhaustion', 'Prevent Heat Exhaustion'),
            'Tech Shirt': ('Cold Chills', 'Prevent Cold Chills'),
            'Weather Shell': ('Cold Chills', 'Prevent Cold Chills')}
COPIES = {'Glare Shades': 'GE-021', 'Singlet': 'GE-022', 'Weather Shell': 'GE-023'}

for card in cards:
    if card['family'] == 'Gear' and card['title'] in PREVENTS:
        condition, text = PREVENTS[card['title']]
        card['effect_components'] = card['effect_components'] + [
            {'type': 'condition_prevention', 'condition': condition}]
        card['effect_text'] = f"{card['effect_text']}; {text}"

copies = '--copies' in sys.argv
if copies:
    by_title = {card['title']: card for card in cards if card['family'] == 'Gear'}
    for title, new_id in COPIES.items():
        extra = copy.deepcopy(by_title[title])
        extra['id'] = new_id
        cards.append(extra)

name = 'race_cards-weather-gear-copies.json' if copies else 'race_cards-weather-gear.json'
(ROOT / 'simulation/variants' / name).write_text(json.dumps(cards, indent=2, ensure_ascii=False) + '\n',
                                                 encoding='utf-8')
print(name, len(cards), 'cards')
