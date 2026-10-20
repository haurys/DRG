# Simulation State

Global state includes seed/RNG, format, course mapping, draw/discard piles, round, active player, events, finish order, and configuration. Runner state includes every field requested by the foundation specification plus cumulative statistics. Events contain pre/post state snapshots sufficient to audit state changes; `config_hash` and `data_hash` bind outputs to inputs.

Current Will state is a single-use `will_available` flag. The turn preview checks total payable Pace plus all chosen Movement-card costs after reductions. Live `WILL_USE` records the exact shortfall, while `PACE_PAYMENT` and each `MOVEMENT_ENERGY_PAYMENT` separate stored Energy paid from Will coverage. A forced empty fallback retains the complete AI plan schema. Pack membership is fixed within a round and recalculated after Pace selection at the next Round Start.

## v1.3 race result state

`race_status` is `ACTIVE`, `FINISHED`, or `DNF`. DNF also records `dnf`, `dnf_reason`, `dnf_round`, and `dnf_turn`; distance, Energy, Will, Conditions, and hand remain available for audit. DNF runners have no finish order and receive no more turns. The race ends when every runner is FINISHED or DNF.

## v1.4 candidate zones

Each normal Training/Gear slot records its installation runner-turn. On the second subsequent runner turn it can be sacrificed directly for Movement, then discards; new/replaced installations reset age. A Condition attachment is separate from normal slots and remains unavailable until its Condition is completely removed, when it discards. The hand is capped at six with no minimum or automatic refill. DNF continuation includes eligible slot Movement.

Course state uses one record per one-mile lane. The physical marathon selects 13 **two-mile cards** and maps each selected card to an outbound and opposite return record, yielding 26 one-mile records and 104 quarter-mile spaces. The Start/Finish end corresponds to mile 1 outbound and mile 26 returning. The runner's `current_course_card`, `current_course_side`, `current_mile`, and `quarter_mile_space` preserve both physical card and side context. Gear `is_footwear` enforces the one-shoe rule; its broad `category` is descriptive. Treat/Prepare action usage and new card plays are separate counters.
