# DRG Course, milestones, and Finish

FROZEN: 30 reversible 4 × 6-inch physical Course cards, each with two one-mile travel sides and four quarter-mile runner positions per side. The existing per-side inventory in [`data/Course-Cards.md`](data/Course-Cards.md) and [`data/course_cards.json`](data/course_cards.json) contains IDs C-01-A through C-30-B, printed Difficulty, elevation, surface, route/condition, and setting; **those baseline numbers have not been rebalanced**. Current Course is selected, ordered, and oriented by recorded deterministic seed and visible before pre-race exchange. Runner tokens sit beside card edges; card orientation decides outbound/return side. No special Course rule is invented when none is printed.

## Construction

| Format | Physical cards | Outbound | Return | Active segments | Course spaces | Finish extension | Threshold |
|---|---:|---|---|---:|---:|---:|---:|
| Marathon | 13 | Positions 1–13 → miles 1–13 | Opposite sides positions 13–1 → miles 14–26 | 26 | 104 | 0.2 mile | 26.2 miles |
| Half | 7 | Positions 1–7 → miles 1–7 | Opposite sides positions 6–1 → miles 8–13; opposite side of position 7 unused | 13 | 52 | 0.1 mile | 13.1 miles |

Marathon examples: position 1 outbound mile 1/return mile 26; position 13 outbound mile 13/return mile 14. Mile milestones attach to **race position**, not the random card. Each one-mile side contributes 0.25-mile spaces. The full Course ends at 26.0 or 13.0; Finish is separate.

## Per-side inventory and terminology

The stored 60 sides are authoritative: Difficulty 1:9, 2:14, 3:9, 4:12, 5:5, 6:7, 7:1, 8:3; weighted total 210; mean 3.5. The older aggregate is superseded. Elevations are Steep Descent, Descent, Flat, Rolling, Incline, Steep Incline. Track is not a printed surface in this inventory.

## Movement Model A and boundary

Total printed Movement-card Effort + applicable Effort modifiers + Pace modifier − Effective Difficulty − applicable Condition/Effort penalties produces integer result. Effective Difficulty is printed Difficulty plus penalties (including numeric Sore Feet and Sudden Rain) minus reductions (Hill Repeats: Incline 2, Steep Incline 1; Downhill Practice: Descent 2, Steep Descent 1). Convert ≤0→0 through ≥15→2.00 miles using the existing table. Apply direct ±Movement afterward at 0.25 mile per point. Direct Movement stays separate, is never converted to Effort, and is not changed by boundary Difficulty accounting.

At each boundary stop and immediately recalculate Effective Difficulty. Completed quarter-mile increments debit **two** integer Movement Result each. Carry only unused positive result. `difficulty_change = new_effective_difficulty - old_effective_difficulty`; `adjusted_remaining = remaining - difficulty_change`; continue only if adjusted remainder >0. Repeat for every boundary. This adjustment applies only to Base Movement, never Direct Movement.

## Fixed stations and Gut Checks

| Race | Water miles | Aid miles | Gut Check mile → requirement |
|---|---|---|---|
| Marathon | 4, 8, 12, 16, 20, 24 | 8, 16, 24 | 10→25; 18→30; 23→35 (**PLAYTEST VALUES**) |
| Half | 3, 6, 9 | 6 | 6→9; 11→11 |

At a Gut Check, sum printed Effort on every Race card remaining in hand and add active Strength +1, Mental Toughness +3, and Pace Band +2. Committed Movement cards are absent; empty hand equals zero. No card is consumed. Pass at or above threshold; failure costs 2 Energy; continue remaining legal Movement.

## Finish

The Finish extension has **no Difficulty**. Any positive legal remaining movement sufficient to cover the final 0.2 or 0.1 mile finishes, then stop and lose unused movement. Same-round finishers are simultaneous; complete the full round before placing them. Compare (1) sum of printed Effort **remaining in hand** after used Movement cards leave it, (2) Energy, (3) unspent Will, and (4) shared place if still tied. Conditions have no tiebreak Effort; seat order is never a Finish tiebreak.

Course physical layout: portrait 4 × 6 inches, mirrored/reversible halves, with Difficulty, terrain/environment, and elevation positioned for legibility. Race card size is 2.5 × 3.5 inches. These are presentation specifications, not extra Course Difficulty rules.
