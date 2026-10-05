# DRG Run 06 v1.3 cleanup — blocked before implementation

## 1. Baseline

Repository: `/workspace/scratch/c44187d30dd1/DRG-Formal-Run-06-v1.2-fresh` on `main`. HEAD, `main`, and `drg-race-card-redesign-v1.2` all resolve to `5f14c84d594163863a53486cd993f036379cfd8e`. `origin/main` is absent. Tracked working tree was clean before this report; the preserved v1.2 audit report and output directory were the only untracked artifacts.

## 2. Milestone root cause

At P4 round 10, crossing mile 8, the recorded active Conditions were Nausea `CO-012` (Effective Severity 4), Cold Chills `CO-011` (5), Gashed Knee `CO-013` (5), Dead Legs `CO-004` (5), and Dehydrated `CO-010` (5). `resolve_milestones` explicitly remedies Water's Dehydrated condition, then builds an Aid-eligible list and passes only `max(eligible, key=effective_severity)` to `named_remedy`. Gashed Knee won over Nausea, so Water removed Dehydrated and Aid removed Gashed Knee but left Nausea active. Preserved event IDs: `EV-001692`–`EV-001697` in `output/Run-06-v1.2/Simulation-Event-Log.jsonl`. P4 ended that turn at 0 Energy. This is an explicit one-condition selection in the resolver, not a missing card-data remedy.

## 3. Aid implementation

Not started. The requested all-eligible rule is unambiguous, but the task was stopped before partial implementation because the assistance action budget remains unresolved.

## 4. Water implementation

Not started. The present resolver specifically looks up Dehydrated rather than iterating every Water-eligible Condition.

## 5. Board-game assistance rule

The newly supplied rule permits the requester to choose any eligible active runner for a one-for-one swap. Existing canonical text only specifies a three-exchange pre-race trade, costing one move per participant, and does not define in-race assistance action cost.

## 6. Simulation assistance policy

The newly supplied leader/second-place helper selection is clear. No implementation was started.

## 7. Swap scoring/selection

No implementation was started.

## 8. DNF implementation

No implementation was started.

## 9. Runner/result state

No implementation was started.

## 10. Events/audit logging

No implementation was started.

## 11. Tests added

None; no tests were run in this cleanup task.

## 12. P4 mile-8 fixture

Not created.

## 13. P4 recoverable stranded fixture

Not created.

## 14. P4 unrecoverable stranded fixture

Not created.

## 15. Full validation

Not run because the RULES AMBIGUITY stop condition was reached before implementation.

## 16. Files changed

Only this untracked blocked-implementation report was created. No tracked source, tests, rules, or configuration were modified.

## 17. Remaining Rules Review items

**RULES AMBIGUITY — in-race assistance action timing and cost.** The request is said to occur during the final legally available Treat opportunity, but the supplied ruling does not state whether the swap consumes the requester's sole Treat/Prepare action, whether it counts toward the two-card play budget, or whether the helper incurs an action cost outside their own turn. The existing pre-race exchange rule does not answer these in-race questions. Implementing the swap without deciding these would invent action-budget semantics. Resolve these points before assistance/DNF implementation and formal execution.

## 18. Repository safety

The v1.2 audit artifacts were not modified. No v1.3 commit or tag was made; no marathon was run.

# Continuation after frozen assistance action-cost rulings

The preceding numbered sections document the correct pre-implementation stop. This section records the subsequent authorized implementation and validation without changing that history.

## Station resolver and mile-8 fixture

`Sim.resolve_milestones` now visits each active Condition whose station remedy or reduction is listed in `data/rules_config.json`. It resolves Water and Aid independently and applies Hydration Belt Water Energy separately. The bounded P4 mile-8 fixture passes: Dehydrated, Nausea, and Gashed Knee are removed; Twisted Ankle falls from 7 to 4, Heat Exhaustion from 8 to 4; Dead Legs remains unchanged; the Hydration Belt grants 1 Energy; Fuel Effect use becomes legal after Nausea removal. Future configured Water-eligible Conditions are covered by the same iteration.

## Assistance and DNF implementation

The physical rule allows any eligible active helper. The simulation policy selects the current leader, or second place if the requester leads, with stable runner ID for ties. The requester uses the one Treat/Prepare action. The swap uses zero Race-card play slots; the helper incurs no present or future action debt. Both hands and every legal one-for-one swap are evaluated without future draws. Rescue-capable swaps are ranked by continuation Movement, helper's current Victory Directive score loss, value of the card received by the helper, and stable card IDs. A received card enters hand immediately; if it needs Treat/Prepare, its next-turn legal use can prevent DNF. An unsuccessful request makes no trade.

Explicit `ACTIVE`, `FINISHED`, and `DNF` states retain DNF distance, Energy, Will, Conditions, round, turn, and reason. The DNF evaluation checks current legal Movement, recovery and cycling, installed Energy, replenishment possibility, and final assistance. DNF runners have no finish place or future turns; the race loop terminates when all runners are finished or DNF. The 400-turn safety guard remains unchanged. Assistance and DNF events record the request, helper, swap alternatives, result, and cause.

## Focused-test stop and corrected expectation

The first new suite ran 12 tests: 11 passed and `test_received_fuel_next_turn_no_second_treat` failed. Its incorrect expectation was that Nausea would reject a received `FU-001` Energy Gel. The designer confirmed Nausea prohibits Fuel **Effect** use only. `FU-001` has Effort 3 and zero Movement Energy cost, so it can legally rescue through Movement where Course Difficulty permits. The fixture now uses a visible Difficulty 2 position and checks that the swap gives positive Movement and prevents DNF. A separate test confirms Nausea blocks an effect-only Fuel rescue with `FU-002` when its Movement cost is unaffordable. The corrected new suite passes 13/13.

## Bounded fixtures and validation

- P4 mile-8 station fixture: PASS.
- P4 recoverable stranded assistance fixture: PASS.
- P4 unrecoverable stranded DNF fixture: PASS.
- Additional station, helper selection, tie, swap enumeration, action budget, replenishment, and mixed-result fixtures: PASS.
- Prior focused suites: Run 06 repair 10/10; Will/closed rules 13/13; frozen redesign 20/20; AI legality 8/8; AI rationale 9/9; AI Victory 12/12; movement boundaries 18/18; integrated race loop 18/18.
- Full suite: 156/156 PASS.
- `git diff --check`: PASS. Transient Python cache files were removed.

## Changed files for v1.3 baseline

`engine/simulate.py`, `tests/test_v13_cleanup.py`, `DRG-Canonical-Playtest-Rules.md`, `DRG-Course-Rules.md`, `DRG-Rules-Review.md`, `DRG-Superseded-Rules.md`, `README.md`, `simulation/Simulation-State.md`, `simulation/Simulation-Decision-Rules.md`, `simulation/Simulation-Event-Schema.md`, `simulation/Simulation-Configuration.md`, and this report.

Historical v1.2 audit files remain untracked and unchanged. There is no remote in this bundle checkout. The action-cost ambiguity documented above was resolved by the subsequent designer ruling; no assistance action-budget ambiguity remains.
