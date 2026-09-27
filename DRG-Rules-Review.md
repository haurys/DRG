# DRG current Rules Review and playtest registers

This register applies to the 2026-09-25 [canonical playtest rules](DRG-Canonical-Playtest-Rules.md). The original Phase 2A audit and earlier `rules/Rules-Review.md` are historical; questions explicitly answered by the current designer prompts are **closed/superseded**, not reopened. `RULES REVIEW` means no authoritative answer; `PLAYTEST VALUE` means a configurable numeric value is intentionally provisional; `BALANCE WATCH` means observe without changing.

## Simulation-blocking source/data questions

**None.** RR-01 through RR-10, RR-12, RR-14, and RR-15 are resolved by the final pre-simulation freeze. Zero unresolved blocking rules are required for the first integrated marathon.

## Other execution and edge-case questions

| ID | RULES REVIEW question | Affected rule |
|---|---|---|
| RR-11 | Does a Treat/Prepare relocation of already-played Gear consume a slot in the two-card-play budget, given that it consumes an action but is not a *new card play*? Can a runner both relocate and play two Movement cards? | Treat/Prepare economy. |
| RR-13 | Which timing and choice procedure forms multiple consensual Packs simultaneously, and when exactly is a voluntary cohesion stop declared? | Pack decisions/round-end cohesion. |
| RR-16 | Can Electrolytes be used without Dehydrated, and must its named remedy resolve when present? May Salt Tabs choose remedy when no Cramp exists? | Fuel legal actions; do not replace missing behavior with zero. |
| RR-17 | For capped final movement and Finish, how are quarter-mile spaces versus 0.1/0.2 extension handled when a runner arrives at the Course end with exactly exhausted movement? | Finish threshold and positive legal remaining movement. |

## PLAYTEST VALUES (configurable; do not rebalance here)

- Porta-Potty maximum 0.5 mile; Dead Legs persistent for current playtest.
- The frozen Movement Model A conversion and normal two-mile cap, Pace modifiers/costs, start/max Energy 15, Water +1, Aid +2, Pack preserve 1 are the current executable **playtest baselines**. Their numeric tuning is not made permanent by this document.
- Deterministic AI valuation, trade offers, policy tie-breaks, and (if designer permits) deck recycling are simulation-policy assumptions, not hidden game rules. Never treat them as a source for canonical card semantics.

## BALANCE WATCH (not defects)

Competitive marathon target ~25–35 rounds, center ~30; average effective movement ~0.85–1.0 mile/turn; two-mile turns exceptional. Watch Pack preserve 1 and stacking/zero-cost Steady/Race/Push; direct Movement frequency and cap waste; Tailwind, Clear Road, Dog Escort, Friendly Rival, Second Wind E8/E9, Perfect Rhythm E10, Feeling Good, Wild Goose Chase, Porta-Potty, Tough Decision; Condition frequency/treatment value; Event hand congestion/play rate; Tough Decision Condition exposure. No claim of balance follows from one deterministic race.

## Current implementation status

The canonical data, configuration, engine rule path, and focused deterministic tests implement the resolved pre-simulation freeze. RR-11, RR-13, RR-16, and RR-17 remain non-blocking and require documented PLAYTEST ASSUMPTIONS when the single integrated marathon is run.
