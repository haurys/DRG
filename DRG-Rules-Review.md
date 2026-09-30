# DRG current Rules Review and playtest registers

This register applies to the 2026-09-30 frozen Race Card [canonical playtest rules](DRG-Canonical-Playtest-Rules.md). The original Phase 2A audit and earlier `rules/Rules-Review.md` are historical; questions explicitly answered by the current designer prompts are **closed/superseded**, not reopened. `RULES REVIEW` means no authoritative answer; `PLAYTEST VALUE` means a configurable numeric value is intentionally provisional; `BALANCE WATCH` means observe without changing.

## Simulation-blocking source/data questions

**None.** RR-01 through RR-10, RR-12, RR-14, and RR-15 are resolved by the final pre-simulation freeze. Zero unresolved blocking rules are required for the first integrated marathon.

## Open execution and edge-case questions

**None of RR-11, RR-13, RR-16, or RR-17 remain open.**

## Closed / superseded register — 2026-09-30 designer freeze

| ID | Former question | Final ruling | Implementation status |
|---|---|---|---|
| RR-11 | Whether relocation consumes Treat/Prepare or a new card-play slot. | Relocation occupies Treat/Prepare, is not a new Race card play, and leaves ordinary Movement allowance; no second Treat/Prepare. | Closed; live relocation uses zero new-card budget. |
| RR-13 | Timing and choice among legal Packs; mid-round exit. | Form at Round Start after Pace selections; same Pace, within 0.5 mile of leader; nearest eligible leader, exact tie by stable runner ID. Membership fixed for round; reevaluate next Round Start. | Closed; deterministic grouping and round-fixed membership. |
| RR-16 | Electrolytes/Salt Tabs eligibility and branch resolution. | Each chooses +2 Energy or the named remedy, never both. Energy always legal; remedy only with its named Condition. | Superseded by redesign; legal action and one-branch tests. |
| RR-17 | Finish extension when Course endpoint is reached with no movement left. | Must have positive legal Movement beyond 26.0/13.0; one quarter-mile unit covers 0.2/0.1 extension; exact endpoint without remaining movement is not Finish. | Closed; finish resolution and boundary tests. |

## PLAYTEST VALUES (configurable; do not rebalance here)

- The frozen 108-card inventory and its Effort-band Energy costs, printed Effects, swaps, and Gut Check modifiers are authoritative for this pass.
- Existing Movement Model A, normal two-mile cap, Pace costs, starting/max Energy 15, Pack preservation, Course and milestones are unchanged. Deterministic AI uses the now-canonical RR-13 Pack selection procedure.

## BALANCE WATCH (not defects)

Competitive marathon target ~25–35 rounds, center ~30; average effective movement ~0.85–1.0 mile/turn; two-mile turns exceptional. Watch Pack preserve 1 and stacking/zero-cost Steady/Race/Push; direct Movement frequency and cap waste; Tailwind, Clear Road, Dog Escort, Friendly Rival, Second Wind E8/E9, Perfect Rhythm E10, Feeling Good, Wild Goose Chase, Porta-Potty, Tough Decision; Condition frequency/treatment value; Event hand congestion/play rate; Tough Decision Condition exposure. No claim of balance follows from one deterministic race.

## Current implementation status

The 2026-09-30 designer consolidation closes RR-11, RR-13, and RR-17 and marks RR-16 superseded by the redesign. Will now covers exact total turn Energy shortfall after reductions, including Movement cards. Historical audit reports retain the rules under which they were run; no new full marathon was run in this implementation pass.
