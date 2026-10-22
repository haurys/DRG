# v1.4 Turn and Action Flow

## What this document is

A practical answer to “What do I do on my turn?” and to the surrounding round timing.

## How to use it

Follow steps in order. The table identifies whether a step is mandatory, optional, or consumes an action/card.

## Key takeaways

Pace locks at Round Start; the normal draw is at most one below six; one Treat/Prepare and two card plays are different budgets; slot Movement pays and counts like hand Movement.

## Two separate budgets

| Action | Treat/Prepare (one per turn) | Race-card plays (maximum two per turn) | Normal remaining plays |
|---|---:|---:|---:|
| Install Training or equip/replace Gear from hand | 1 | 1 | 1 |
| Use Fuel Effect from hand | 1 | 1 | 1 |
| Treat/remedy Condition or attach compatible Gear from hand | 1 | 1 | 1 |
| Relocate already-equipped eligible Gear | 1 | 0 new plays | 2 |
| Request assistance | 1 | 0 | 2 |
| Direct Slot Movement (after two-turn delay) | 0 | 1 | 1 |
| Two legal Movement cards from hand/eligible slots | 0 | 2 | 0 |

Each new-card Treat/Prepare play has **zero Movement Effort**. No second Treat/Prepare is granted after installation, treatment, relocation, or assistance. A runner may use the remaining legal Movement play(s) if payment and timing permit.

## Before the turn: same-time round setup

1. Activate staged Global effects. Each active runner selects one legal Pace simultaneously; record Round Start positions and Pace. From round 2 onward, form same-Pace Packs within 0.5 mile of a leader; no Pack forms in round 1. Pace selection is **mandatory once per round** and is not a Race-card play.
2. Resolve each runner’s turn sequentially; this administrative order does not make their race times sequential. FINISHED and DNF runners have no turn.

## Your turn in order

| Step | Requirement and budget | What to do | Consequence |
|---|---|---|---|
| 1. Replenish | Mandatory check, at most one normal draw | If hand has fewer than six normal cards, draw one; auto-place revealed Conditions and seek the replacement. Recycle eligible discard if draw empty. | If both piles lack eligible cards, skip; hand may remain zero. |
| 2. Treat/Prepare | Optional, **once per turn** | Install/replace Training or Gear; attach compatible Gear; use Fuel Effect; relocate eligible equipped Gear; or request stranded assistance. | Playing a new card here consumes one of two plays, contributes no Effort. Relocation/assistance uses the action but no new play. Installed Effect starts immediately. |
| 3. Select Movement cards | Normally mandatory; total at most two plays, at most one Event | Select hand cards and/or continuously installed, two-turn-eligible Training/Gear. An Event may use Movement or legal Effect mode. | A slot card is removed and loses Effect before payment and Effort calculation; its printed Effort cost applies. Attachments never qualify. |
| 4. Pay | Mandatory for selected legal turn | Calculate Pace cost after preservation and per-card Movement Energy. Spend Energy, then optionally one Will for the exact otherwise-legal shortfall. | Later Event/station gains do not pay the earlier cost; an unaffordable plan is illegal. |
| 5. Resolve Movement and Effects | Mandatory | Convert Effort to quarter-miles, apply direct modifiers, traverse boundaries; resolve Event at printed timing. | Check side Difficulty and Condition modifiers, two-mile cap, current/staged Effect timing, target legality. |
| 6. Milestones | Mandatory if crossed | At fixed Water/Aid treat **all** eligible Conditions and station Energy separately. At a Marathon Gut marker pause and check Prepared Effort in hand and normal Training/Gear slots plus bonuses, and stored Energy (exact shortfall may use Will). | Pass clears that checkpoint and continues Movement; fail stops there, loses remainder, and begins 4/3/2 recovery turns at miles 10/18/23. Half retains hand-only checks and old failure cost. |
| 7. End | Mandatory once | Record post-turn state and expire temporary items. Outside Gut recovery, evaluate exhausted continuation including slots, future draw, stations, and assistance. | Gut-stalled runners retain their complete recovery window before a distinct Gut DNF. |

At **Round End**, observe Pack cohesion, assign places for all same-round finishers by hand Effort/Energy/unused Will, expire round effects, and advance the round if anyone remains active.

**Gut recovery turn (Marathon):** Replenish normally. Use at most one normal Treat/Prepare (including Fuel or one-for-one assistance); recalculate both Prepared Effort and Energy after each change. On the first recovery turn only, if still failing after Replenish/Treat and holding six cards, optionally discard one chosen hand card and draw one legal replacement. Will can pay only the exact missing Gut Energy once per race. If the check passes, clear the stall and use the remaining legal card-play budget for Movement that turn; otherwise end without Movement. After the fourth/third/second failed recovery turn at miles 10/18/23, record `failed_gut_check` DNF. The current 25/4, 30/2, 35/1 threshold pairs are provisional simulation inputs.

## Common turns

- **Build:** draw one below six, choose Steady, play one Training into an empty slot using Treat/Prepare **and the first card play**, then use the single remaining play for one affordable hand Movement card. Training starts helping at installation; it cannot be sacrificed this turn or next.
- **Travel light:** with hand zero and an eligible Gear slot, draw one if possible; choose legal Pace and move using Gear directly, perhaps alongside the drawn hand card. The Gear Effect ends before Energy payment and Course calculation; the slot empties.
- **Recover:** at zero Energy, use Fuel for +2 Energy through Treat/Prepare if no active Nausea, then play a zero-cost Movement card. If the normal paid plan has a shortfall, unused Will can cover that exact amount. Fuel contributes no printed Effort when used for recovery.
- **Help:** a stranded runner spends Treat/Prepare on one legal assistance swap. The received card enters hand immediately. Its zero-cost Movement can be used within remaining play allowance now; a received Fuel Effect waits until a later legal Treat/Prepare opportunity.
- **No target:** when everyone else has FINISHED or DNF, a Crowd Support Effect requiring another active runner is illegal. Its ordinary Movement mode remains available if payment and card budget permit.
