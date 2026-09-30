#!/usr/bin/env python3
"""Deterministic, audit-first DRG engine with integrated live-turn rules."""
from pathlib import Path
import argparse, collections, copy, hashlib, itertools, json, random, statistics

PACE_ORDER = ['Easy', 'Steady', 'Race', 'Push']
MILESTONES = {
    'marathon': {'Water': [4, 8, 12, 16, 20, 24], 'Aid/Fuel': [8, 16, 24], 'Gut Check': [10, 18, 23]},
    'half': {'Water': [3, 6, 9], 'Aid/Fuel': [6], 'Gut Check': [6, 11]},
}
GUT_CHECK_THRESHOLDS = {'marathon': {10: 25, 18: 30, 23: 35}, 'half': {6: 9, 11: 11}}
CONDITION_DEFS = {
    'Cramp': (4, False), 'Tight Calf': (3, True), 'Dead Legs': (5, True),
    'Blister': (3, True), 'Hot Spot': (2, True), 'Sore Feet': (4, True),
    'Dehydrated': (5, False), 'Nausea': (4, False), 'Gashed Knee': (5, False),
    'Side Stitch': (3, False), 'Twisted Ankle': (7, True), 'Heat Exhaustion': (8, False),
    'Cold Chills': (5, False),
}
TRAINING_DURATION = {}
GEAR_DURATION = {'Tempo Shoes': 5, 'Carbon Racers': 3, 'GPS Watch': 2}
FOOTWEAR = {'Running Shoes', 'Cushioned Shoes', 'Trail Shoes', 'Tempo Shoes', 'Carbon Racers'}
ATTACHMENT = {'Running Socks': ('Blister', 2), 'Compression Sleeves': ('Cramp', 2),
              'Recovery Sleeves': ('Tight Calf', 1)}
TRAINING_RESISTANCE = {
    'Long Run': {'Dead Legs': 2},
    'Base Miles': {'Dead Legs': 1, 'Tight Calf': 1},
    'Strength Training': {'Cramp': 1, 'Tight Calf': 1},
    'Pacing Practice': {'Side Stitch': 2},
    'Form Drills': {'Hot Spot': 1, 'Sore Feet': 1},
}
OTHER_EVENTS = {'EV-001', 'EV-002', 'EV-011', 'EV-012', 'EV-019', 'EV-025', 'EV-030'}
DIRECT_PLUS = {'EV-003', 'EV-004', 'EV-008', 'EV-013', 'EV-019', 'EV-023', 'EV-027'}
AFTER_ENERGY = {'EV-007': 1, 'EV-015': 1, 'EV-016': 1, 'EV-021': 3, 'EV-022': 3,
                'EV-024': 2, 'EV-028': 1, 'EV-029': 1}
EVENT_COVERAGE = {
    'EV-001': 'NEXT_ROUND_OTHER', 'EV-002': 'NEXT_ROUND_OTHER',
    'EV-003': 'CURRENT_DIRECT', 'EV-004': 'CURRENT_DIRECT', 'EV-005': 'COURSE',
    'EV-006': 'SELF_NEXT_ROUND', 'EV-007': 'ENERGY_GAIN', 'EV-008': 'CURRENT_DIRECT',
    'EV-009': 'CURRENT_DIRECT_LOSS', 'EV-010': 'SELF_NEXT_ROUND',
    'EV-011': 'NEXT_ROUND_OTHER_CHOICE', 'EV-012': 'NEXT_ROUND_OTHER_CHOICE',
    'EV-013': 'CURRENT_DIRECT', 'EV-014': 'CURRENT_IGNORE_DIFFICULTY',
    'EV-015': 'IMMEDIATE_ENERGY_SELF_OTHER', 'EV-016': 'IMMEDIATE_ENERGY_SELF_OTHER', 'EV-017': 'AFTER_CYCLE',
    'EV-018': 'IMMEDIATE_PACK_ENERGY', 'EV-019': 'CURRENT_DIRECT_OTHER',
    'EV-020': 'OTHER_ENERGY', 'EV-021': 'ENERGY_GAIN', 'EV-022': 'ENERGY_GAIN',
    'EV-023': 'CURRENT_DIRECT', 'EV-024': 'IMMEDIATE_ENERGY',
    'EV-025': 'NEXT_ROUND_OTHER', 'EV-026': 'CURRENT_DIRECT_ENERGY_GAIN',
    'EV-027': 'CURRENT_DIRECT', 'EV-028': 'IMMEDIATE_ENERGY', 'EV-029': 'IMMEDIATE_ENERGY',
    'EV-030': 'NEXT_ROUND_OTHER',
}


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def load_json(path):
    with open(path, encoding='utf-8') as stream:
        return json.load(stream)


def movement(result):
    if result <= 0:
        return 0
    if result >= 15:
        return 8
    return (result + 1) // 2


def movement_energy_cost(card):
    """The physical card's printed expenditure applies only to Movement use."""
    effort = card.get('effort')
    if effort is None:
        raise ValueError('Condition cannot be used for Movement')
    return 0 if effort <= 3 else 1 if effort <= 6 else 2


def card_effort(card):
    return (card.get('effort') or 0) if card.get('use_mode', 'MOVEMENT') == 'MOVEMENT' else 0


def active_effect_cards(cards):
    return [card for card in cards if card.get('use_mode', 'MOVEMENT') == 'EFFECT']


def calculate_total_effort(cards, modes):
    return sum((card.get('effort') or 0) for card, mode in zip(cards, modes)
               if mode in ('MOVEMENT', 'EFFORT'))


def make_condition(card):
    base, persistent = CONDITION_DEFS[card['title']]
    assert card.get('severity') == base and card.get('effort') is None
    return {'id': card['id'], 'title': card['title'], 'base_severity': base,
            'current_severity': base, 'suppression': 0, 'effective_severity': base,
            'persistent': persistent, 'attachments': []}


def update_effective_severity(condition):
    condition['effective_severity'] = max(0, condition['current_severity'] - condition.get('suppression', 0))
    return condition


def set_suppression(condition, amount):
    condition['suppression'] = max(0, amount)
    return update_effective_severity(condition)


def apply_remedy(condition, remedy):
    if remedy == 'Aid' and condition['title'] in ('Twisted Ankle', 'Heat Exhaustion'):
        condition['current_severity'] = max(0, condition['current_severity'] -
                                            (3 if condition['title'] == 'Twisted Ankle' else 4))
        update_effective_severity(condition)
        return condition if condition['persistent'] or condition['current_severity'] else None
    allowed = {('Dehydrated', 'Electrolytes'), ('Dehydrated', 'Water'), ('Cramp', 'Salt Tabs'),
               ('Nausea', 'Aid'), ('Gashed Knee', 'Aid')}
    if (condition['title'], remedy) not in allowed:
        return condition
    condition['current_severity'] = 0
    update_effective_severity(condition)
    return condition if condition['persistent'] else None


def condition_effects(condition, pace=None, surface=None):
    severity = condition.get('effective_severity', 0)
    title = condition['title']
    result = {'effort_penalty': 0, 'difficulty_penalty': 0, 'direct_movement': 0, 'extra_energy': 0,
              'max_pace': None, 'push_available': True, 'fuel_available': True,
              'fuel_energy_penalty': 0}
    if severity <= 0:
        return result
    if title in ('Hot Spot', 'Side Stitch', 'Dead Legs') and pace in ('Race', 'Push'):
        result['direct_movement'] = -1
    if title == 'Gashed Knee':
        result['direct_movement'] = -1
    if title == 'Sore Feet' and surface in ('Concrete', 'Asphalt'):
        result['difficulty_penalty'] = 2
    if title == 'Cramp':
        result['push_available'] = False
    if title in ('Tight Calf', 'Blister') and pace == 'Push':
        result['extra_energy'] = 1
    if title == 'Dehydrated' and pace in ('Steady', 'Race', 'Push'):
        result['extra_energy'] = 1
    if title == 'Cold Chills' and pace in ('Race', 'Push'):
        result['extra_energy'] = 1
    if title == 'Twisted Ankle':
        result['max_pace'] = 'Steady'
    if title == 'Heat Exhaustion':
        result['max_pace'] = 'Easy'
    if title == 'Nausea':
        result['fuel_available'] = False
    return result


def anti_chafe_prevents(title, active):
    return active and title == 'Hot Spot'


def training_difficulty_reduction(title, elevation):
    if title == 'Hill Repeats':
        return {'Incline': 2, 'Steep Incline': 1}.get(elevation, 0)
    if title == 'Downhill Practice':
        return {'Descent': 2, 'Steep Descent': 1}.get(elevation, 0)
    return 0


def effective_difficulty(segment, conditions=(), training=(), course_bonus=0):
    penalties = sum(condition_effects(c, surface=segment.get('surface'))['difficulty_penalty'] for c in conditions)
    reductions = sum(training_difficulty_reduction(t, segment.get('elevation')) for t in training)
    return max(0, segment['difficulty'] + penalties + course_bonus - reductions)


def gut_check(hand, active_training=(), active_gear=(), threshold=0):
    cards = [card for card in hand if card.get('family') != 'Condition']
    hand_effort = sum(card.get('effort') or 0 for card in cards)
    modifier_sources = ([{'card': title, 'value': value} for title in active_training
                         for name, value in (('Strength Training', 1), ('Mental Toughness', 3))
                         if title == name]
                        + [{'card': 'Pace Band', 'value': 2} for title in active_gear
                           if title == 'Pace Band'])
    modifiers = sum(source['value'] for source in modifier_sources)
    total = hand_effort + modifiers
    return {'cards': [{'id': card['id'], 'title': card['title'], 'effort': card.get('effort') or 0}
                      for card in cards],
            'hand_effort': hand_effort, 'modifiers': modifiers,
            'modifier_sources': modifier_sources, 'total': total,
            'threshold': threshold, 'passed': total >= threshold,
            'energy_loss': 0 if total >= threshold else 2}


def tough_decision_cycle(hand, event_id='EV-017', limit=2):
    eligible = [card for card in hand if card['id'] != event_id]
    return eligible[:min(limit, len(eligible))]


def sudden_rain(card_id, current_mile, total_miles, round_number):
    if current_mile >= total_miles:
        return None
    return {'source_card': card_id, 'affected_mile': current_mile + 1,
            'start_round': round_number, 'remaining_duration': 4,
            'expiry_round': round_number + 4, 'difficulty_bonus': 1}


def tick_course_events(events):
    for event in events:
        event['remaining_duration'] -= 1
    return [event for event in events if event['remaining_duration'] > 0]


def course_event_bonus(events, mile):
    return sum(event['difficulty_bonus'] for event in events
               if event['affected_mile'] == mile and event['remaining_duration'] > 0)


def apply_trade(a, b, card_a, card_b, limit=3):
    if a['exchanges_used'] >= limit or b['exchanges_used'] >= limit:
        return False
    a['hand'].remove(card_a)
    b['hand'].remove(card_b)
    a['hand'].append(card_b)
    b['hand'].append(card_a)
    a['exchanges_used'] += 1
    b['exchanges_used'] += 1
    a.setdefault('locked_ids', set()).add(card_b['id'])
    b.setdefault('locked_ids', set()).add(card_a['id'])
    return True


def recycle_discard(draw, discard, rng, in_play_ids=(), audit=None):
    if draw:
        return True
    blocked = set(in_play_ids)
    eligible = [card for card in discard if card['id'] not in blocked]
    if not eligible:
        return False
    discard[:] = [card for card in discard if card['id'] in blocked]
    rng.shuffle(eligible)
    draw.extend(eligible)
    if audit is not None:
        audit.append({'eligible_count': len(eligible), 'excluded_count': len(discard)})
    return True


def resolve_movement(start_space, movement_result, difficulties, course_quarters,
                     turn_cap=8, direct_movement=0):
    """Resolve Base Movement with boundary deltas, then distinct Direct Movement."""
    pos, remaining, moved, boundaries = start_space, movement_result, 0, []
    while remaining > 0 and moved < turn_cap and pos < course_quarters:
        segment = min(pos // 4, len(difficulties) - 1)
        boundary = min((segment + 1) * 4, course_quarters)
        distance_to_boundary = boundary - pos
        possible = movement(remaining)
        if possible < distance_to_boundary:
            step = min(possible, turn_cap - moved, course_quarters - pos)
            pos += step
            moved += step
            remaining -= step * 2
            break
        step = min(distance_to_boundary, turn_cap - moved, course_quarters - pos)
        pos += step
        moved += step
        remaining -= step * 2
        if step < distance_to_boundary or pos >= course_quarters:
            break
        previous, new = difficulties[segment], difficulties[segment + 1]
        change, before = new - previous, remaining
        adjustment_applied = remaining > 0 and moved < turn_cap
        if adjustment_applied:
            remaining -= change
        boundaries.append({
            'boundary_space': pos, 'boundary_mile': pos / 4,
            'movement_result_used': step * 2, 'remaining_before_adjustment': before,
            'previous_difficulty': previous, 'new_difficulty': new,
            'difficulty_change': change, 'adjustment_applied': adjustment_applied,
            'adjusted_remaining': remaining,
            'stopped': adjustment_applied and remaining <= 0,
            'stop_reason': ('harder_terrain' if adjustment_applied and remaining <= 0 and change > 0
                            else 'movement_result_exhausted' if not adjustment_applied and remaining <= 0
                            else 'turn_cap' if not adjustment_applied and moved >= turn_cap else None),
        })
        if remaining <= 0 or moved >= turn_cap:
            break
    base_moved = moved
    direct = max(-base_moved, direct_movement)
    direct_applied = max(-base_moved, min(direct, turn_cap - base_moved, course_quarters - pos))
    pos += direct_applied
    moved += direct_applied
    unused_direct = max(0, direct_movement - max(0, direct_applied))
    cap_prevented = moved >= turn_cap and pos < course_quarters and remaining > 0
    return {
        'from_space': start_space, 'to_space': pos, 'quarter_miles': moved,
        'base_quarter_miles': base_moved, 'direct_quarter_miles': direct_applied,
        'direct_requested': direct_movement, 'direct_remaining': unused_direct,
        'movement_result': movement_result, 'remaining_result': remaining,
        'positive_finish_movement': pos >= course_quarters and (remaining > 0 or unused_direct > 0),
        'boundaries': boundaries, 'cap_prevented': cap_prevented,
        'cap_prevented_quarters': movement(remaining) if cap_prevented else 0,
        'result_wasted_above_cap': max(0, remaining) if cap_prevented else 0,
    }


def public_runner(runner):
    result = {key: value for key, value in runner.items() if key != 'hand'}
    if isinstance(result.get('locked_ids'), set):
        result['locked_ids'] = sorted(result['locked_ids'])
    return result


class Sim:
    def __init__(self, root, cfg):
        self.root, self.cfg = root, cfg
        self.rng = random.Random(cfg['seed'])
        self.events, self.seq, self.round = [], 0, 0
        self.cards = load_json(root / 'data/race_cards.json')
        self.course_cards = load_json(root / 'data/course_cards.json')
        self.profiles = load_json(root / 'simulation/players.json')
        self.draw, self.discard, self.course, self.runners = [], [], [], []
        self.finish, self.pending_finishers, self.turn_records = [], [], []
        self.course_events, self.global_events = [], []
        self.deck_audit, self.round_pack_snapshot = [], {}
        self.ai_rationale_enabled = True
        self.ai_decisions = []

    def emit(self, event_type, player=None, payload=None, state=None):
        self.seq += 1
        event = {'event_id': f'EV-{self.seq:06d}', 'sequence': self.seq,
                 'type': event_type, 'round': self.round, 'player_id': player,
                 'payload': payload or {}, 'state': state or {}}
        self.events.append(event)
        return event

    def card(self, card_id):
        return next(card for card in self.cards if card['id'] == card_id)

    def cardview(self, card):
        return {key: card.get(key) for key in ['id', 'title', 'family', 'effort', 'severity',
                                               'movement_energy_cost', 'movement_energy_icon',
                                               'energy', 'effect_text']}

    def build_course(self):
        by_card = {}
        for side in self.course_cards:
            by_card.setdefault(side['course_card_id'], {})[side['side']] = side
        count = 13 if self.cfg['race_format'] == 'marathon' else 7
        selected = self.rng.sample(sorted(by_card), count)
        self.rng.shuffle(selected)
        oriented = []
        for position, card_id in enumerate(selected, 1):
            flip = self.rng.choice([False, True])
            outbound, returning = ('B', 'A') if flip else ('A', 'B')
            oriented.append((position, card_id, outbound, returning))
            self.emit('COURSE_SELECT', payload={'position': position, 'course_card_id': card_id})
            self.emit('COURSE_ORIENT', payload={'position': position, 'course_card_id': card_id,
                                                'outbound_side': outbound, 'return_side': returning})
        if self.cfg['race_format'] == 'marathon':
            mapping = ([(position, by_card[card_id][outbound]) for position, card_id, outbound, _ in oriented]
                       + [(27 - position, by_card[card_id][returning])
                          for position, card_id, _, returning in reversed(oriented)])
        else:
            mapping = ([(position, by_card[card_id][outbound]) for position, card_id, outbound, _ in oriented]
                       + [(14 - position, by_card[card_id][returning])
                          for position, card_id, _, returning in reversed(oriented[:-1])])
        self.course = []
        for mile, segment in sorted(mapping):
            item = copy.deepcopy(segment)
            item['mile'] = mile
            item['quarter_positions'] = [(mile - 1) * 4 + index for index in range(1, 5)]
            self.course.append(item)
        for kind, miles in MILESTONES[self.cfg['race_format']].items():
            for mile in miles:
                self.course[mile - 1].setdefault('milestones', []).append(kind)

    def new_runner(self, index, profile, hand):
        colors = ['Blue', 'Orange', 'Green', 'Purple', 'Red', 'Yellow', 'Teal', 'Black']
        stats = {key: 0 for key in ['cards_drawn', 'cards_played', 'cards_discarded', 'total_effort_used',
                                    'energy_gained', 'energy_spent', 'conditions_drawn', 'conditions_treated',
                                    'distance_moved', 'zero_movement_turns', 'deck_exchanges', 'pack_entries',
                                    'pack_exits', 'will_used', 'treat_prepare_actions', 'events_played']}
        return {
            'player_id': f'P{index + 1}', 'player_name': profile, 'profile': profile,
            'color': colors[index % len(colors)], 'race_turn_number': 0, 'round': 0,
            'distance_completed': 0.0, 'quarter_mile_space': 0,
            'current_course_card': self.course[0]['course_card_id'],
            'current_course_side': self.course[0]['side'], 'current_mile': 1,
            'current_difficulty': self.course[0]['difficulty'], 'pace': 'Easy',
            'previous_pace': None, 'energy': self.cfg['starting_energy'], 'will_available': True,
            'hand': hand, 'active_conditions': [], 'active_training': [],
            'equipped_gear': [], 'attached_gear': [], 'staged_events': [],
            'active_effects': [], 'pack_state': None, 'pack_members_snapshot': [],
            'pack_leader': None, 'finished': False, 'finish_pending': False,
            'finish_order': None, 'finish_turn': None, 'finish_round': None,
            'locked_ids': set(), 'exchanges_used': 0, 'stats': stats,
        }

    def setup(self):
        self.build_course()
        non_conditions = [copy.deepcopy(card) for card in self.cards if card['family'] != 'Condition']
        conditions = [copy.deepcopy(card) for card in self.cards if card['family'] == 'Condition']
        self.rng.shuffle(non_conditions)
        profiles = (self.profiles * ((self.cfg['player_count'] + 7) // 8))[:self.cfg['player_count']]
        for index, profile in enumerate(profiles):
            hand = [non_conditions.pop() for _ in range(self.cfg['starting_hand'])]
            runner = self.new_runner(index, profile['profile'], hand)
            self.runners.append(runner)
            self.emit('DEAL', runner['player_id'], {'cards': [self.cardview(card) for card in hand]},
                      {'private_hand': [card['id'] for card in hand]})
        surrendered = []
        expected_draw_value = statistics.mean(self.prevalue(card) for card in self.cards
                                               if card['family'] != 'Condition')
        for runner in self.runners:
            while runner['exchanges_used'] < self.cfg['exchange_limit'] and non_conditions:
                eligible = [card for card in runner['hand'] if card['id'] not in runner['locked_ids']]
                if not eligible:
                    break
                old = min(eligible, key=self.prevalue)
                if self.prevalue(old) >= expected_draw_value:
                    break
                new = non_conditions.pop()
                runner['hand'].remove(old)
                runner['hand'].append(new)
                runner['locked_ids'].add(new['id'])
                runner['exchanges_used'] += 1
                runner['stats']['deck_exchanges'] += 1
                surrendered.append(old)
                self.emit('DECK_EXCHANGE', runner['player_id'], {'surrendered': old['id'],
                          'replacement': new['id'], 'locked': new['id'],
                          'exchanges_used': runner['exchanges_used']})
        non_conditions.extend(surrendered)
        non_conditions.extend(conditions)
        self.rng.shuffle(non_conditions)
        self.draw = non_conditions
        self.emit('DECK_SHUFFLE', payload={'seed': self.cfg['seed'], 'remaining_count': len(self.draw)})

    def prevalue(self, card):
        # Before the race, no replacement identity or future draw is visible.
        # Keep printed Movement Effort foremost; recovery is a small tie-break.
        return (card.get('effort') or 0) * 10 + (card.get('energy') or 0)

    def locate(self, runner):
        quarter = min(runner['quarter_mile_space'], len(self.course) * 4 - 1)
        segment = self.course[quarter // 4]
        runner['current_mile'] = segment['mile']
        runner['current_course_card'] = segment['course_card_id']
        runner['current_course_side'] = segment['side']
        runner['current_difficulty'] = segment['difficulty']

    def installed_titles(self, runner, kind):
        key = 'active_training' if kind == 'training' else 'equipped_gear'
        return [item['card']['title'] for item in runner[key]]

    def anti_chafe_active(self, runner):
        return 'Anti-Chafe' in self.installed_titles(runner, 'gear')

    def in_play_ids(self):
        ids = set()
        for runner in self.runners:
            ids.update(card['id'] for card in runner['hand'])
            ids.update(item['card']['id'] for item in runner['active_training'])
            ids.update(item['card']['id'] for item in runner['equipped_gear'])
            ids.update(item['card']['id'] for item in runner['attached_gear'])
            ids.update(condition['id'] for condition in runner['active_conditions'])
            ids.update(event['card']['id'] for event in runner['staged_events'])
        ids.update(event['source_card'] for event in self.course_events)
        ids.update(event['card']['id'] for event in self.global_events)
        return ids

    def refill(self):
        if self.draw:
            return True
        audit = []
        if not recycle_discard(self.draw, self.discard, self.rng, self.in_play_ids(), audit):
            self.emit('DRAW_FAILED', payload={'reason': 'draw and eligible discard empty'})
            return False
        row = audit[-1]
        self.deck_audit.append(row)
        self.emit('DECK_SHUFFLE', payload={'reason': 'eligible discard recycle',
                                          'count': len(self.draw), **row})
        return True

    def draw_one(self, runner, replacement=False):
        if not self.refill():
            return None
        card = self.draw.pop()
        runner['stats']['cards_drawn'] += 1
        self.emit('REPLACEMENT_DRAW' if replacement else 'DRAW', runner['player_id'],
                  {'card': self.cardview(card), 'draw_count': len(self.draw),
                   'discard_count': len(self.discard)})
        if card['family'] == 'Condition':
            runner['stats']['conditions_drawn'] += 1
            if anti_chafe_prevents(card['title'], self.anti_chafe_active(runner)):
                self.discard.append(card)
                self.emit('CONDITION_PREVENT', runner['player_id'],
                          {'condition': card['id'], 'source': 'Anti-Chafe'})
                return self.draw_one(runner, True)
            condition = make_condition(card)
            reductions = [{'card': item['card']['id'], 'title': item['card']['title'],
                           'amount': TRAINING_RESISTANCE.get(item['card']['title'], {}).get(card['title'], 0)}
                          for item in runner['active_training']]
            reductions = [item for item in reductions if item['amount']]
            condition['current_severity'] = max(0, condition['base_severity']
                                                - sum(item['amount'] for item in reductions))
            update_effective_severity(condition)
            runner['active_conditions'].append(condition)
            self.emit('CONDITION_APPLY', runner['player_id'],
                      {'condition': card['id'], **condition, 'training_resistance': reductions})
            if condition['current_severity'] == 0 and not condition['persistent']:
                self.discard_condition(runner, condition, 'acquisition severity zero')
            return self.draw_one(runner, True)
        runner['hand'].append(card)
        return card

    def replenish(self, runner):
        normal_draws, before = 0, len(runner['hand'])
        while len(runner['hand']) < 7 and normal_draws < 2:
            card = self.draw_one(runner)
            if card is None:
                break
            normal_draws += 1
        self.emit('REPLENISH', runner['player_id'], {'hand_before': before,
                  'normal_cards_drawn': normal_draws, 'hand_after': len(runner['hand'])})
        return normal_draws

    def condition_by_title(self, runner, title):
        return next((condition for condition in runner['active_conditions'] if condition['title'] == title), None)

    def discard_condition(self, runner, condition, reason):
        if condition in runner['active_conditions']:
            runner['active_conditions'].remove(condition)
        for item in list(runner['attached_gear']):
            if item['condition_id'] == condition['id']:
                runner['attached_gear'].remove(item)
                item['condition_id'] = None
                item['amount'] = 0
                if len(runner['equipped_gear']) < self.cfg['gear_slots'] and not (
                        item['card']['title'] in FOOTWEAR and
                        any(entry['card']['title'] in FOOTWEAR for entry in runner['equipped_gear'])):
                    runner['equipped_gear'].append(item)
                    destination = 'equipped'
                else:
                    runner['hand'].append(item['card'])
                    destination = 'hand'
                self.emit('GEAR_DETACH', runner['player_id'], {'card': item['card']['id'],
                          'condition': condition['id'], 'destination': destination,
                          'policy': 'PLAYTEST ASSUMPTION after Condition removal'})
        self.discard.append(copy.deepcopy(self.card(condition['id'])))
        self.emit('CONDITION_REMOVE', runner['player_id'], {'condition': condition['id'], 'reason': reason})

    def recompute_suppression(self, runner, condition):
        total = sum(item['amount'] for item in runner['attached_gear'] if item['condition_id'] == condition['id'])
        before = condition['effective_severity']
        set_suppression(condition, total)
        self.emit('CONDITION_SUPPRESSION', runner['player_id'], {'condition': condition['id'],
                  'suppression': total, 'effective_before': before,
                  'effective_after': condition['effective_severity']})

    def install_training(self, runner, card, replace_id=None):
        replaced = None
        if len(runner['active_training']) >= self.cfg['training_slots']:
            replaced = next((item for item in runner['active_training']
                             if item['card']['id'] == replace_id), None)
            if replaced is None:
                raise ValueError('Training replacement required')
            runner['active_training'].remove(replaced)
            self.discard.append(replaced['card'])
        entry = {'card': card, 'remaining_turns': TRAINING_DURATION.get(card['title'])}
        runner['active_training'].append(entry)
        self.emit('TRAINING_INSTALL', runner['player_id'], {'card': card['id'],
                  'remaining_turns': entry['remaining_turns'],
                  'replaced': replaced['card']['id'] if replaced else None})
        options = TRAINING_RESISTANCE.get(card['title'], {})
        matching = [condition for condition in runner['active_conditions']
                    if condition['title'] in options and condition['current_severity'] > 0]
        if matching:
            target = max(matching, key=lambda condition: (condition['effective_severity'], condition['id']))
            before = target['current_severity']
            target['current_severity'] = max(0, before - options[target['title']])
            update_effective_severity(target)
            self.emit('CONDITION_SEVERITY_CHANGE', runner['player_id'], {'source': card['id'],
                      'condition': target['id'], 'current_before': before,
                      'current_after': target['current_severity'],
                      'effective_after': target['effective_severity']})
            if target['current_severity'] == 0 and not target['persistent']:
                self.discard_condition(runner, target, 'Training installation reduction')

    def equip_gear(self, runner, card, replace_id=None):
        replaced = None
        if card['title'] in FOOTWEAR:
            existing = next((item for item in runner['equipped_gear']
                             if item['card']['title'] in FOOTWEAR), None)
            if existing:
                runner['equipped_gear'].remove(existing)
                self.discard.append(existing['card'])
                replaced = existing
        if replaced is None and len(runner['equipped_gear']) >= self.cfg['gear_slots']:
            replaced = next((item for item in runner['equipped_gear']
                             if item['card']['id'] == replace_id), None)
            if replaced is None:
                raise ValueError('Gear replacement required')
            runner['equipped_gear'].remove(replaced)
            self.discard.append(replaced['card'])
        entry = {'card': card, 'remaining_turns': GEAR_DURATION.get(card['title'])}
        runner['equipped_gear'].append(entry)
        self.emit('GEAR_EQUIP', runner['player_id'], {'card': card['id'],
                  'remaining_turns': entry['remaining_turns'],
                  'replaced': replaced['card']['id'] if replaced else None})

    def attach_gear(self, runner, card, condition):
        required, amount = ATTACHMENT[card['title']]
        if condition['title'] != required:
            return False
        entry = {'card': card, 'condition_id': condition['id'], 'amount': amount,
                 'remaining_turns': GEAR_DURATION.get(card['title'])}
        runner['attached_gear'].append(entry)
        condition['attachments'].append(card['id'])
        self.recompute_suppression(runner, condition)
        self.emit('GEAR_ATTACH', runner['player_id'], {'card': card['id'],
                  'condition': condition['id'], 'suppression': amount})
        return True

    def remove_gear(self, runner, item, reason='expired'):
        collection = runner['attached_gear'] if item in runner['attached_gear'] else runner['equipped_gear']
        collection.remove(item)
        self.discard.append(item['card'])
        condition = next((c for c in runner['active_conditions']
                          if c['id'] == item.get('condition_id')), None)
        if condition:
            if item['card']['id'] in condition['attachments']:
                condition['attachments'].remove(item['card']['id'])
            self.recompute_suppression(runner, condition)
        self.emit('GEAR_REMOVE', runner['player_id'], {'card': item['card']['id'], 'reason': reason})

    def treat_condition(self, runner, condition, effort):
        before = condition['current_severity']
        condition['current_severity'] = max(0, before - effort)
        update_effective_severity(condition)
        runner['stats']['conditions_treated'] += 1
        self.emit('CONDITION_TREAT', runner['player_id'], {'condition': condition['id'],
                  'effort': effort, 'current_before': before,
                  'current_after': condition['current_severity'],
                  'effective_after': condition['effective_severity']})
        if condition['current_severity'] == 0 and not condition['persistent']:
            self.discard_condition(runner, condition, 'nonpersistent severity zero')

    def named_remedy(self, runner, condition, remedy):
        result = apply_remedy(condition, remedy)
        self.emit('CONDITION_REMEDY', runner['player_id'], {'condition': condition['id'],
                  'remedy': remedy, 'removed': result is None,
                  'current_severity': 0 if result is None else result['current_severity']})
        if result is None:
            self.discard_condition(runner, condition, f'{remedy} remedy')

    def use_fuel(self, runner, card, choice=None):
        if not self.fuel_available(runner):
            return False
        title = card['title']
        if title in ('Electrolytes', 'Salt Tabs', 'Banana', 'Water Bottle') and choice not in ('energy', 'remedy', 'severity'):
            raise ValueError('Fuel choice required')
        recovery = (card.get('energy') or 0) if choice in (None, 'energy') else 0
        old = runner['energy']
        runner['energy'] = min(15, runner['energy'] + recovery)
        if title == 'Electrolytes' and choice == 'remedy':
            condition = self.condition_by_title(runner, 'Dehydrated')
            if condition:
                self.named_remedy(runner, condition, 'Electrolytes')
        elif title == 'Salt Tabs' and choice == 'remedy':
            condition = self.condition_by_title(runner, 'Cramp')
            if condition:
                self.named_remedy(runner, condition, 'Salt Tabs')
        elif title in ('Banana', 'Water Bottle') and choice == 'severity':
            target = self.condition_by_title(runner, 'Tight Calf' if title == 'Banana' else 'Heat Exhaustion')
            if target:
                self.treat_condition(runner, target, 2)
        self.emit('FUEL_USE', runner['player_id'], {'card': card['id'], 'choice': choice,
                  'energy_before': old, 'energy_after': runner['energy'],
                  'recovery': runner['energy'] - old})
        return True

    def fuel_available(self, runner):
        return all(condition_effects(condition)['fuel_available']
                   for condition in runner['active_conditions'])

    def legal_treat_prepare(self, runner, plan):
        if not plan:
            return True
        card = next((item for item in runner['hand'] if item['id'] == plan.get('card_id')), None)
        if card is None or card['family'] == 'Event':
            return False
        action = plan.get('action')
        if action == 'fuel':
            if card['family'] != 'Fuel' or not self.fuel_available(runner):
                return False
            if card['title'] in ('Electrolytes', 'Salt Tabs'):
                return plan.get('choice') == 'energy' or (
                    plan.get('choice') == 'remedy' and self.condition_by_title(
                        runner, 'Dehydrated' if card['title'] == 'Electrolytes' else 'Cramp') is not None)
            if card['title'] in ('Banana', 'Water Bottle'):
                return plan.get('choice') == 'energy' or (
                    plan.get('choice') == 'severity' and self.condition_by_title(
                        runner, 'Tight Calf' if card['title'] == 'Banana' else 'Heat Exhaustion') is not None)
            return plan.get('choice') in (None, 'energy')
        if action == 'training':
            if card['family'] != 'Training':
                return False
            if len(runner['active_training']) < self.cfg['training_slots']:
                return plan.get('replace_id') is None
            return any(item['card']['id'] == plan.get('replace_id')
                       for item in runner['active_training'])
        if action == 'gear':
            if card['family'] != 'Gear' or card['title'] in ATTACHMENT:
                return False
            footwear = next((item for item in runner['equipped_gear']
                             if item['card']['title'] in FOOTWEAR), None)
            if card['title'] in FOOTWEAR and footwear:
                return plan.get('replace_id') == footwear['card']['id']
            if len(runner['equipped_gear']) < self.cfg['gear_slots']:
                return plan.get('replace_id') is None
            return any(item['card']['id'] == plan.get('replace_id')
                       for item in runner['equipped_gear'])
        if action == 'attach':
            target = next((condition for condition in runner['active_conditions']
                           if condition['id'] == plan.get('condition_id')), None)
            return (card['family'] == 'Gear' and card['title'] in ATTACHMENT
                    and target is not None and target['title'] == ATTACHMENT[card['title']][0]
                    and not target['attachments'])
        return False

    def choose_treat_prepare(self, runner):
        return self.choose_turn_plan(runner)['treat_prepare']

    def treat_candidates(self, runner):
        """Generate legal preparation choices without inspecting any future draw."""
        candidates = [None]
        for card in runner['hand']:
            if card['family'] == 'Fuel':
                if card['title'] == 'Electrolytes' and self.condition_by_title(runner, 'Dehydrated'):
                    candidates.append({'card_id': card['id'], 'action': 'fuel', 'choice': 'remedy'})
                if card['title'] == 'Salt Tabs' and self.condition_by_title(runner, 'Cramp'):
                    candidates.append({'card_id': card['id'], 'action': 'fuel', 'choice': 'remedy'})
                if card['title'] in ('Banana', 'Water Bottle'):
                    target = 'Tight Calf' if card['title'] == 'Banana' else 'Heat Exhaustion'
                    if self.condition_by_title(runner, target):
                        candidates.append({'card_id': card['id'], 'action': 'fuel', 'choice': 'severity'})
        for card in runner['hand']:
            if card['title'] in ATTACHMENT:
                target = self.condition_by_title(runner, ATTACHMENT[card['title']][0])
                if target:
                    candidates.append({'card_id': card['id'], 'action': 'attach', 'condition_id': target['id']})
        for card in runner['hand']:
            if card['family'] == 'Training':
                replacements = ([item['card']['id'] for item in runner['active_training']]
                                if len(runner['active_training']) >= self.cfg['training_slots'] else [None])
                candidates.extend({'card_id': card['id'], 'action': 'training', 'replace_id': old}
                                  for old in replacements)
            if card['family'] == 'Gear' and card['title'] not in ATTACHMENT:
                footwear = next((item for item in runner['equipped_gear'] if item['card']['title'] in FOOTWEAR), None)
                replacements = ([footwear['card']['id']] if card['title'] in FOOTWEAR and footwear
                                else [item['card']['id'] for item in runner['equipped_gear']]
                                if len(runner['equipped_gear']) >= self.cfg['gear_slots'] else [None])
                candidates.extend({'card_id': card['id'], 'action': 'gear', 'replace_id': old}
                                  for old in replacements)
            if card['family'] == 'Fuel':
                candidates.append({'card_id': card['id'], 'action': 'fuel',
                                   'choice': 'energy'})
        return [plan for plan in candidates if self.legal_treat_prepare(runner, plan)]

    def resolve_treat_prepare(self, runner, plan):
        if not plan:
            self.emit('TREAT_PREPARE', runner['player_id'], {'action': 'none'})
            return 0
        if plan['action'] == 'relocate':
            item = next((entry for entry in runner['equipped_gear'] + runner['attached_gear']
                         if entry['card']['id'] == plan['card_id']), None)
            if item is None:
                raise ValueError('Gear relocation source is not installed')
            old_condition = next((condition for condition in runner['active_conditions']
                                  if condition['id'] == item.get('condition_id')), None)
            if item in runner['equipped_gear']:
                runner['equipped_gear'].remove(item)
            else:
                runner['attached_gear'].remove(item)
            if old_condition:
                self.recompute_suppression(runner, old_condition)
            if plan.get('condition_id'):
                condition = next(c for c in runner['active_conditions'] if c['id'] == plan['condition_id'])
                if item['card']['title'] not in ATTACHMENT or not self.attach_gear(runner, item['card'], condition):
                    raise ValueError('incompatible Gear relocation')
                destination = condition['id']
            else:
                self.equip_gear(runner, item['card'])
                destination = 'equipped'
            self.emit('GEAR_RELOCATE', runner['player_id'], {'card': item['card']['id'],
                      'destination': destination, 'card_play_budget': 0,
                      'policy': 'PLAYTEST ASSUMPTION for RR-11'})
            runner['stats']['treat_prepare_actions'] += 1
            return 0
        if not self.legal_treat_prepare(runner, plan):
            raise ValueError('illegal Treat/Prepare action')
        card = next((item for item in runner['hand'] if item['id'] == plan['card_id']), None)
        if card is None or card['family'] == 'Event':
            raise ValueError('illegal Treat/Prepare card')
        runner['hand'].remove(card)
        action = plan['action']
        if action == 'training' and card['family'] == 'Training':
            self.install_training(runner, card, plan.get('replace_id'))
        elif action == 'gear' and card['family'] == 'Gear':
            self.equip_gear(runner, card, plan.get('replace_id'))
        elif action == 'attach' and card['family'] == 'Gear':
            condition = next(c for c in runner['active_conditions'] if c['id'] == plan['condition_id'])
            if not self.attach_gear(runner, card, condition):
                raise ValueError('incompatible Gear attachment')
        elif action == 'fuel' and card['family'] == 'Fuel':
            if not self.use_fuel(runner, card, plan.get('choice')):
                runner['hand'].append(card)
                raise ValueError('Fuel unavailable')
            self.discard.append(card)
        else:
            runner['hand'].append(card)
            raise ValueError('illegal Treat/Prepare action')
        runner['stats']['cards_played'] += 1
        runner['stats']['treat_prepare_actions'] += 1
        self.emit('TREAT_PREPARE', runner['player_id'], {'action': action, 'card': card['id'],
                  'movement_effort': 0})
        return 1

    def maximum_legal_pace(self, runner):
        maximum = 'Push'
        for condition in runner['active_conditions']:
            effect = condition_effects(condition)
            if not effect['push_available']:
                maximum = min(maximum, 'Race', key=PACE_ORDER.index)
            if effect['max_pace']:
                maximum = min(maximum, effect['max_pace'], key=PACE_ORDER.index)
        return maximum

    def choose_pace(self, runner):
        maximum = self.maximum_legal_pace(runner)
        candidates = PACE_ORDER[:PACE_ORDER.index(maximum) + 1]
        scored = []
        for pace in candidates:
            preview = copy.deepcopy(runner)
            preview['pace'] = pace
            preview['pack_state'] = None  # This round's Pack is formed after all Pace choices.
            plan = self.choose_turn_plan(preview)
            pack_style = 0.4 if runner['profile'] == 'Pack Runner' and any(
                other is not runner and not other['finished']
                and abs(other['quarter_mile_space'] - runner['quarter_mile_space']) <= 2
                and (other['previous_pace'] or other['pace']) == pace
                for other in self.runners) else 0
            scored.append({'pace': pace, 'score': plan['score'] + pack_style,
                           'movement_quarters': plan['movement_quarters'],
                           'expected_turns_remaining': plan['expected_turns_remaining']})
        return scored, max(scored, key=lambda item: (item['score'], -PACE_ORDER.index(item['pace'])))['pace']

    def movement_candidates(self, runner, available_plays):
        legal = [card for card in runner['hand'] if card.get('effort') is not None]
        choices = [()]
        for size in range(1, min(available_plays, len(legal)) + 1):
            for combo in itertools.combinations(legal, size):
                if sum(card['family'] == 'Event' for card in combo) > 1:
                    continue
                choices.append(tuple({**card, 'use_mode': 'MOVEMENT'} for card in combo))
                if any(card['family'] == 'Event' for card in combo):
                    event = next(card for card in combo if card['family'] == 'Event')
                    if event['id'] in OTHER_EVENTS and not (
                            self.beneficial_target(runner) if event['id'] == 'EV-019'
                            else self.event_target(runner)):
                        continue
                    if event['id'] in ('EV-015', 'EV-016', 'EV-020') and not self.beneficial_target(runner):
                        continue
                    choices.append(tuple({**card, 'use_mode': 'EFFECT' if card['family'] == 'Event' else 'MOVEMENT'}
                                         for card in combo))
        return choices

    def energy_gains_on_side(self, runner, side):
        """Visible trigger check; future evaluation uses current Pace only as a proxy."""
        gains = []
        for entry in runner['active_training'] + runner['equipped_gear']:
            for effect in entry['card'].get('effect_components', []):
                if effect['type'] != 'energy_gain':
                    continue
                if effect.get('trigger') == 'Water':
                    continue
                applies = all(not effect.get(field) or value in
                              (effect[field] if isinstance(effect[field], list) else [effect[field]])
                              for field, value in [('pace', runner['pace']), ('route', side['route']),
                                                   ('surface', side['surface']), ('elevation', side['elevation'])])
                if applies:
                    gains.append((entry['card']['id'], effect['energy_delta']))
        return gains

    def installed_energy(self, runner):
        """Once per runner-turn, on the Movement's starting Course side and locked Pace."""
        side = self.course[min(runner['quarter_mile_space'] // 4, len(self.course) - 1)]
        return self.energy_gains_on_side(runner, side)

    def apply_installed_energy(self, runner):
        for card_id, amount in self.installed_energy(runner):
            self.apply_energy(runner, amount, f'Installed {card_id}')
            if self.card(card_id)['title'] == 'GPS Watch':
                item = next(i for i in runner['equipped_gear'] if i['card']['id'] == card_id)
                self.emit('GPS_WATCH_TICK', runner['player_id'], {'card': card_id,
                          'round': self.round, 'nominal_gain': amount,
                          'remaining_turns_including_current': item['remaining_turns']})

    def preview_preparation(self, runner, plan):
        projected = copy.deepcopy(runner)
        if not plan:
            return projected
        card = next(c for c in projected['hand'] if c['id'] == plan['card_id'])
        projected['hand'].remove(card)
        action = plan['action']
        if action in ('training', 'gear'):
            zone = projected['active_training'] if action == 'training' else projected['equipped_gear']
            if plan.get('replace_id'):
                zone[:] = [item for item in zone if item['card']['id'] != plan['replace_id']]
            zone.append({'card': card, 'remaining_turns':
                         (TRAINING_DURATION if action == 'training' else GEAR_DURATION).get(card['title'])})
            if action == 'training':
                options = TRAINING_RESISTANCE.get(card['title'], {})
                matching = [c for c in projected['active_conditions']
                            if c['title'] in options and c['current_severity'] > 0]
                if matching:
                    target = max(matching, key=lambda c: (c['effective_severity'], c['id']))
                    target['current_severity'] = max(0, target['current_severity'] - options[target['title']])
                    update_effective_severity(target)
                    if target['current_severity'] == 0 and not target['persistent']:
                        projected['active_conditions'].remove(target)
        elif action == 'attach':
            target = next(c for c in projected['active_conditions'] if c['id'] == plan['condition_id'])
            amount = ATTACHMENT[card['title']][1]
            projected['attached_gear'].append({'card': card, 'condition_id': target['id'],
                                                'amount': amount, 'remaining_turns': None})
            set_suppression(target, target['suppression'] + amount)
        elif action == 'fuel':
            if plan.get('choice') in ('remedy', 'severity'):
                title = 'Dehydrated' if card['title'] == 'Electrolytes' else 'Cramp'
                if plan.get('choice') == 'severity':
                    title = 'Tight Calf' if card['title'] == 'Banana' else 'Heat Exhaustion'
                target = next(c for c in projected['active_conditions'] if c['title'] == title)
                if plan.get('choice') == 'severity':
                    target['current_severity'] = max(0, target['current_severity'] - 2)
                    update_effective_severity(target)
                    if target['current_severity'] == 0 and not target['persistent']:
                        projected['active_conditions'].remove(target)
                elif apply_remedy(target, card['title']) is None:
                    projected['active_conditions'].remove(target)
            else:
                projected['energy'] = min(15, projected['energy'] + (card['energy'] or 0))
        return projected

    def preview_payment(self, runner):
        projected = copy.deepcopy(runner)
        projected['energy'] = min(15, projected['energy'] +
                                  sum(amount for _, amount in self.installed_energy(projected)))
        cost = self.pace_cost(projected, projected['pace'])['final']
        if cost > projected['energy']:
            if projected['will_available']:
                projected['will_available'] = False
                projected['energy'] = 0
            else:
                affordable = [pace for pace in PACE_ORDER[:PACE_ORDER.index(projected['pace']) + 1]
                              if self.pace_cost(projected, pace)['final'] <= projected['energy']]
                projected['pace'] = affordable[-1] if affordable else 'Easy'
                projected['energy'] -= self.pace_cost(projected, projected['pace'])['final']
        else:
            projected['energy'] -= cost
        return projected

    def preview_movement(self, runner, cards):
        """Estimate this legal plan from visible state, without mutation or random draws."""
        course_end = len(self.course) * 4
        index = min(runner['quarter_mile_space'] // 4, len(self.course) - 1)
        segment = self.course[index]
        installed, _ = self.movement_effort_bonus(runner, segment)
        ids = {c['id'] for c in active_effect_cards(cards) if c['family'] == 'Event'}
        event_bonus = 0
        direct = sum(2 if event_id == 'EV-023' else 1 for event_id in ids & DIRECT_PLUS)
        if 'EV-009' in ids or 'EV-026' in ids:
            direct -= 1
        staged_energy_cost = 0
        for staged in self.active_staged(runner):
            event_id = staged['card']['id']
            if event_id == 'EV-019':
                direct += 1
            if event_id in ('EV-001', 'EV-002', 'EV-030'):
                direct -= 1
            if event_id in ('EV-011', 'EV-012', 'EV-025'):
                direct -= 1
        ignored = 'EV-014' in ids
        rain = (sudden_rain('EV-005', segment['mile'], len(self.course), self.round)
                if 'EV-005' in ids else None)
        visible_events = self.course_events + ([rain] if rain else [])
        difficulties = [(0 if ignored else effective_difficulty(
            s, runner['active_conditions'], self.installed_titles(runner, 'training'),
            course_event_bonus(visible_events, s['mile']))) for s in self.course]
        penalty = sum(condition_effects(c, runner['pace'], segment['surface'])['effort_penalty']
                      for c in runner['active_conditions'])
        direct += sum(condition_effects(c, runner['pace'], segment['surface'])['direct_movement']
                      for c in runner['active_conditions'])
        result = (sum(card_effort(c) for c in cards) + installed + event_bonus
                  + self.cfg['pace'][runner['pace']]['modifier'] - penalty
                  - (0 if runner['quarter_mile_space'] >= course_end else difficulties[index]))
        resolved = resolve_movement(runner['quarter_mile_space'], result, difficulties, course_end,
                                    turn_cap=8, direct_movement=direct)
        resolved['staged_energy_cost'] = staged_energy_cost
        resolved['milestone_energy_gain'] = (sum(
            runner['quarter_mile_space'] < mile * 4 <= resolved['to_space']
            for mile in MILESTONES[self.cfg['race_format']]['Water'])
            if 'Hydration Belt' in self.installed_titles(runner, 'gear') else 0)
        return resolved

    def plan_score(self, runner, prepared, paid, plan, cards, movement_result):
        moved = movement_result['quarter_miles']
        remaining = max(0, len(self.course) * 4 - movement_result['to_space'])
        opponents = [r['quarter_mile_space'] for r in self.runners if r['player_id'] != runner['player_id']
                     and not r['finished']]
        gap = max(opponents, default=runner['quarter_mile_space']) - runner['quarter_mile_space']
        progress_weight = 12 + min(2, max(0, gap) / 16)
        turns = remaining / max(2, moved or 2)
        score = progress_weight * moved - remaining / 8 - turns * 0.15
        if movement_result['to_space'] >= len(self.course) * 4 and movement_result['positive_finish_movement']:
            score += 1000
        # Setup pays only over the visible remaining Course. Its card's lost Effort is
        # already charged through the full Movement comparison; replacement removes
        # the old installed effect from this projection.
        if plan and plan['action'] in ('training', 'gear', 'attach'):
            horizon = min(remaining, 24) / 24
            setup_card = next(c for c in runner['hand'] if c['id'] == plan['card_id'])
            duration = (TRAINING_DURATION if plan['action'] == 'training' else GEAR_DURATION).get(
                setup_card['title'])
            if duration:
                horizon *= min(1, duration / 6)
            cost_delta = self.pace_cost(runner, runner['pace'])['final'] - self.pace_cost(prepared, prepared['pace'])['final']
            energy_delta = sum(amount for _, amount in self.installed_energy(prepared)) - sum(
                amount for _, amount in self.installed_energy(runner))
            visible = self.course[min(runner['quarter_mile_space'] // 4, len(self.course) - 1):]
            visible = visible[:min(6, len(visible))]
            effort_delta = (sum(self.movement_effort_bonus(prepared, s)[0]
                                - self.movement_effort_bonus(runner, s)[0]
                                for s in visible) / len(visible)) if visible else 0
            old_titles = self.installed_titles(runner, 'training')
            new_titles = self.installed_titles(prepared, 'training')
            difficulty_delta = (sum(effective_difficulty(s, runner['active_conditions'], old_titles)
                                    - effective_difficulty(s, prepared['active_conditions'], new_titles)
                                    for s in visible) / len(visible)) if visible else 0
            future_sides = visible[1:]
            future_energy_delta = (sum(sum(v for _, v in self.energy_gains_on_side(prepared, s))
                                       - sum(v for _, v in self.energy_gains_on_side(runner, s))
                                       for s in future_sides) / len(future_sides)) if future_sides else 0
            # Already-staged next-round weather is public; unseen weather draws are not.
            water_delta = sum(
                ('Hydration Belt' in self.installed_titles(prepared, 'gear'))
                - ('Hydration Belt' in self.installed_titles(runner, 'gear'))
                for side in future_sides
                if side['mile'] in MILESTONES[self.cfg['race_format']]['Water'])
            weather_next = [e for e in self.global_events if e['activate_round'] == self.round + 1
                            and e['source'] == runner['player_id']]
            weather_preservation = sum(
                any(ef['type'] == 'weather_protection' and
                    {'EV-006': 'Heat', 'EV-010': 'Cold'}.get(event['card']['id']) in ef['weather']
                    for entry in prepared['equipped_gear'] for ef in entry['card'].get('effect_components', []))
                - any(ef['type'] == 'weather_protection' and
                      {'EV-006': 'Heat', 'EV-010': 'Cold'}.get(event['card']['id']) in ef['weather']
                      for entry in runner['equipped_gear'] for ef in entry['card'].get('effect_components', []))
                for event in weather_next)
            score += horizon * (max(-3, min(3, effort_delta)) * 2
                                + max(-3, min(3, difficulty_delta)) * 2
                                + cost_delta * 2 + energy_delta * 2
                                + future_energy_delta * 2 + min(3, water_delta) * 2
                                + weather_preservation * 2)
            score -= 1 - 0.6 * horizon
            if plan['action'] == 'training':
                old_resistance = sum(sum(TRAINING_RESISTANCE.get(title, {}).values()) for title in old_titles)
                new_resistance = sum(sum(TRAINING_RESISTANCE.get(title, {}).values()) for title in new_titles)
                score += horizon * max(-2, min(2, (new_resistance - old_resistance) / 2))
            gut_miles = [mile for mile in MILESTONES[self.cfg['race_format']]['Gut Check']
                         if runner['quarter_mile_space'] < mile * 4]
            if gut_miles:
                old_mod = gut_check([], old_titles, self.installed_titles(runner, 'gear'))['modifiers']
                new_mod = gut_check([], new_titles, self.installed_titles(prepared, 'gear'))['modifiers']
                score += horizon * (new_mod - old_mod)
            if setup_card['title'] == 'Anti-Chafe' and not self.anti_chafe_active(runner):
                score += horizon * 0.5
        if plan and plan['action'] in ('fuel', 'attach'):
            future = {c['id']: c for c in prepared['active_conditions']}
            reduction = sum(max(0, c['effective_severity'] -
                                (future[c['id']]['effective_severity'] if c['id'] in future else 0))
                            for c in runner['active_conditions'])
            caps_removed = sum(4 for c in runner['active_conditions']
                               if c['effective_severity'] > 0 and c['title'] in
                               ('Cramp', 'Twisted Ankle', 'Heat Exhaustion', 'Nausea')
                               and (c['id'] not in future or future[c['id']]['effective_severity'] == 0))
            score += min(remaining, 24) / 24 * min(14, 2 * reduction + caps_removed)
        energy = max(0, paid['energy'] - movement_result['staged_energy_cost'])
        effect_ids = {c['id'] for c in active_effect_cards(cards)}
        event_gain = sum(AFTER_ENERGY.get(c['id'], 0) for c in active_effect_cards(cards))
        if 'EV-026' in effect_ids:
            event_gain += 2
        if 'EV-018' in effect_ids:
            event_gain += 1
        energy = min(15, energy + event_gain + movement_result['milestone_energy_gain'])
        for mile in MILESTONES[self.cfg['race_format']]['Gut Check']:
            if runner['quarter_mile_space'] < mile * 4 <= movement_result['to_space']:
                hand = [c for c in prepared['hand'] if c not in cards]
                check = gut_check(hand, self.installed_titles(prepared, 'training'),
                                  self.installed_titles(prepared, 'gear'),
                                  GUT_CHECK_THRESHOLDS[self.cfg['race_format']][mile])
                energy = max(0, energy - check['energy_loss'])
        score += min(energy, 5) * 0.8 + max(0, energy - 5) * 0.15
        if energy == 0 and remaining > 0:
            score -= 4
        if runner['will_available'] and not paid['will_available']:
            score -= 3
        if remaining:
            held = sum(c.get('effort') or 0 for c in prepared['hand'] if c not in cards)
            score += min(1.0, held * 0.025) * min(1, remaining / 16)
        if runner['profile'] in ('Aggressive', 'Front Runner'):
            score += 0.55 * PACE_ORDER.index(paid['pace'])
        elif runner['profile'] == 'Energy Conservative':
            score += min(1.5, energy * 0.3)
        elif runner['profile'] == 'Pack Runner' and runner['pack_state']:
            score += 0.4
        elif runner['profile'] == 'Course Planner' and plan and plan['action'] == 'training':
            score += 0.2
        elif runner['profile'] == 'Opportunist' and event_gain:
            score += 0.2
        return score, turns

    def choose_turn_plan(self, runner, rationale=None):
        candidates = []
        for plan in self.treat_candidates(runner):
            prepared = self.preview_preparation(runner, plan)
            paid = self.preview_payment(prepared)
            allowance = self.cfg['max_voluntary_plays'] - bool(plan)
            for cards in self.movement_candidates(prepared, allowance):
                if not cards and prepared['hand']:
                    continue
                cost = sum(movement_energy_cost(card) for card in cards
                           if card['use_mode'] == 'MOVEMENT')
                if cost > paid['energy']:
                    continue
                after_cards = copy.deepcopy(paid)
                after_cards['energy'] -= cost
                resolved = self.preview_movement(after_cards, cards)
                score, turns = self.plan_score(runner, prepared, after_cards, plan, cards, resolved)
                candidates.append({'treat_prepare': plan,
                                   'movement_cards': [c['id'] for c in cards],
                                   'card_modes': [c['use_mode'] for c in cards],
                                   'movement_energy_cost': cost,
                                   'movement_quarters': resolved['quarter_miles'],
                                   'expected_turns_remaining': turns, 'score': score})
        if not candidates:
            fallback = {'treat_prepare': None, 'movement_cards': [], 'movement_quarters': 0,
                        'expected_turns_remaining': len(self.course) * 2, 'score': -1000}
            if rationale is not None:
                rationale.update({'candidates': [], 'eligible': [], 'selected': fallback,
                                  'emergency': False})
            return fallback
        all_candidates = candidates
        positive = any(item['movement_quarters'] > 0 for item in candidates)
        emergency = False
        if positive:
            emergency = runner['energy'] <= 1 or any(
                c['effective_severity'] >= 4 for c in runner['active_conditions'])
            if not emergency:
                candidates = [item for item in candidates if item['movement_quarters'] > 0]
        selected = max(candidates, key=lambda item: (item['score'], item['movement_quarters'],
                                                     tuple(item['movement_cards']),
                                                     str(item['treat_prepare'])))
        if rationale is not None:
            rationale.update({'candidates': all_candidates, 'eligible': candidates,
                              'selected': selected, 'emergency': emergency})
        return selected

    def form_packs(self):
        old = {runner['player_id']: runner['pack_state'] for runner in self.runners}
        for runner in self.runners:
            runner['pack_state'] = None
            runner['pack_members_snapshot'] = []
            runner['pack_leader'] = None
        pack_number = 0
        for pace in PACE_ORDER:
            available = sorted((runner for runner in self.runners if not runner['finished'] and runner['pace'] == pace
                                and not any(event['card']['id'] == 'EV-030'
                                            for event in self.active_staged(runner))),
                               key=lambda runner: (-runner['quarter_mile_space'], runner['player_id']))
            while available:
                leader = available.pop(0)
                members = [leader] + [runner for runner in available
                                      if leader['quarter_mile_space'] - runner['quarter_mile_space'] <= 2]
                available = [runner for runner in available if runner not in members]
                if len(members) < 2:
                    continue
                pack_number += 1
                pack_id = f'PACK-R{self.round}-{pack_number}'
                member_ids = [runner['player_id'] for runner in members]
                for runner in members:
                    runner['pack_state'] = pack_id
                    runner['pack_members_snapshot'] = member_ids
                    runner['pack_leader'] = leader['player_id']
        self.round_pack_snapshot = {runner['player_id']: list(runner['pack_members_snapshot']) for runner in self.runners}
        for runner in self.runners:
            if old[runner['player_id']] != runner['pack_state']:
                key = 'pack_entries' if runner['pack_state'] else 'pack_exits'
                runner['stats'][key] += 1
                self.emit('PACK_ENTER' if runner['pack_state'] else 'PACK_EXIT', runner['player_id'],
                          {'from': old[runner['player_id']], 'to': runner['pack_state'],
                           'members': runner['pack_members_snapshot'], 'leader': runner['pack_leader'],
                           'pace_preservation': 1 if runner['pack_state'] else 0})

    def start_round(self, scripted_paces=None):
        self.round += 1
        for runner in self.runners:
            for event in self.active_staged(runner):
                self.emit('STAGED_EVENT_ACTIVATE', runner['player_id'], {'card': event['card']['id'],
                          'source': event['source'], 'target_lock': event.get('target_lock', True)})
        for event in self.global_events:
            if event['activate_round'] == self.round:
                self.emit('GLOBAL_EVENT_ACTIVATE', payload={'card': event['card']['id'],
                          'source': event['source']})
                weather = {'EV-006': 'Heat', 'EV-010': 'Cold'}.get(event['card']['id'])
                if weather:
                    for runner in self.runners:
                        if runner['player_id'] != event['source'] or runner['finished']:
                            continue
                        protector = next((entry['card']['title'] for entry in runner['equipped_gear']
                                          if any(effect['type'] == 'weather_protection'
                                                 and weather in effect['weather']
                                                 for effect in entry['card'].get('effect_components', []))), None)
                        before = runner['energy']
                        if not protector:
                            self.apply_energy(runner, -1, f'{event["card"]["title"]} weather')
                        self.emit('GLOBAL_WEATHER', runner['player_id'], {'card': event['card']['id'],
                                  'weather': weather, 'protected_by': protector,
                                  'energy_before': before, 'energy_after': runner['energy'],
                                  'actual_loss': before - runner['energy']})
        for runner in self.runners:
            if runner['finished']:
                continue
            runner['round_start_position'] = runner['quarter_mile_space']
            runner['previous_pace'] = runner['pace']
            options, selected = self.choose_pace(runner)
            if scripted_paces and runner['player_id'] in scripted_paces:
                selected = scripted_paces[runner['player_id']]
                maximum = self.maximum_legal_pace(runner)
                if PACE_ORDER.index(selected) > PACE_ORDER.index(maximum):
                    selected = maximum
            runner['pace'] = selected
            self.emit('PACE_SELECT', runner['player_id'], {'options': options, 'selected': selected,
                      'maximum_legal': self.maximum_legal_pace(runner)})
        self.form_packs()
        self.emit('ROUND_START', payload={'positions': {runner['player_id']: runner['round_start_position']
                                                        for runner in self.runners if not runner['finished']},
                                          'packs': self.round_pack_snapshot})

    def active_staged(self, runner):
        return [event for event in runner['staged_events'] if event['activate_round'] == self.round]

    def pace_preservation(self, runner, pace):
        sources = []
        if runner['pack_state'] and not any(event['card']['id'] == 'EV-030' for event in self.active_staged(runner)):
            sources.append('Pack')
        training = self.installed_titles(runner, 'training')
        gear = self.installed_titles(runner, 'gear')
        if pace == 'Race' and 'Long Run' in training:
            sources.append('Long Run')
        if pace == 'Steady' and 'Pacing Practice' in training:
            sources.append('Pacing Practice')
        return sources

    def pace_cost(self, runner, pace):
        base = abs(self.cfg['pace'][pace]['energy_cost'])
        condition_extra = sum(condition_effects(condition, pace)['extra_energy']
                              for condition in runner['active_conditions'])
        staged_extra = 0
        sources = self.pace_preservation(runner, pace)
        final = max(0, base + condition_extra + staged_extra - len(sources))
        return {'base': base, 'condition_extra': condition_extra, 'staged_extra': staged_extra,
                'preservation_sources': sources, 'final': final}

    def pay_pace(self, runner):
        maximum = self.maximum_legal_pace(runner)
        if PACE_ORDER.index(runner['pace']) > PACE_ORDER.index(maximum):
            runner['pace'] = maximum
        cost = self.pace_cost(runner, runner['pace'])
        will_used = False
        if cost['final'] > runner['energy']:
            if runner['will_available']:
                will_used = True
                runner['will_available'] = False
                runner['stats']['will_used'] += 1
                paid = runner['energy']
                runner['energy'] = 0
            else:
                affordable = [pace for pace in PACE_ORDER[:PACE_ORDER.index(runner['pace']) + 1]
                              if self.pace_cost(runner, pace)['final'] <= runner['energy']]
                runner['pace'] = affordable[-1] if affordable else 'Easy'
                cost = self.pace_cost(runner, runner['pace'])
                paid = cost['final']
                runner['energy'] -= paid
        else:
            paid = cost['final']
            runner['energy'] -= paid
        runner['stats']['energy_spent'] += paid
        self.emit('PACE_PAYMENT', runner['player_id'], {**cost, 'selected_pace': runner['pace'],
                  'paid': paid, 'will_used': will_used, 'energy_after': runner['energy']})
        return cost, will_used

    def movement_effort_bonus(self, runner, segment):
        # The redesigned installed effects produce Energy or Difficulty changes,
        # never generic Movement Effort.
        return 0, []

    def choose_movement_cards(self, runner, available_plays):
        paid = self.preview_payment(runner)
        choices = self.movement_candidates(runner, available_plays)
        ranked = []
        for cards in choices:
            cost = sum(movement_energy_cost(c) for c in cards if c['use_mode'] == 'MOVEMENT')
            if cost > paid['energy']:
                continue
            after = copy.deepcopy(paid)
            after['energy'] -= cost
            resolved = self.preview_movement(after, cards)
            score, _ = self.plan_score(runner, runner, after, None, cards, resolved)
            ranked.append((score, resolved['quarter_miles'], tuple(c['id'] for c in cards), cards))
        return list(max(ranked, key=lambda row: row[:3])[-1]) if ranked else []

    def event_target(self, source):
        locked = {event['target'] for runner in self.runners for event in runner['staged_events']
                  if event.get('target_lock', True)}
        candidates = [runner for runner in self.runners if runner is not source and not runner['finished']
                      and not runner['finish_pending']
                      and runner['player_id'] not in locked]
        return sorted(candidates, key=lambda runner: (-runner['quarter_mile_space'],
                                                      runner['player_id']))[0] if candidates else None

    def beneficial_target(self, source):
        candidates = [runner for runner in self.runners if runner is not source
                      and not runner['finished'] and not runner['finish_pending']]
        return sorted(candidates, key=lambda runner: runner['player_id'])[0] if candidates else None

    def stage_other_event(self, source, card, target=None):
        beneficial = card['id'] == 'EV-019'
        target = target or (self.beneficial_target(source) if beneficial else self.event_target(source))
        if target is None:
            self.emit('EVENT_NO_TARGET', source['player_id'], {'card': card['id']})
            return False
        if not beneficial and any(event.get('target_lock', True) for event in target['staged_events']):
            raise ValueError('OTHER Target Lock violation')
        entry = {'card': card, 'source': source['player_id'], 'target': target['player_id'],
                 'staged_round': self.round, 'activate_round': self.round + 1,
                 'target_lock': not beneficial}
        target['staged_events'].append(entry)
        self.emit('EVENT_STAGE', source['player_id'], {'card': card['id'], 'target': target['player_id'],
                  'activate_round': self.round + 1, 'target_lock': not beneficial})
        return True

    def event_current_effects(self, runner, cards):
        event_ids = {card['id'] for card in active_effect_cards(cards) if card['family'] == 'Event'}
        effort_bonus, direct, ignore_difficulty, cap = 0, 0, False, 8
        direct += sum(2 if event_id == 'EV-023' else 1 for event_id in event_ids & DIRECT_PLUS)
        direct -= int('EV-009' in event_ids) + int('EV-026' in event_ids)
        if 'EV-014' in event_ids:
            ignore_difficulty = True
        for event in self.active_staged(runner):
            event_id = event['card']['id']
            if event_id == 'EV-019':
                direct += 1
            if event_id in ('EV-001', 'EV-002', 'EV-030'):
                direct -= 1
            if event_id in ('EV-011', 'EV-012', 'EV-025'):
                direct -= 1
        return effort_bonus, direct, ignore_difficulty, cap

    def resolve_event_play(self, runner, card, target=None):
        event_id = card['id']
        if target and (target is runner or target['finished'] or target['finish_pending']):
            raise ValueError('Event requires a legal other Runner')
        if event_id == 'EV-018' and target and target['player_id'] not in self.round_pack_snapshot.get(
                runner['player_id'], []):
            raise ValueError('High Five recipient must be an eligible Pack member')
        if event_id in ('EV-015', 'EV-016', 'EV-020') and not (target or self.beneficial_target(runner)):
            raise ValueError('Event requires another Runner')
        runner['stats']['events_played'] += 1
        if event_id in ('EV-011', 'EV-012', 'EV-025'):
            target = target or self.event_target(runner)
            if target and target['energy'] > 0:
                if any(event.get('target_lock', True) for event in target['staged_events']):
                    raise ValueError('OTHER Target Lock violation')
                self.apply_energy(target, -1, f'{card["title"]} Runner choice')
                self.emit('EVENT_TARGET_CHOICE', target['player_id'],
                          {'card': event_id, 'source': runner['player_id'],
                           'choice': 'lose 1 Energy', 'timing': 'IMMEDIATE'})
                return 'discard'
            return 'staged' if self.stage_other_event(runner, card, target) else 'discard'
        if event_id in OTHER_EVENTS:
            return 'staged' if self.stage_other_event(runner, card, target) else 'discard'
        if event_id == 'EV-005':
            rain = sudden_rain(event_id, runner['current_mile'], len(self.course), self.round)
            if rain:
                self.course_events.append(rain)
                self.emit('COURSE_EVENT_APPLY', runner['player_id'], rain)
                return 'course'
        if event_id in ('EV-006', 'EV-010'):
            entry = {'card': card, 'source': runner['player_id'], 'staged_round': self.round,
                     'activate_round': self.round + 1, 'expiry_round': self.round + 1}
            self.global_events.append(entry)
            self.emit('GLOBAL_EVENT_STAGE', runner['player_id'], {'card': event_id,
                      'activate_round': self.round + 1, 'scope': 'CURRENT_PLAYER'})
            return 'global'
        if event_id in AFTER_ENERGY:
            self.apply_energy(runner, AFTER_ENERGY[event_id], card['title'])
            if event_id in ('EV-015', 'EV-016'):
                recipient = target or self.beneficial_target(runner)
                if recipient:
                    self.apply_energy(recipient, 1, 'Crowd Support Runner')
        elif event_id == 'EV-018':
            members = self.round_pack_snapshot.get(runner['player_id'], [])
            recipient = target or next((r for r in self.runners if r['player_id'] in members
                                        and r is not runner and not r['finished']), None)
            beneficiaries = [runner['player_id']] + ([recipient['player_id']] if recipient else [])
            self.apply_energy(runner, 1, 'High Five')
            if recipient:
                self.apply_energy(recipient, 1, 'High Five')
            self.emit('HIGH_FIVE', runner['player_id'], {'pack_snapshot': members,
                      'beneficiaries': beneficiaries, 'timing': 'EFFECT_RESOLUTION'})
        elif event_id == 'EV-020':
            recipient = target or self.beneficial_target(runner)
            if recipient:
                self.apply_energy(recipient, 1, 'Helpful Runner')
                self.emit('EVENT_OTHER_ENERGY', runner['player_id'], {'card': event_id,
                          'recipient': recipient['player_id'], 'amount': 1})
        elif event_id == 'EV-026':
            self.apply_energy(runner, 2, 'Porta-Potty')
        return 'discard'

    def apply_energy(self, runner, amount, source):
        before = runner['energy']
        runner['energy'] = min(15, max(0, runner['energy'] + amount))
        delta = runner['energy'] - before
        if delta >= 0:
            runner['stats']['energy_gained'] += delta
        else:
            runner['stats']['energy_spent'] += -delta
        self.emit('ENERGY_CHANGE', runner['player_id'], {'source': source, 'from': before,
                  'to': runner['energy'], 'delta': delta})

    def after_movement_events(self, runner, played, held_states):
        for card in played:
            event_id = card['id']
            if event_id == 'EV-017':
                cycled = tough_decision_cycle(runner['hand'])
                for old in cycled:
                    runner['hand'].remove(old)
                    self.discard.append(old)
                    self.draw_one(runner, True)
                self.emit('TOUGH_DECISION', runner['player_id'], {'cycled': [card['id'] for card in cycled]})

    def resolve_milestones(self, runner, old_space, new_space):
        for mile in range(old_space // 4 + 1, new_space // 4 + 1):
            self.emit('MILE_CROSS', runner['player_id'], {'mile': mile})
            if mile in MILESTONES[self.cfg['race_format']]['Water']:
                condition = self.condition_by_title(runner, 'Dehydrated')
                if condition:
                    self.named_remedy(runner, condition, 'Water')
                for item in runner['equipped_gear']:
                    if item['card']['title'] == 'Hydration Belt':
                        self.apply_energy(runner, 1, 'Hydration Belt at Water')
                self.emit('MILESTONE', runner['player_id'], {'mile': mile, 'kind': 'Water'})
            if mile in MILESTONES[self.cfg['race_format']]['Aid/Fuel']:
                eligible = [condition for condition in runner['active_conditions']
                            if condition['title'] in ('Twisted Ankle', 'Heat Exhaustion', 'Nausea', 'Gashed Knee')]
                if eligible:
                    self.named_remedy(runner, max(eligible, key=lambda condition: condition['effective_severity']), 'Aid')
                self.emit('MILESTONE', runner['player_id'], {'mile': mile, 'kind': 'Aid/Fuel'})
            if mile in MILESTONES[self.cfg['race_format']]['Gut Check']:
                check = gut_check(runner['hand'], self.installed_titles(runner, 'training'),
                                  self.installed_titles(runner, 'gear'),
                                  GUT_CHECK_THRESHOLDS[self.cfg['race_format']][mile])
                if check['energy_loss']:
                    self.apply_energy(runner, -check['energy_loss'], 'Gut Check failure')
                self.emit('MILESTONE', runner['player_id'], {'mile': mile, 'kind': 'Gut Check',
                                                              'gut_check': check})

    def expire_temporary(self, runner):
        for item in list(runner['active_training']):
            if item['remaining_turns'] is not None:
                item['remaining_turns'] -= 1
                if item['remaining_turns'] <= 0:
                    runner['active_training'].remove(item)
                    self.discard.append(item['card'])
                    self.emit('TRAINING_EXPIRE', runner['player_id'], {'card': item['card']['id']})
        for item in list(runner['equipped_gear']) + list(runner['attached_gear']):
            if item['remaining_turns'] is not None:
                before = item['remaining_turns']
                item['remaining_turns'] -= 1
                self.emit('TEMPORARY_GEAR_TICK', runner['player_id'], {'card': item['card']['id'],
                          'before': before, 'after': item['remaining_turns']})
                if item['remaining_turns'] <= 0:
                    self.remove_gear(runner, item)

    def consume_staged_events(self, runner):
        for event in list(self.active_staged(runner)):
            runner['staged_events'].remove(event)
            self.discard.append(event['card'])
            self.emit('EVENT_EXPIRE', runner['player_id'], {'card': event['card']['id'],
                      'target_lock': False})

    def turn(self, runner, script=None):
        script = script or {}
        if runner['finished'] or runner['finish_pending']:
            return None
        runner['race_turn_number'] += 1
        runner['round'] = self.round
        self.locate(runner)
        self.emit('TURN_START', runner['player_id'], {'turn': runner['race_turn_number'],
                  'hand': [card['id'] for card in runner['hand']], 'energy': runner['energy'],
                  'pack': runner['pack_state']}, {'runner': public_runner(runner)})
        self.replenish(runner)
        capture = {} if self.ai_rationale_enabled and not script else None
        ai_plan = self.choose_turn_plan(runner, capture) if not script else None
        plan = (script['treat_prepare'] if 'treat_prepare' in script else
                None if 'movement_cards' in script else
                ai_plan['treat_prepare'] if ai_plan else self.choose_treat_prepare(runner))
        planned_cards = ai_plan['movement_cards'] if ai_plan else None
        if ai_plan:
            self.emit('AI_TURN_PLAN', runner['player_id'], {'treat_prepare': plan,
                      'movement_cards': planned_cards, 'predicted_movement_quarters':
                      ai_plan['movement_quarters'], 'score': ai_plan['score'],
                      'card_modes': ai_plan['card_modes'],
                      'movement_energy_cost': ai_plan['movement_energy_cost'],
                      'expected_turns_remaining': ai_plan['expected_turns_remaining']})
            if capture is not None:
                from engine.ai_rationale import describe_decision
                decision = describe_decision(self, runner, capture)
                self.ai_decisions.append(decision)
                self.emit('AI_TURN_RATIONALE', runner['player_id'], copy.deepcopy(decision))
        used_plays = self.resolve_treat_prepare(runner, plan)
        if 'pace' in script and script['pace'] != runner['pace']:
            raise ValueError('Pace is locked at Round Start')
        self.apply_installed_energy(runner)
        self.pay_pace(runner)
        available = 2 - used_plays
        if 'movement_cards' in script or planned_cards is not None:
            ids = script['movement_cards'] if 'movement_cards' in script else planned_cards
            if len(ids) > available:
                raise ValueError('card-play budget exceeded')
            played = [next(card for card in runner['hand'] if card['id'] == card_id) for card_id in ids]
            if sum(card['family'] == 'Event' for card in played) > 1:
                raise ValueError('more than one Event played')
            modes = script.get('card_modes', ['MOVEMENT'] * len(played)) if script else ai_plan['card_modes']
        else:
            played = self.choose_movement_cards(runner, available)
            modes = [card['use_mode'] for card in played]
            played = [next(real for real in runner['hand'] if real['id'] == card['id']) for card in played]
        if len(modes) != len(played) or any(mode not in ('MOVEMENT', 'EFFECT') for mode in modes):
            raise ValueError('invalid card use modes')
        if any(mode == 'EFFECT' and card['family'] != 'Event' for card, mode in zip(played, modes)):
            raise ValueError('non-Event Effects use Treat/Prepare')
        card_cost = sum(movement_energy_cost(card) for card, mode in zip(played, modes)
                        if mode == 'MOVEMENT')
        if card_cost > runner['energy']:
            raise ValueError('Movement Energy unavailable')
        for card in played:
            runner['hand'].remove(card)
        for card, mode in zip(played, modes):
            card['use_mode'] = mode
            if mode == 'MOVEMENT':
                cost = movement_energy_cost(card)
                before = runner['energy']
                runner['energy'] -= cost
                runner['stats']['energy_spent'] += cost
                self.emit('MOVEMENT_ENERGY_PAYMENT', runner['player_id'],
                          {'card': card['id'], 'printed_effort': card['effort'],
                           'cost': cost, 'before': before, 'after': runner['energy']})
            runner['stats']['cards_played'] += 1
            runner['stats']['total_effort_used'] += card_effort(card)
            self.emit('PLAY', runner['player_id'], {'card': self.cardview(card), 'mode': mode,
                      'movement_energy_cost': movement_energy_cost(card) if mode == 'MOVEMENT' else 0,
                      'effect_active': mode == 'EFFECT'})
        event_cards = [card for card in active_effect_cards(played) if card['family'] == 'Event']
        event_states = {}
        for card in event_cards:
            target = None
            if script.get('event_target'):
                target = next(item for item in self.runners if item['player_id'] == script['event_target'])
            event_states[card['id']] = self.resolve_event_play(runner, card, target)
        course_end = len(self.course) * 4
        at_finish_extension = runner['quarter_mile_space'] >= course_end
        start_index = min(runner['quarter_mile_space'] // 4, len(self.course) - 1)
        segment = self.course[start_index]
        installed_bonus, installed_sources = self.movement_effort_bonus(runner, segment)
        event_effort_bonus, direct, ignore_difficulty, turn_cap = self.event_current_effects(runner, played)
        condition_penalty = sum(condition_effects(condition, runner['pace'], segment['surface'])['effort_penalty']
                                for condition in runner['active_conditions'])
        training_titles = self.installed_titles(runner, 'training')
        difficulties = [(0 if ignore_difficulty else effective_difficulty(
            course_segment, runner['active_conditions'], training_titles,
            course_event_bonus(self.course_events, course_segment['mile']))) for course_segment in self.course]
        direct += sum(condition_effects(c, runner['pace'], segment['surface'])['direct_movement']
                      for c in runner['active_conditions'])
        effort = sum(card_effort(card) for card in played)
        start_difficulty = 0 if at_finish_extension else difficulties[start_index]
        result_value = (effort + installed_bonus + event_effort_bonus
                        + self.cfg['pace'][runner['pace']]['modifier'] - condition_penalty
                        - start_difficulty)
        old_space = runner['quarter_mile_space']
        resolved = resolve_movement(old_space, result_value, difficulties, len(self.course) * 4,
                                    turn_cap=turn_cap, direct_movement=direct)
        runner['quarter_mile_space'] = resolved['to_space']
        runner['distance_completed'] = runner['quarter_mile_space'] / 4
        runner['stats']['distance_moved'] += resolved['quarter_miles'] / 4
        if resolved['quarter_miles'] == 0:
            runner['stats']['zero_movement_turns'] += 1
        self.emit('MOVE', runner['player_id'], {'formula': 'Effort + installed/Event/Pace - Condition - Effective Difficulty',
                  'effort_cards': [{'id': card['id'], 'printed_effort': card.get('effort'),
                                    'used_effort': card_effort(card), 'mode': card['use_mode']}
                                   for card in played],
                  'movement_energy_cost': card_cost,
                  'total_effort': effort, 'installed_effort_bonus': installed_bonus,
                  'installed_effort_sources': installed_sources, 'event_effort_bonus': event_effort_bonus,
                  'pace': runner['pace'], 'pace_modifier': self.cfg['pace'][runner['pace']]['modifier'],
                  'condition_penalty': condition_penalty,
                  'starting_printed_difficulty': segment['difficulty'],
                  'starting_effective_difficulty': start_difficulty,
                  'movement_result': result_value, **resolved})
        if ai_plan and capture is not None:
            from engine.ai_rationale import describe_outcome
            outcome = describe_outcome(self.ai_decisions[-1], resolved['quarter_miles'])
            self.ai_decisions[-1]['outcome'] = outcome
            self.emit('AI_TURN_OUTCOME', runner['player_id'], outcome)
        for boundary in resolved['boundaries']:
            self.emit('MOVE_BOUNDARY', runner['player_id'], boundary)
        self.resolve_milestones(runner, old_space, runner['quarter_mile_space'])
        self.after_movement_events(runner, event_cards, event_states)
        for card in played:
            state = event_states.get(card['id'])
            card.pop('use_mode', None)
            if state in ('staged', 'course', 'global', 'transferred'):
                continue
            self.discard.append(card)
            runner['stats']['cards_discarded'] += 1
            self.emit('DISCARD', runner['player_id'], {'card': card['id'], 'reason': 'played'})
        if runner['quarter_mile_space'] >= course_end and resolved['positive_finish_movement']:
            runner['finish_pending'] = True
            runner['finish_round'] = self.round
            runner['finish_turn'] = runner['race_turn_number']
            self.pending_finishers.append(runner)
            self.emit('FINISH_PENDING', runner['player_id'], {'course_endpoint': course_end / 4,
                      'finish_extension': 0.2 if self.cfg['race_format'] == 'marathon' else 0.1,
                      'positive_movement_remaining': True,
                      'hand_effort': sum(card.get('effort') or 0 for card in runner['hand']),
                      'energy': runner['energy'], 'will_available': runner['will_available']})
        elif runner['quarter_mile_space'] >= course_end:
            self.emit('COURSE_ENDPOINT', runner['player_id'], {'finished': False,
                      'reason': 'no positive legal movement remaining for Finish extension'})
        self.expire_temporary(runner)
        self.consume_staged_events(runner)
        self.locate(runner)
        self.turn_records.append({'round': self.round, 'player_id': runner['player_id'],
                                  'movement_quarters': resolved['quarter_miles'],
                                  'movement_result': result_value, 'cards_played': len(played) + used_plays,
                                  'pace': runner['pace'], 'boundaries': resolved['boundaries'],
                                  'cap_prevented': resolved['cap_prevented'],
                                  'cap_prevented_quarters': resolved['cap_prevented_quarters'],
                                  'result_wasted_above_cap': resolved['result_wasted_above_cap'],
                                  'hand_size_at_decision': len(runner['hand']) + len(played),
                                  'effort_count': len(played), 'energy_effect_count': 0})
        self.emit('TURN_END', runner['player_id'], {'position': runner['quarter_mile_space'],
                  'energy': runner['energy'], 'hand': [card['id'] for card in runner['hand']],
                  'finish_pending': runner['finish_pending']})
        return resolved

    def resolve_same_round_finishers(self):
        finishers = [runner for runner in self.pending_finishers if runner['finish_round'] == self.round]
        if not finishers:
            return
        groups = collections.defaultdict(list)
        for runner in finishers:
            key = (sum(card.get('effort') or 0 for card in runner['hand']), runner['energy'],
                   1 if runner['will_available'] else 0)
            groups[key].append(runner)
        place = len(self.finish) + 1
        for key in sorted(groups, reverse=True):
            group = groups[key]
            for runner in group:
                runner['finished'] = True
                runner['finish_pending'] = False
                runner['finish_order'] = place
                self.finish.append(runner['player_id'])
                self.emit('FINISH', runner['player_id'], {'place': place, 'shared': len(group) > 1,
                          'tiebreak': {'hand_effort': key[0], 'energy': key[1], 'will': key[2]}})
            place += len(group)
        self.pending_finishers = [runner for runner in self.pending_finishers if runner not in finishers]

    def end_round(self):
        self.resolve_same_round_finishers()
        expired_course = [event for event in self.course_events if event['remaining_duration'] == 1]
        self.course_events = tick_course_events(self.course_events)
        for event in expired_course:
            self.discard.append(copy.deepcopy(self.card(event['source_card'])))
            self.emit('COURSE_EVENT_EXPIRE', payload=event)
        for event in list(self.global_events):
            if event['expiry_round'] <= self.round:
                self.global_events.remove(event)
                self.discard.append(event['card'])
                self.emit('GLOBAL_EVENT_EXPIRE', payload={'card': event['card']['id']})
        for pack_id in sorted({runner['pack_state'] for runner in self.runners if runner['pack_state']}):
            members = [runner for runner in self.runners if runner['pack_state'] == pack_id and not runner['finished']]
            if members:
                lead_position = max(runner['quarter_mile_space'] for runner in members)
                members = [runner for runner in members if lead_position - runner['quarter_mile_space'] <= 2]
            if len(members) < 2:
                members = []
            member_ids = [runner['player_id'] for runner in members]
            for runner in self.runners:
                if runner['pack_state'] == pack_id:
                    runner['pack_state'] = pack_id if runner in members else None
                    runner['pack_members_snapshot'] = member_ids if runner in members else []
            self.emit('PACK_COHESION', payload={'pack': pack_id, 'members': member_ids,
                                                'dissolved': len(members) < 2})
        self.emit('ROUND_END', payload={'positions': {runner['player_id']: runner['quarter_mile_space']
                                                     for runner in self.runners},
                                        'finishers': [runner['player_id'] for runner in self.runners
                                                      if runner.get('finish_round') == self.round]})

    def run_round(self, scripts=None, scripted_paces=None):
        self.start_round(scripted_paces)
        scripts = scripts or {}
        for runner in self.runners:
            if not runner['finished']:
                self.turn(runner, scripts.get(runner['player_id']))
        self.end_round()

    def run(self):
        self.setup()
        while len(self.finish) < len(self.runners):
            if any(runner['race_turn_number'] >= self.cfg['max_turns_per_runner']
                   for runner in self.runners if not runner['finished']):
                raise RuntimeError('turn cap')
            self.run_round()
        self.emit('SIMULATION_END', payload={'finish_order': self.finish, 'rounds': self.round})
        return self.events


def render_trace(sim):
    lines = [f"# DRG Simulation Trace\n\nSeed: `{sim.cfg['seed']}`  \nFormat: `{sim.cfg['race_format']}`  \nRunners: `{len(sim.runners)}`\n",
             '## Course generation']
    for segment in sim.course:
        lines.append(f"- Mile {segment['mile']}: {segment['course_card_id']} side {segment['side']} — "
                     f"{segment['setting']}; {segment['surface']} {segment['route']}; "
                     f"{segment['elevation']}; Difficulty {segment['difficulty']}; "
                     f"milestones {', '.join(segment.get('milestones', [])) or 'none'}")
    lines.append('\n## Chronological events')
    for event in sim.events:
        player = f" [{event['player_id']}]" if event['player_id'] else ''
        lines.append(f"\n### {event['event_id']} — {event['type']}{player}\n\n```json\n"
                     f"{json.dumps(event['payload'], indent=2)}\n```")
    return '\n'.join(lines) + '\n'


def diagnostics(sim):
    records = sim.turn_records
    moves = [record['movement_quarters'] / 4 for record in records]
    distribution = collections.Counter(moves)
    boundaries = [boundary for record in records for boundary in record['boundaries']]
    finish_turns = [runner['finish_turn'] for runner in sim.runners if runner['finish_turn'] is not None]
    from engine.ai_rationale import rationale_metrics
    return {'rounds': sim.round, 'turns': len(records),
            'ai_rationale': rationale_metrics(sim.ai_decisions),
            'average_movement': statistics.mean(moves) if moves else 0,
            'median_movement': statistics.median(moves) if moves else 0,
            'maximum_movement': max(moves, default=0),
            'movement_distribution': {f'{quarter / 4:.2f}': distribution.get(quarter / 4, 0)
                                      for quarter in range(9)},
            'boundary_crossings': len(boundaries),
            'turns_prevented_by_two_mile_cap': sum(record['cap_prevented'] for record in records),
            'movement_prevented_by_two_mile_cap_miles': sum(record['cap_prevented_quarters']
                                                             for record in records) / 4,
            'movement_result_wasted_above_two_mile_cap': sum(record['result_wasted_above_cap']
                                                              for record in records),
            'first_finisher_turn': min(finish_turns) if finish_turns else None,
            'final_finisher_turn': max(finish_turns) if finish_turns else None,
            'finishing_spread_turns': (max(finish_turns) - min(finish_turns)) if finish_turns else None}


def summary(sim):
    lines = [f"# Simulation Summary\n\nSeed: `{sim.cfg['seed']}`\n\nStatus: completed in {sim.round} rounds.\n",
             '## Finish order']
    for runner in sorted(sim.runners, key=lambda item: (item['finish_order'], item['player_id'])):
        lines.append(f"{runner['finish_order']}. {runner['player_id']} {runner['profile']} — "
                     f"turn {runner['finish_turn']}, Energy {runner['energy']}")
    from engine.ai_rationale import rationale_metrics
    lines.append('\n## AI decision diagnostics')
    for key, value in rationale_metrics(sim.ai_decisions).items():
        lines.append(f'- {key}: {value}')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='simulation/config.json')
    parser.add_argument('--output', default='output')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cfg = load_json(root / args.config)
    sim = Sim(root, cfg)
    sim.run()
    output = root / args.output
    output.mkdir(exist_ok=True)
    diag = diagnostics(sim)
    metadata = {'seed': cfg['seed'], 'config_hash': digest(cfg),
                'data_hash': digest({'cards': sim.cards, 'course': sim.course_cards}),
                'event_hash': digest(sim.events), 'diagnostics_hash': digest(diag),
                'event_count': len(sim.events)}
    with open(output / 'Simulation-Event-Log.jsonl', 'w') as stream:
        stream.write(json.dumps({'metadata': metadata}) + '\n')
        for event in sim.events:
            stream.write(json.dumps(event, sort_keys=True) + '\n')
    (output / 'Simulation-Trace.md').write_text(render_trace(sim))
    (output / 'Simulation-Summary.md').write_text(summary(sim))
    (output / 'Simulation-Diagnostics.json').write_text(json.dumps(diag, indent=2) + '\n')
    (output / 'Simulation-Metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
