# Simulation State

Global state includes seed/RNG, format, course mapping, draw/discard piles, round, active player, events, finish order, and configuration. Runner state includes every field requested by the foundation specification plus cumulative statistics. Events contain pre/post state snapshots sufficient to audit state changes; `config_hash` and `data_hash` bind outputs to inputs.
