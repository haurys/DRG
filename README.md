# DRG Simulation Foundation

Deterministic, audit-first baseline for Downtown Running Game. Markdown is the human-readable specification; JSON companions are validated engine inputs.

## Run

```bash
python3 engine/simulate.py --config simulation/config.json --output output
python3 -m unittest discover -s tests -v
```

The supplied simulation configuration is historical. Do not run a formal marathon as part of the frozen redesign validation.

## Movement implementation status

**Frozen card redesign under validation.** The live race path now executes Replenish, Treat/Prepare, Pace payment and Will, Pack preservation, installed Training/Gear, Fuel/remedies, Condition treatment/suppression, mandatory Event timing, Gut Checks, Effective Difficulty boundaries, Finish extension, and same-round placement. Validation uses bounded turn/round fixtures; it does not run the 8-runner marathon.

## Frozen 108-card redesign

Current source: `DRG-Canonical-Playtest-Rules.md`, `DRG-Race-Card-Simulation-Effect-Definitions.md`, and `data/race_cards.json`. Non-Condition cards use either MOVEMENT (Effort plus 0/1/2 Energy by Effort band) or EFFECT (no printed Effort or card Movement cost). Conditions have Severity. The Pace costs and starting Energy remain unchanged.
