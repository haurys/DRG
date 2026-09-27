# DRG Simulation Foundation

Deterministic, audit-first baseline for Downtown Running Game. Markdown is the human-readable specification; JSON companions are validated engine inputs.

## Run

```bash
python3 engine/simulate.py --config simulation/config.json --output output
python3 -m unittest discover -s tests -v
```

Default target: 8-runner full marathon, seed `20260924`. Do not execute it until the single-audit gate is approved.

## Movement implementation status

**READY FOR SINGLE-AUDIT PREFLIGHT.** The live race path now executes Replenish, Treat/Prepare, Pace payment and Will, Pack preservation, installed Training/Gear, Fuel/remedies, Condition treatment/suppression, mandatory Event timing, Gut Checks, Effective Difficulty boundaries, Finish extension, and same-round placement. Validation uses bounded turn/round fixtures; it does not run the 8-runner marathon.
