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

Marathon Gut recovery is now implemented with Prepared Effort in hand and normal slots plus specialist bonuses, a separate Energy requirement, exact-shortfall Will, a checkpoint stop, and four/three/two recovery turns. The first-turn full-hand special exchange is one card after Replenish/Treat; assistance remains a one-for-one use of the available Treat/Prepare. The 25/4, 30/2, 35/1 test pairs are provisional configuration values pending calibration. Half Marathon keeps the hand-only check. Older historical audit results predate both this implementation and the round-1 Pack restriction.

## v1.3 closures

Station treatment applies to every eligible Condition. In-race assistance uses the requesting runner's Treat/Prepare action, no Race-card play slot, and no helper out-of-turn action cost. The requesting player may choose any eligible active helper. DNF requires exhausted practical continuation after assistance. These action-cost questions are closed.

## v1.4 candidate qualification

RR-11 is superseded **for Condition-attached Gear**: once attached it cannot relocate or return to hand/slot and discards on complete Condition removal. Moving an equipped Gear into a compatible attachment remains a Treat/Prepare action. The v1.4 candidate retains the unresolved historical direct-Movement boundary accounting item without changing the current engine resolution.

**RESOLVED — descriptive Gear category versus footwear legality.** The prior `category` values marked Running Socks as Footwear, Tempo Trainers as Apparel, and Carbon Racers as Accessory, despite established shoe legality saying the opposite. The v1.4 remediation explicitly authorizes alignment: Gear now has `is_footwear` as the **only machine-readable category-like equip restriction**; the six physical shoe cards (Road Trainers ×2, Cushion Trainers, Trail Shoes, Tempo Trainers, Carbon Racers) are true, Running Socks is false. Descriptive categories have been aligned (`GE-003` Apparel, `GE-007`/`GE-011` Footwear) but do not enforce any restriction themselves. No apparel/accessory/technology/support slot limit exists. The historical direct-Movement boundary-accounting question remains RULES REVIEW and nonblocking; no new ruling was invented.
