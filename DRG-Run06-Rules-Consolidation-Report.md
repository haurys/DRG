# DRG rules consolidation and Will correction

**Baseline:** `drg-race-card-redesign-v1.1` → `1924ea771eff85107bda67eaf3f5d3de26266050`
**Status:** validated in bounded fixtures; no full marathon, commit, or tag.

## Preserved audit and repair

The interrupted seed-20260930 Run 06 remains incomplete: 17 full rounds, 139 complete turns, P4 round-18 exception, no finisher. `DRG-Marathon-Audit-Run-06.md` and every file in `output/Run-06/` remain untouched. The complete fallback plan schema in `engine/simulate.py`, deterministic audit-only set serialization in `audit/run_output.py`, and their regression tests remain intact. `DRG-Run06-Blocking-Repair-Report.md` is historical evidence of the former Pace-only Will rule; this report supersedes its Will interpretation without editing it.

## Final rulings and implementation

| Ruling | Final behavior | Implementation and bounded evidence |
|---|---|---|
| RR-11 — CLOSED | Relocation of played Gear occupies the sole Treat/Prepare action, spends no new-card play, and leaves two card-play slots for Movement. | Existing `resolve_treat_prepare()` returns zero used plays for relocation; new full-turn test plays two Movement cards after relocation. |
| RR-13 — CLOSED | After Round Start Pace selection, same-Pace runners within 0.5 mile of a leader join the nearest legal Pack; exact leader-distance ties use stable runner ID. Membership stays fixed for the round and is reevaluated at the next Round Start. | `form_packs()` explicitly chooses nearest eligible leader. Round End emits observational cohesion without mutating membership; a bounded separation/next-round fixture confirms delayed exit. |
| RR-16 — SUPERSEDED | Electrolytes chooses exactly +2 Energy or Remedy Dehydrated; Salt Tabs chooses exactly +2 Energy or Remedy Cramp. Energy does not require the named Condition; remedy does. Nausea's general Fuel prohibition still applies. | Existing Fuel legality/use code retained; branch tests verify remedy eligibility and zero Energy gain on remedy. Printed values unchanged. |
| RR-17 — CLOSED | At exactly 26.0/13.0 with no legal Movement left, the runner is not finished. One positive quarter-mile unit beyond the Course endpoint crosses the respective 0.2/0.1 extension, with no Difficulty. | Existing finish resolver retained; bounded Marathon and Half Marathon edge tests pass. |

The Rules Review register retains all four identifiers with former questions, final rulings, closure context/date, and implementation status.

## Will: combined Energy payment

The former Pace-only Will fallback is removed. For each proposed legal turn, the AI preview and live turn calculate **Pace cost after preservation + all Movement-card costs**. Installed Gear/Training Energy triggers and legal Fuel preparation resolve before payment. Stored Energy pays first; one available Will covers exactly the remaining shortfall. It never adds stored Energy, Effort, Movement, or a Pace exception. A runner may finish at 0 Energy.

The live turn determines selected cards/modes and nominal combined cost before payment. `WILL_USE` records one shortfall, `PACE_PAYMENT` records actual stored Pace payment, and every `MOVEMENT_ENERGY_PAYMENT` records nominal cost, stored amount paid, and Will-covered amount. For each card, stored paid plus Will coverage equals nominal cost. No-Will behavior keeps the established affordable-Pace step-down and rejects unaffordable Movement cards. The preview and AI rationale now use the same combined payment model. No Will-use threshold was added; the existing Victory score can spend Will for faster progress or a finishing line.

**Historical P4 state under the new rule:** P4 at 9.5 miles, Easy Pace, 0 Energy, active Nausea, Will available, seven cards each costing 1 Energy for Movement. The deterministic fixture selects FU-017 and GE-018 in Movement mode, projects and executes one mile, records a 2-Energy Will shortfall, leaves stored Energy at 0, spends Will, and reaches TURN_END. No Fuel Effect was used. With Will marked unavailable in the same state, no normal complete plan survives; the repaired complete-schema empty fallback executes deterministically through TURN_END with zero Movement and no KeyError.

## Energy accounting and Victory Directive tests

Bounded fixtures cover Pace-only, Movement-only, combined, multiple-card, and exact stored-Energy payments; Pack plus Long Run preservation and Running Shoes Energy before shortfall; spent Will; finish at zero; and illegal unaffordable cards without Will. Repeated P4, no-Will fallback, Pace-only, Movement-only, combined, and final-segment fixtures produce identical plans, card modes, score, rationale, Movement, Energy, Will state, and event payloads. The existing P1 round-1 two-card WIN_SPEED decision remains asserted in the Run 06 regression suite. No evaluator weights or AI profile identities changed.

## Validation

| Suite | Result |
|---|---:|
| Updated Run 06 repair | 10/10 PASS |
| New Will and closed-rules tests | 13/13 PASS |
| Frozen redesign | 20/20 PASS |
| AI legality | 8/8 PASS |
| AI rationale | 9/9 PASS |
| AI victory | 12/12 PASS |
| Movement boundaries | 18/18 PASS |
| Integrated race loop | 18/18 PASS |
| Full suite | **143/143 PASS** |

`git diff --check` passed. Race Card JSON, Course JSON, printed Effort, Movement Energy bands, starting/maximum Energy, Pace costs, Gut Check thresholds, and AI profile identities did not change. Comparison of `simulation/config.json` with HEAD confirms every executable/balance value is identical; only the Will rule descriptor and canonical Pack descriptor changed.

## Files changed in this consolidation

- Engine/AI: `engine/simulate.py`, `engine/ai_rationale.py`.
- Tests: `tests/test_will_consolidation.py`, `tests/test_run06_repair.py`, `tests/test_frozen_redesign.py`, `tests/test_ai_victory.py`.
- Canonical/current documentation: `DRG-Canonical-Playtest-Rules.md`, `DRG-Course-Rules.md`, `DRG-Rules-Review.md`, `DRG-Superseded-Rules.md`, `README.md`, `data/Component-Manifest.md`, `rules/Race-Formats.md`, `rules/Rules-Review.md`, `simulation/Simulation-Configuration.md`, `simulation/Simulation-Decision-Rules.md`, `simulation/Simulation-Event-Schema.md`, `simulation/Simulation-State.md`, `simulation/config.json`.
- This report: `DRG-Run06-Rules-Consolidation-Report.md`.

The earlier uncommitted `audit/run_output.py`, `DRG-Run06-Blocking-Repair-Report.md`, and preserved Run 06 artifacts also remain in the working tree. No commit or tag was created.
