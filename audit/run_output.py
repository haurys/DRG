"""Deterministic JSON conversion for observation-only audit state exports."""

import json


def json_safe(value):
    """Return a JSON-compatible copy without changing the simulation state."""
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((json_safe(item) for item in value),
                      key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    return value


def final_state_json(sim):
    """Serialize a finished or interrupted runner/course/deck audit snapshot."""
    return json.dumps(json_safe({'seed': sim.cfg['seed'], 'runners': sim.runners,
                                 'course': sim.course, 'deck_audit': sim.deck_audit}),
                      indent=2, ensure_ascii=False) + '\n'
