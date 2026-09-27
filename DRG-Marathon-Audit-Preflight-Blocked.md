# DRG Single Deterministic Marathon Audit — Preflight Blocked

Date: 2026-09-26  
Configured seed: `20260924` (not consumed for an audited race)  
Audited marathon runs performed: **0**  
Preflight note: the required 40-test suite includes an in-memory determinism test that invokes the existing simulator twice with the configured seed. These were test executions, not the requested audited marathon, and they produced no audit output.

## Result

**BUG — BLOCKING IMPLEMENTATION MISMATCH**

The canonical Markdown and structured inventories match the stated integration baseline, and all 40 tests pass. The executable race loop does not implement enough of the frozen canonical systems to conduct a rules-faithful marathon. Per the audit instruction, the race was not started, no Course was generated for the audit, and no alternate seed was run.

## Verified baseline

- Tests: 40/40 PASS
- Race cards: 108
- Families: Training 20; Gear 20; Fuel 22; Event 30; Condition 16
- Duplicate physical IDs: 0
- Missing physical IDs: 0
- Course sides: 60
- Weighted Difficulty: 210
- Mean Difficulty: 3.5
- Duplicate Course-side IDs: 0
- Missing Course-side IDs: 0

## Blocking executable-path findings

1. `simulation/config.json` explicitly says most card effects are not executed: only standalone signed Energy values are applied.
2. The configuration marks Will as unused, contradicting the frozen canonical Will payment rule.
3. The configuration and engine disable Pack Energy preservation; Pack transitions are logged with `benefit: none; RULES REVIEW`.
4. The race loop has no Treat/Prepare decision phase. It cannot install Training, equip/attach Gear, consume Fuel for remedies, relocate Gear, or replace installed cards.
5. Runner state has no active-Training collection. Effective Difficulty is called with an empty Training list, so Hill Repeats and Downhill Practice cannot affect a race.
6. Condition helper functions support remedies and suppression, but the race loop never invokes treatment or Gear suppression. Effective Severity rebound and zero-severity behavior therefore cannot be exercised through play.
7. Binary Condition restrictions are calculated by helpers but not enforced by Pace selection. Cramp, Twisted Ankle, Heat Exhaustion, Dehydrated, Tight Calf, and Blister cannot govern legal Pace or its full Energy cost as required.
8. Gut Checks call the helper without active Training or Gear, so Strength, Mental Toughness, and Pace Band modifiers can never apply.
9. Event integration is partial. The loop special-cases Sudden Rain, Tough Decision, High Five, and Helpful Runner, but all other mandatory Event effects are ignored. Card-play logging labels Effort-mode Event effects as `none`.
10. Finish occurs immediately at the 26.0-mile Course endpoint. The separate 0.2-mile positive-movement Finish extension and same-round placement/tiebreak procedure are not executed.
11. The 40-test suite primarily validates helper functions and data. It does not verify these systems through the full `Sim.turn()` / `Sim.run()` path, allowing the integration mismatch to pass.

## Classification

- Canonical rule ambiguity discovered: none.
- Existing non-blocking RULES REVIEW items remain RR-11, RR-13, RR-16, and RR-17.
- New finding: **BUG**, not a new permanent rules decision.
- Rules-faithful continuation possible: **No**.
- Ready for broader batch simulation: **No**.

## Required next gate

Complete and integration-test the frozen systems in the executable race path, then repeat this preflight. The deterministic marathon audit must still use exactly one seed after that gate passes.
