# Simulation State

Global state includes seed/RNG, format, course mapping, draw/discard piles, round, active player, events, finish order, and configuration. Runner state includes every field requested by the foundation specification plus cumulative statistics. Events contain pre/post state snapshots sufficient to audit state changes; `config_hash` and `data_hash` bind outputs to inputs.

Current Will state is a single-use `will_available` flag. The turn preview checks total payable Pace plus all chosen Movement-card costs after reductions. Live `WILL_USE` records the exact shortfall, while `PACE_PAYMENT` and each `MOVEMENT_ENERGY_PAYMENT` separate stored Energy paid from Will coverage. A forced empty fallback retains the complete AI plan schema. Pack membership is fixed within a round and recalculated after Pace selection at the next Round Start.
