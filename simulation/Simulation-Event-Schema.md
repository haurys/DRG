# Simulation Event Schema

JSON Lines, chronological. Required keys: `event_id`, `sequence`, `type`, `round`, `player_id`, `payload`, and `state`. IDs are `EV-000001` etc. Course/setup events use null player IDs. State contains public global state and the acting runner snapshot; setup deal events include that runner’s private hand because the output is a designer audit artifact. `MOVE` contains the complete continuous calculation and all boundary steps; each transition also emits `MOVE_BOUNDARY`. Event types include every category requested, plus `DECISION`, `ROUND_START`, `MOVE_BOUNDARY`, and `SIMULATION_END`.

## Frozen card economy audit fields

`PLAY` records `mode`, printed card Effort, Movement Energy cost paid, and whether its Effect activated. `MOVEMENT_ENERGY_PAYMENT` records the per-card cost and before/after Energy. `PACE_PAYMENT` records the independent Pace cost, preservation sources and Will. `MOVE` records printed/used Effort per played card, Effective Difficulty, direct Movement, and boundary deltas. `FUEL_USE`, `ENERGY_CHANGE`, `CONDITION_TREAT`, `CONDITION_REMEDY`, `CONDITION_SUPPRESSION`, `TRAINING_INSTALL`, `GEAR_EQUIP`, `GEAR_REMOVE`, `GLOBAL_EVENT_ACTIVATE/EXPIRE`, `GLOBAL_WEATHER` with source runner and protection, and `COURSE_EVENT_APPLY/EXPIRE` record effect-specific transitions. A Gut Check `MILESTONE` includes hand Effort and total modifiers.
