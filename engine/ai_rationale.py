"""Read-only explanations of the existing Victory AI's scored legal plans.

This module never generates, filters, ranks, or executes actions. Its estimates are
those already produced by the AI preview; the live MOVE event remains authoritative.
"""
import collections
from engine.simulate import (GEAR_DURATION, TRAINING_DURATION, MILESTONES, course_event_bonus,
                             effective_difficulty)

REASON_CODES = frozenset({
    'WIN_SPEED', 'FINISH_SPRINT', 'POSITION_RECOVERY', 'ENERGY_SUSTAINABILITY',
    'CONDITION_EMERGENCY', 'SETUP_PAYOFF', 'PACK_ADVANTAGE', 'LEGALITY_FORCED',
    'NO_POSITIVE_MOVEMENT_AVAILABLE',
})


def plan_class(sim, row):
    plan = row['treat_prepare']
    cards = row['movement_cards']
    if plan:
        action = plan['action']
        if action == 'training':
            return 'Training install/replace + Move'
        if action == 'gear':
            return 'Gear equip/replace + Move'
        if action == 'attach':
            return 'attached Gear remedy + Move'
        if action == 'fuel':
            return 'Fuel remedy + Move' if plan.get('choice') in ('remedy', 'severity') else 'Fuel recovery + Move'
        return 'Treat/Prepare + Move'
    if any(sim.card(cid)['family'] == 'Event' for cid in cards):
        return 'Event-related legal plan'
    return 'Move + Move' if len(cards) == 2 else 'Move' if cards else 'No card play'


def _rank(row):
    return (row['score'], row['movement_quarters'], tuple(row['movement_cards']),
            str(row['treat_prepare']))


def _position(sim, runner):
    space = runner['quarter_mile_space']
    others = [r['quarter_mile_space'] for r in sim.runners
              if r['player_id'] != runner['player_id'] and not r['finished']]
    ahead = [p - space for p in others if p > space]
    behind = [space - p for p in others if p < space]
    return {'place': 1 + sum(p > space for p in others),
            'gap_to_leader_miles': max(0, max(others, default=space) - space) / 4,
            'gap_to_runner_ahead_miles': min(ahead, default=None) / 4 if ahead else None,
            'gap_to_runner_behind_miles': min(behind, default=None) / 4 if behind else None}


def _detail(sim, runner, row, baseline, before_quarters):
    plan = row['treat_prepare']
    prepared = sim.preview_preparation(runner, plan)
    paid = sim.preview_payment(prepared)
    cards = [{**next(c for c in prepared['hand'] if c['id'] == cid), 'use_mode': mode}
             for cid, mode in zip(row['movement_cards'], row.get('card_modes', ['MOVEMENT'] * len(row['movement_cards'])))]
    after_cards = sim.preview_payment(prepared, row.get('movement_energy_cost', 0))
    result = sim.preview_movement(after_cards, cards)
    remaining_after = max(0, len(sim.course) * 4 - result['to_space'])
    rate = max(2, row['movement_quarters'] or 2)
    roles = ([{'id': plan['card_id'], 'title': sim.card(plan['card_id'])['title'],
               'printed_effort': sim.card(plan['card_id']).get('effort'),
               'role': plan['action'], 'replaces': plan.get('replace_id')}] if plan else [])
    roles += [{'id': c['id'], 'title': c['title'], 'printed_effort': c.get('effort'),
               'role': c['use_mode'], 'movement_energy_cost':
               c['movement_energy_cost'] if c['use_mode'] == 'MOVEMENT' else 0} for c in cards]
    old_conditions = {c['id']: c['effective_severity'] for c in runner['active_conditions']}
    new_conditions = {c['id']: c['effective_severity'] for c in prepared['active_conditions']}
    condition_impact = {cid: {'before': sev, 'after': new_conditions.get(cid, 0)}
                        for cid, sev in old_conditions.items() if new_conditions.get(cid, 0) != sev}
    setup = bool(plan and plan['action'] in ('training', 'gear', 'attach'))
    horizon = min(remaining_after, 24) / 24 if setup else None
    if setup:
        title = sim.card(plan['card_id'])['title']
        duration = (TRAINING_DURATION if plan['action'] == 'training' else GEAR_DURATION).get(title)
        if duration:
            horizon *= min(1, duration / 6)
    pace_cost = sim.pace_cost(prepared, prepared['pace'])
    setup_estimate = None
    if setup:
        visible = sim.course[min(runner['quarter_mile_space'] // 4, len(sim.course) - 1):][:6]
        effort_delta = (sum(sim.movement_effort_bonus(prepared, side)[0]
                            - sim.movement_effort_bonus(runner, side)[0]
                            for side in visible) / len(visible)) if visible else 0
        old_titles = sim.installed_titles(runner, 'training')
        new_titles = sim.installed_titles(prepared, 'training')
        difficulty_delta = (sum(effective_difficulty(side, runner['active_conditions'], old_titles)
                                - effective_difficulty(side, prepared['active_conditions'], new_titles)
                                for side in visible) / len(visible)) if visible else 0
        setup_estimate = {
            'visible_segments_sampled': len(visible),
            'mean_effort_gain': effort_delta,
            'mean_difficulty_reduction': difficulty_delta,
            'pace_energy_cost_reduction': sim.pace_cost(runner, runner['pace'])['final']
                                          - sim.pace_cost(prepared, prepared['pace'])['final'],
            'installed_energy_this_turn': sum(amount for _, amount in sim.installed_energy(prepared))
                                          - sum(amount for _, amount in sim.installed_energy(runner)),
            'future_visible_energy_gain_at_current_pace':
            (sum(sum(amount for _, amount in sim.energy_gains_on_side(prepared, side))
                 - sum(amount for _, amount in sim.energy_gains_on_side(runner, side))
                 for side in visible[1:]) / len(visible[1:])) if len(visible) > 1 else 0,
            'future_visible_water_opportunity_delta':
            sum(('Hydration Belt' in sim.installed_titles(prepared, 'gear'))
                - ('Hydration Belt' in sim.installed_titles(runner, 'gear'))
                for side in visible[1:]
                if side['mile'] in MILESTONES[sim.cfg['race_format']]['Water']),
            'discount_factor': horizon,
            'note': 'Current Pace is a proxy for future visible Course starts; no future draw or Pace choice is assumed. Other resistance, Gut Check, and staged-weather terms are not fully decomposed.'}
    gap = _position(sim, runner)['gap_to_leader_miles']
    return {'plan_type': plan_class(sim, row), 'treat_prepare': plan,
            'movement_cards': row['movement_cards'], 'card_modes': row.get('card_modes'),
            'cards_used': roles,
            'selected_pace': paid['pace'], 'projected_effort': sum(c['effort'] for c in cards
                                                                 if c['use_mode'] == 'MOVEMENT'),
            'projected_movement_quarters': row['movement_quarters'],
            'projected_movement_miles': row['movement_quarters'] / 4,
            'projected_energy_cost': pace_cost['final'] + row.get('movement_energy_cost', 0),
            'projected_movement_energy_cost': row.get('movement_energy_cost', 0),
            'projected_energy_after_pace': paid['energy'],
            'projected_energy_after_action': None if any(c['family'] == 'Event' and c['use_mode'] == 'EFFECT'
                                                         for c in cards) else
            min(15, max(0, after_cards['energy'] - result['staged_energy_cost'])
                + result['milestone_energy_gain']),
            'energy_after_note': 'Event and checkpoint effects resolve in the live turn; preview score estimates them.',
            'projected_condition_impact': condition_impact,
            'projected_setup_benefit': setup_estimate,
            'immediate_movement_opportunity_cost_quarters':
            max(0, baseline['movement_quarters'] - row['movement_quarters']) if setup else 0,
            'future_benefit_estimate': setup_estimate,
            'remaining_distance_discount': horizon,
            'estimated_turns_to_recover_setup': remaining_after / rate if setup else None,
            'expected_turns_remaining_before_plan': before_quarters / rate,
            'expected_turns_remaining_after_plan': row['expected_turns_remaining'],
            'turns_estimate_note': 'Before uses the same projected rate and minimum 2-quarter denominator as the scorer; neither estimate predicts draws.',
            'relative_race_position_effect': {'gap_to_leader_miles': gap,
                                              'progress_weight': 12 + min(2, gap / 4)},
            'profile_specific_modifier': 'Included in total score; not separately exposed by scorer.',
            'total_plan_score': row['score'], 'score_components': None}


def describe_decision(sim, runner, capture):
    rows = capture['candidates']
    selected = capture['selected']
    positive = [row for row in rows if row['movement_quarters'] > 0]
    best_positive = max(positive, key=_rank) if positive else None
    moves = [r for r in rows if r['treat_prepare'] is None and len(r['movement_cards']) == 2]
    baseline = max(moves, key=_rank) if moves else best_positive or selected
    classes = collections.Counter(plan_class(sim, row) for row in rows)
    best_by_class = {kind: max((r for r in rows if plan_class(sim, r) == kind), key=_rank)
                     for kind in classes}
    alternatives = [r for r in rows if r is not selected]
    important = sorted(alternatives, key=_rank, reverse=True)[:3]
    important += [r for r in alternatives if r['movement_quarters'] > selected['movement_quarters']]
    zeros = [r for r in alternatives if r['movement_quarters'] == 0]
    if zeros:
        important.append(max(zeros, key=_rank))
    important += [r for r in best_by_class.values() if r is not selected]
    unique = []
    seen = set()
    for row in important:
        key = (str(row['treat_prepare']), tuple(row['movement_cards']), tuple(row.get('card_modes', [])))
        if key not in seen:
            unique.append(row)
            seen.add(key)
    before = max(0, len(sim.course) * 4 - runner['quarter_mile_space'])
    selected_detail = _detail(sim, runner, selected, baseline, before)
    rejected = [_detail(sim, runner, row, baseline, before) for row in unique]
    for detail in rejected:
        detail['rejection_explanation'] = (
            f"Projects {detail['projected_movement_miles']:.2f} miles and "
            f"{detail['expected_turns_remaining_after_plan']:.2f} estimated turns remaining; "
            f"selected projects {selected_detail['projected_movement_miles']:.2f} miles "
            f"and {selected_detail['expected_turns_remaining_after_plan']:.2f} turns. "
            f"Existing total scores are {detail['total_plan_score']:.3f} versus "
            f"{selected_detail['total_plan_score']:.3f}; components are not separately exposed.")
    position = _position(sim, runner)
    course_index = min(runner['quarter_mile_space'] // 4, len(sim.course) - 1)
    segment = sim.course[course_index]
    pace_event = next((e['payload'] for e in reversed(sim.events)
                       if e['type'] == 'PACE_SELECT' and e['player_id'] == runner['player_id']
                       and e['round'] == sim.round), None)
    options = pace_event['options'] if pace_event else []
    selected_pace = runner['pace']
    other_paces = [o for o in options if o['pace'] != selected_pace]
    pace_cost = sim.pace_cost(runner, selected_pace)
    option_comparison = '; '.join(
        f"{o['pace']} {o['movement_quarters'] / 4:.2f} miles, "
        f"{o['expected_turns_remaining']:.2f} estimated turns, score {o['score']:.3f}"
        for o in options)
    pace_reason = (f"{selected_pace} costs {pace_cost['final']} Energy after "
                   f"{', '.join(pace_cost['preservation_sources']) or 'no preservation'}; "
                   + (f"Round Start visible-hand Pace comparisons: {option_comparison}. "
                      "Pace was locked before Replenish and Pack formation."
                      if options else 'Pace was set before this turn; no Round Start comparison is available.'))
    emergency = capture['emergency']
    if selected['movement_quarters'] == 0:
        reason = ('NO_POSITIVE_MOVEMENT_AVAILABLE' if not best_positive else
                  'CONDITION_EMERGENCY' if any(c['effective_severity'] >= 4
                                               for c in runner['active_conditions']) else
                  'ENERGY_SUSTAINABILITY' if emergency else 'LEGALITY_FORCED')
    elif before <= 12 and selected['movement_quarters'] >= before:
        reason = 'FINISH_SPRINT'
    elif selected['treat_prepare'] and selected['treat_prepare']['action'] in ('training', 'gear', 'attach'):
        reason = 'SETUP_PAYOFF'
    elif selected['treat_prepare'] and selected['treat_prepare']['action'] == 'fuel':
        reason = 'CONDITION_EMERGENCY' if selected_detail['projected_condition_impact'] else 'ENERGY_SUSTAINABILITY'
    else:
        reason = 'WIN_SPEED'
    secondary = []
    if position['gap_to_leader_miles'] > 0:
        secondary.append('POSITION_RECOVERY')
    if runner['pack_state']:
        secondary.append('PACK_ADVANTAGE')
    if before <= 12 and reason != 'FINISH_SPRINT':
        secondary.append('FINISH_SPRINT')
    comparison = (f" Against the best Move + Move plan ({baseline['movement_quarters'] / 4:.2f} miles), "
                  f"setup sacrifices {selected_detail['immediate_movement_opportunity_cost_quarters'] / 4:.2f} miles; "
                  f"its remaining-distance discount is {selected_detail['remaining_distance_discount']:.2f}; "
                  f"visible mean Effort gain is {selected_detail['projected_setup_benefit']['mean_effort_gain']:.2f}, "
                  f"Difficulty reduction {selected_detail['projected_setup_benefit']['mean_difficulty_reduction']:.2f}, "
                  f"and Pace Energy cost reduction "
                  f"{selected_detail['projected_setup_benefit']['pace_energy_cost_reduction']}."
                  if selected_detail['remaining_distance_discount'] is not None else '')
    reason_text = (f"Selected {selected_detail['plan_type']} with "
                   f"{', '.join(selected['movement_cards']) or 'no Movement card'}: "
                   f"projects {selected['movement_quarters'] / 4:.2f} miles, "
                   f"estimated turns-to-finish {selected_detail['expected_turns_remaining_before_plan']:.2f} "
                   f"to {selected['expected_turns_remaining']:.2f}, "
                   f"and a {position['gap_to_leader_miles']:.2f}-mile gap to the leader. "
                   f"Projected Pace plus Movement-card cost is {selected_detail['projected_energy_cost']} Energy "
                   f"({selected_detail['projected_movement_energy_cost']} from cards); "
                   f"total score {selected['score']:.3f}." + comparison)
    if rejected:
        reason_text += (' Closest rejected alternative projects '
                        f"{rejected[0]['projected_movement_miles']:.2f} miles "
                        f"at score {rejected[0]['total_plan_score']:.3f}.")
    finish_phase = {'remaining_miles': before / 4, 'energy': runner['energy'],
                    'within_final_three_miles': before <= 12,
                    'finish_sprint': before <= 12 and selected['movement_quarters'] > 0,
                    'setup_discount': selected_detail['remaining_distance_discount'],
                    'non_movement_setup_justification': reason_text if before <= 12 and
                    selected['treat_prepare'] else None}
    return {'schema_version': 1, 'round': sim.round, 'turn': runner['race_turn_number'],
            'runner_id': runner['player_id'], 'profile': runner['profile'],
            'race_position': position, 'distance_completed_miles': runner['quarter_mile_space'] / 4,
            'distance_remaining_miles': before / 4, 'energy': runner['energy'],
            'current_pace': selected_pace,
            'active_conditions': [{'id': c['id'], 'title': c['title'],
                                   'effective_severity': c['effective_severity']}
                                  for c in runner['active_conditions']],
            'installed_training': [i['card']['id'] for i in runner['active_training']],
            'equipped_gear': [i['card']['id'] for i in runner['equipped_gear']],
            'course_segment': {'mile': segment['mile'], 'id': segment.get('id'),
                               'printed_difficulty': segment['difficulty'],
                               'effective_difficulty': effective_difficulty(
                                   segment, runner['active_conditions'],
                                   sim.installed_titles(runner, 'training'),
                                   course_event_bonus(sim.course_events, segment['mile']))},
            'legal_plan_set': {'count': len(rows), 'eligible_after_victory_zero_filter': len(capture['eligible']),
                               'class_counts': dict(classes),
                               'best_by_class': {k: {'treat_prepare': v['treat_prepare'],
                                                     'movement_cards': v['movement_cards'],
                                                     'card_modes': v.get('card_modes'),
                                                     'movement_energy_cost': v.get('movement_energy_cost'),
                                                     'movement_quarters': v['movement_quarters'],
                                                     'score': v['score']} for k, v in best_by_class.items()},
                               'summary_note': 'Counts cover every enumerated legal complete plan; representative plans omit redundant permutations.'},
            'selected_plan': selected_detail, 'rejected_alternatives': rejected,
            'best_positive_alternative': _detail(sim, runner, best_positive, baseline, before)
            if best_positive else None,
            'best_move_move_alternative': _detail(sim, runner, baseline, baseline, before)
            if moves else None,
            'reason_code': reason, 'secondary_reasons': secondary, 'reason': reason_text,
            'emergency_override_eligible': emergency,
            'emergency_override_reason': ('Energy at most 1' if runner['energy'] <= 1 else
                                          'Condition Effective Severity at least 4') if emergency else None,
            'pace_rationale': {'legal_options_at_round_start': options,
                               'selected': selected_pace, 'maximum_legal': sim.maximum_legal_pace(runner),
                               'projected_selected_cost': pace_cost,
                               'pack': runner['pack_state'], 'comparison': pace_reason,
                               'faster_slower_rejected': [o for o in other_paces]},
            'finish_phase': finish_phase}


def describe_outcome(decision, actual_quarters):
    positive = decision['best_positive_alternative']
    selected = decision['selected_plan']
    zero = actual_quarters == 0
    emergency = decision['emergency_override_eligible'] and zero and positive is not None
    forced = zero and positive is None
    return {'actual_movement_quarters': actual_quarters,
            'actual_movement_miles': actual_quarters / 4,
            'selected_projected_zero': selected['projected_movement_quarters'] == 0,
            'legal_positive_alternative_existed': positive is not None,
            'best_legal_positive_alternative': positive if zero else None,
            'positive_alternative_rejection_reason':
            (decision['reason'] if zero and positive else None),
            'emergency_override_applied': bool(emergency),
            'exact_override_reason': decision['emergency_override_reason'] if emergency else None,
            'forced_by_legality_or_state': forced,
            'forced_reason': 'No enumerated legal plan projected forward Movement.' if forced else None}


def rationale_metrics(decisions):
    outcomes = [d['outcome'] for d in decisions if 'outcome' in d]
    zeros = [o for o in outcomes if o['actual_movement_quarters'] == 0]
    setup = [d for d in decisions if d['selected_plan']['treat_prepare'] and
             d['selected_plan']['treat_prepare']['action'] in ('training', 'gear', 'attach')]
    def selected(action):
        return [d for d in setup if d['selected_plan']['treat_prepare']['action'] == action]
    rejected_setup = [d for d in decisions if any(a['treat_prepare'] and
                      a['treat_prepare']['action'] in ('training', 'gear', 'attach') and
                      a['immediate_movement_opportunity_cost_quarters'] > 0
                      for a in d['rejected_alternatives'])]
    return {'total_zero_movement_turns': len(zeros),
            'zero_movement_with_positive_alternative': sum(o['legal_positive_alternative_existed'] for o in zeros),
            'zero_movement_with_no_positive_alternative': sum(not o['legal_positive_alternative_existed'] for o in zeros),
            'zero_movement_emergency_override': sum(o['emergency_override_applied'] for o in zeros),
            'zero_movement_forced_legality_state': sum(o['forced_by_legality_or_state'] for o in zeros),
            'training_installs': sum(not d['selected_plan']['treat_prepare'].get('replace_id') for d in selected('training')),
            'training_replacements': sum(bool(d['selected_plan']['treat_prepare'].get('replace_id')) for d in selected('training')),
            'gear_equips': sum(not d['selected_plan']['treat_prepare'].get('replace_id') for d in selected('gear')),
            'gear_replacements': sum(bool(d['selected_plan']['treat_prepare'].get('replace_id')) for d in selected('gear')),
            'attached_gear_actions': len(selected('attach')),
            'setup_actions_reducing_movement': sum(d['selected_plan']['immediate_movement_opportunity_cost_quarters'] > 0 for d in setup),
            'setup_actions_producing_zero_movement': sum(d['outcome']['actual_movement_quarters'] == 0 for d in setup if 'outcome' in d),
            'turns_with_setup_rejected_for_opportunity_cost': len(rejected_setup)}
