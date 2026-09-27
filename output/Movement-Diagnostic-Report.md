# Movement Model A — Boundary Diagnostic Report

Seed: `20260924`  
Players: `8`  
Format: Full marathon

## Classification

**A — MOVEMENT MODEL A IMPLEMENTED AND VALIDATED**

## Baseline comparison

| Measure | Previous baseline | Boundary update | Change |
|---|---:|---:|---:|
| Rounds | 146 | 182 | +36 |
| Turns | 867 | 1,076 | +209 |
| Average movement | 0.241 mi | 0.193 mi | -0.047 mi (-19.7%) |
| Median movement | 0.00 mi | 0.00 mi | None |
| Maximum movement | 2.00 mi | 2.00 mi | None |
| Zero-movement turns | 534 | 731 | +197 |
| One-Effort-card turns | 695 | 875 | +180 |
| One-card average | 0.199 mi | 0.158 mi | -20.6% |
| Two-Effort-card turns | 48 | 48 | None |
| Two-card average | 1.458 mi | 1.432 mi | -1.8% |
| Energy gained | 203 | 248 | +45 |
| Energy spent | 296 | 339 | +43 |
| First finisher turn | 70 | 100 | +30 |
| Final finisher turn | 146 | 182 | +36 |
| Finishing spread | 76 turns | 82 turns | +6 |

Finish order is recorded for reproducibility but is not treated as balance evidence.

## Movement distribution

| Distance | Previous | Updated |
|---:|---:|---:|
| 0.00 mi | 534 | 731 |
| 0.25 mi | 118 | 131 |
| 0.50 mi | 91 | 101 |
| 0.75 mi | 55 | 48 |
| 1.00 mi | 25 | 24 |
| 1.25 mi | 13 | 14 |
| 1.50 mi | 16 | 11 |
| 1.75 mi | 11 | 5 |
| 2.00 mi | 4 | 11 |

## Boundary behavior

- Boundary crossings: 200
- Harder terrain: 72
- Easier terrain: 88
- Equal Difficulty: 40
- Movement Result removed by applied harder transitions: 170
- Movement Result added by applied easier transitions: 114
- Net boundary adjustment: -56 Movement Result
- Harder transitions that stopped movement at the boundary: 26
- Turns crossing multiple boundaries: 21
- Turns where the two-mile cap prevented additional movement: 0
- Movement Result wasted above the cap: 0

All eight runners crossed the same 25 mile boundaries. A boundary reached with no positive carried remainder is logged, but its new Difficulty does not revive exhausted movement.

## Pace breakpoints

| Pace | Turns | Share |
|---|---:|---:|
| Easy | 807 | 75.0% |
| Steady | 5 | 0.5% |
| Race | 141 | 13.1% |
| Push | 123 | 11.4% |

- Pace changes that increased actual movement: 70
- Pace changes that did not increase actual movement: 162
- Energy spent on upward Pace changes producing no movement gain: 74

The counterfactual uses the same cards, position, terrain, and state with the runner's preceding Pace. It measures conversion breakpoints without changing AI policy.

## Hand economy

- Minimum hand size at the decision point: 1
- Turns with 0 cards in hand: 0
- Turns with 1–2 cards in hand: 1,028 of 1,076 (95.5%)
- One-Effort-card plays: 875
- Two-Effort-card plays: 48
- Mixed Effort + Energy/Effect plays: 7
- Energy/Effect + Energy/Effect plays: 1
- Voluntary no-card turns: 0
- Average hand size falls to 1.18 at Mile 10 and remains 1.00 from Mile 11 onward.

Hand size is measured after the mandatory draw/replacement sequence and before voluntary play.

## Material behavior caused by the boundary rule

The corrected rule materially lengthened the run because harder transitions can terminate a movement action at a boundary, while easier transitions only help when positive Movement Result remains to carry. The net applied boundary adjustment was negative, and the longer race produced additional draws, Energy transactions, and one-card turns. Two-card Effort performance changed only slightly; the largest effect occurred on the much more frequent one-card turns.

## Apparent pressure points — observation only

- Zero-movement turns increased to 67.9% of all turns.
- Two Effort cards remained uncommon but produced substantially more movement than one-card turns.
- 162 Pace changes failed to cross a movement breakpoint; 74 Energy was spent on upward changes without an actual movement gain.
- Hand size reached approximately one card by Mile 10 and remained there.
- Harder transitions removed more Movement Result than easier transitions restored.
- The two-mile cap was reached 11 times, but no turn had positive excess beyond it.

No numeric values or strategies were changed in response to these observations.

## Implementation interpretation

“Carry the excess” is implemented as carrying only positive Movement Result. Reaching a boundary with zero or negative remainder records the crossing and ends movement; an easier next segment does not create movement from an exhausted remainder. This is the only boundary interpretation needed beyond the approved rule text.
