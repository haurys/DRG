# DRG Course, milestones, and Finish

FROZEN: 30 reversible 4 × 6-inch **physical Course cards** in the selectable inventory. One physical card carries **two total race miles**: a one-mile lane along one side and a one-mile lane along the opposite side, each divided by four quarter-mile arrows/spaces. The 60 entries in [`data/Course-Cards.md`](data/Course-Cards.md) and [`data/course_cards.json`](data/course_cards.json) are **one-mile side/data records**, not 60 separate physical cards. Their printed Difficulty, elevation, surface, route/condition, and setting have not been rebalanced. Selection, order, and orientation are recorded by deterministic seed and visible before pre-race exchange; no Course information is hidden. No special rule is invented where none is printed.

For a marathon, connect **13 Course cards long-side to long-side** from the **Start/Finish card** at one end. Runners begin at Start, travel away along one side for 13 miles, turn at the far end, and travel back on the opposite side of those same cards for 13 miles, finishing at the Start/Finish end. The physical row is a visible out-and-back layout. Review it to plan Pace, Training/Gear installation, Condition treatment, station approach, and whether to retain or sacrifice a two-turn-eligible slot card.

## Construction

| Format | Physical cards | Outbound | Return | Active segments | Course spaces | Finish extension | Threshold |
|---|---:|---|---|---:|---:|---:|---:|
| Marathon | 13 | Positions 1–13 → miles 1–13 | Opposite sides positions 13–1 → miles 14–26 | 26 | 104 | 0.2 mile | 26.2 miles |
| Half | 7 | Positions 1–7 → miles 1–7 | Opposite sides positions 6–1 → miles 8–13; opposite side of position 7 unused | 13 | 52 | 0.1 mile | 13.1 miles |

Marathon examples: position 1 next to Start/Finish is outbound mile 1/return mile 26; position 13 is outbound mile 13/return mile 14. Mile milestones attach to **race mileage**, not a randomly selected physical card. Each one-mile lane has four 0.25-mile increments. The full Course ends at 26.0 or 13.0; Finish extension is separate.

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

The Finish extension has **no Difficulty**. Exactly reaching 26.0 or 13.0 miles with no remaining Movement does not finish. One positive legal quarter-mile Movement unit beyond the Course endpoint crosses the final 0.2 or 0.1 mile, then stop and lose unused movement. Same-round finishers are simultaneous; complete the full round before placing them. Compare (1) sum of printed Effort **remaining in hand** after used Movement cards leave it, (2) Energy, (3) unspent Will, and (4) shared place if still tied. Conditions have no tiebreak Effort; seat order is never a Finish tiebreak.

Course physical layout: 4 × 6 inches, cards connected long-side to long-side, with two opposite travel lanes and Difficulty, terrain/environment, and elevation positioned for legibility. The separate Start/Finish card anchors one end. Race card size is 2.5 × 3.5 inches. These are presentation specifications, not extra Course Difficulty rules.

## Station treatment — FROZEN v1.3

Crossing Water or Aid resolves every active Condition eligible for that station independently. Water remedies Dehydrated; Aid remedies Nausea and Gashed Knee and reduces Twisted Ankle by 3 and Heat Exhaustion by 4. Zero-Severity nonpersistent Conditions are removed. Station Energy effects resolve separately.

## v1.4 candidate visibility and stations

Reveal the entire Course before pre-race exchanges. A runner can install a specialist before its visible segment, retain it for its Effect, or sacrifice it for Effort only after two complete runner turns. Water and Aid markers stay at the fixed race miles above regardless of card selection or orientation; every eligible active Condition resolves at each station. No Course Difficulty, orientation, or station value changes in v1.4.
