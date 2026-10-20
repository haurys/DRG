# v1.4 Complete Gameplay Rules List

## What this document is

A standalone player reference for the current v1.4 candidate.

## How to use it

Read A–AJ in game order; use the quick reference during play. Card specifics appear in the complete family tables.

## Key takeaways

Six is the hand maximum, not a refill; eligible slots are a delayed Movement source; attached treatment is committed; all runners share each round’s race-time interval.

## A. Game setup

Choose marathon (26.2 miles) or half (13.1); select runners/profiles, shuffle Race and Course supplies with separately tracked zones. Deal six non-Condition Race cards per runner, resolving drawn Conditions immediately and replacing that draw until a normal card or exhaustion. Reveal the whole assembled Course before exchanges. Each runner has three total pre-race exchange moves; a one-for-one trade costs one move to each participant, a Deck Exchange one move, and acquired cards lock.

## B. Player count

Support 4–12 runners, preferably 6–8; 12 requires tabletop validation. Do not extrapolate a 13–20-player expansion.

## C. Course setup

For a marathon, connect 13 physical two-mile Course cards long-side to long-side from the Start/Finish card at one end. Each card carries a one-mile outbound lane and an opposite one-mile return lane, each with four quarter-mile arrows/spaces. Runners start at Start, travel out along one side, turn, and return along the other to finish at the Start/Finish end. The 30-card inventory has 60 one-mile side records in simulation data; a side record is not a whole physical card. All lanes are visible for Pace, Training/Gear, treatment, station approach, slot retention, and sacrifice planning. A half marathon uses seven physical cards and 13 one-mile lanes, leaving the seventh card’s opposite return lane unused. The separate Finish extension is 0.2 or 0.1 mile; station mileage stays fixed.

## D. Hand / draw

Six normal Race cards maximum, no minimum. At Replenish, if below six, draw exactly one normal card, skipping any revealed Condition into play and continuing for the one replacement. No automatic refill, return of slotted cards, or End-turn draw. If at six, skip normal draw.

## E. Round structure

Round Start activates staged Global effects, locks simultaneous Pace choices and Round Start positions, forms Packs, and snapshots public state. Runners resolve Replenish → Treat/Prepare → Movement → End sequentially in the same race-time interval. Round End observes cohesion, assigns simultaneous Finish places, expires effects, and cleans up.

## F. Runner turn structure

Draw if eligible; optionally take one Treat/Prepare action; then normally play one or two Race cards, with at least one used for Movement. A Move may be hand or eligible slot. A Treat/Prepare card itself gives no Effort. Two Treat/Prepare actions or a normal zero-card turn are illegal absent a specific override; simulator forced fallback is recorded when no legal path exists.

## G. Race-card use

A non-Condition card has one use mode: Movement gives printed Effort and no Effect; Effect gives the Effect and no printed Effort. Two played-card maximum per turn and one Event maximum. A slot sacrifice counts as a played card; assistance and relocating existing Gear do not use a play slot.

## H. Effort

Printed Effort from committed Movement cards is immediate, never stored. Add legal Pace and installed modifiers; subtract starting Effective Difficulty and applicable Condition penalties. Neither a Treat/Prepare card nor Event Effect supplies its printed Effort.

## I. Movement Energy

Printed Effort 1–3 costs 0 Energy, 4–6 costs 1, and 7+ costs 2 per Movement card. Pace cost is separate; applicable preservation reduces Pace cost, not the Movement-card band. Pay the complete otherwise-legal turn cost before Movement; later gains cannot finance it.

## J. Movement conversion

After modifiers convert result ≤0→0, 1–2→0.25, 3–4→0.50, 5–6→0.75, 7–8→1.00, 9–10→1.25, 11–12→1.50, 13–14→1.75, ≥15→2.00 miles. Direct +/− Movement adjusts quarter-mile units. Floor zero, normal cap two miles. At a one-mile boundary carry only positive integer remainder after debiting 2 per completed quarter-mile and adjust by new minus old Difficulty; stop at nonpositive remainder. Do not start a fresh Movement calculation.

## K. Pace

Easy +0 Effort/base 0 Energy; Steady +1/1; Race +2/1; Push +3/2. Select simultaneously at Round Start and lock for the round, subject to Conditions and affordability. An unaffordable Pace may step down; selecting a Pace is not a card play.

## L. Energy

Begin and cap at 15; Energy persists and never regenerates automatically. Card/station/Event gains follow their printed triggers and cap. A runner may have zero Energy and may finish at zero.

## M. Training

Two active slots; install by Treat/Prepare and start Effect immediately. Temporary duration counts installation turn as Turn 1. Resistance may reduce one eligible active Condition on install and future acquisitions under the existing stacking rule. Replaced/expired cards discard; Training never attaches.

## N. Gear

Two normal equipped slots; at most one Footwear. `is_footwear` marks Road Trainers (two copies), Cushion Trainers, Trail Shoes, Tempo Trainers, and Carbon Racers as shoe cards; Running Socks are not footwear. Broad `category` labels describe Gear and impose no further limits. Install a new Gear card through Treat/Prepare and one card play. Some compatible Gear attaches to a Condition instead, outside the equipped slots; committed attachments cannot be used as active equipped Effects or Effort.

## O. Slot installation

Installation uses the one Treat/Prepare opportunity and one of two card plays. Replacing an occupied legal slot discards the old card, never returns it to hand, and starts the new card’s own age at installation turn. Installed Effects begin immediately.

## P. Two-turn slot commitment

A slotted Training/Gear card must survive two complete runner turns continuously: install turn 10, still in slot turn 11, first eligible turn 12. Leaving, replacement, reassignment, expiration, or removal resets that physical card’s continuous installation age.

## Q. Direct Slot Movement

After eligibility, remove installed Training/Gear directly from its normal slot, terminate Effect, recompute legality and payment without it, use printed Effort and normal Movement Energy, count one play, resolve Movement, discard. No hand return or Treat/Prepare needed. Hand+hand, hand+slot, and slot+slot remain within two plays; attachments never qualify.

## R. Condition system

Condition cards auto-enter on draw and do not enter hand. Track printed Base Severity, permanently treated Current Severity, and temporarily suppressed Effective Severity (floor zero); only positive Effective Severity imposes penalties. Remove nonpersistent Conditions at zero; persistent zero can remain. Suppression rebounds when its source leaves.

## S. Condition treatment attachments

Compatible new Gear attached via Treat/Prepare and one card play is committed to its specific Condition outside normal slots. It cannot move, be slotted, traded, reassigned, or establish DNF continuation. Partial Severity treatment leaves it attached. When the Condition is completely removed by any legal means, discard every attached card. Persistent zero is not removal.

## T. Fuel

Fuel Effect uses Treat/Prepare and one of two card plays, yielding either +2 Energy or its printed remedy/Severity reduction, never both. The remedy requires its named active Condition; Energy choice may be used without it. Nausea prints `Cannot use Fuel`: while active, it blocks Fuel Effect use only; legal Fuel Movement still uses printed Effort and normal Movement Energy. Used Fuel discards.

## U. Events

At most one Event per turn during Movement; choose Effect with zero printed Effort or ordinary Movement with Effort and Energy cost. Current, after-Movement, staged next-round, Course, and Global effects resolve in their defined order. Staged cards remain out of discard until expiration.

## V. Event targeting

An Effect requiring another runner needs an eligible other ACTIVE runner (neither finished nor DNF). Finished/DNF runners are not targets. If none exists, Effect mode is illegal but Movement may remain legal. OTHER Target Lock prevents targeting an already locked opponent with another staged/active OTHER Event until expiration; targetless/global/self effects obey their own rules.

## W. Packs

At Round Start, same-Pace runners within 0.5 mile of a Pack leader form a Pack of at least two without distance chaining; tie by nearest leader then ID. Membership locks for the round. Save one Pace Energy, stack preservation to floor zero; Round End cohesion is observational.

## X. Treat / Prepare

One Treat/Prepare opportunity per turn may install/replace Training or Gear, use Fuel Effect, attach compatible Gear, treat/remedy a Condition with a new card, relocate eligible already-played Gear, or request stranded assistance. Any new card played from hand for this action consumes **both** the Treat/Prepare opportunity **and one of two card plays**; it contributes no printed Movement Effort. Installing a Training or Gear card therefore normally leaves only one Movement card play; relocation and assistance consume the action but no new card play. No second Treat/Prepare is granted.

## Y. Assistance

A stranded requester can seek one-for-one hand swap with any eligible active runner using the requester’s Treat/Prepare action. Helper pays no current/future action cost. Swap uses no Race-card play; received card enters hand immediately. It may be used in remaining card allowance if otherwise legal, or enable next-turn treatment. Simulation alone selects leader (or second if requester leads) and best legal rescue deterministically; do not force meaningless swaps.

## Z. Will

One Will use per runner per race covers the exact Energy shortfall for an otherwise-legal Pace/Movement turn after stored Energy and preservation. It neither adds stored Energy nor Effort nor an illegal card/action. It can pay for slot-derived Movement. A spent Will cannot pay again.

## AA. Water

Marathon mile 4/8/12/16/20/24; half 3/6/9. Treat every active Water-eligible Condition: Dehydrated Current Severity to zero, removing nonpersistent zero. Resolve separate station Energy independently. Complete Condition removal discards attachments.

## AB. Aid

Marathon mile 8/16/24; half mile 6. Treat every eligible active Condition: Nausea/Gashed Knee Current Severity 0, Twisted Ankle −3, Heat Exhaustion −4, floor zero and remove nonpersistent zero. No single-target station choice; station Energy is separate.

## AC. Gut Checks

Marathon mile 10/18/23 thresholds 25/30/35; half mile 6/11 thresholds 9/11. Pause crossing, total printed Effort on cards still in hand plus Strength +1, Mental Toughness +3, Pace Band +2 if active. Played/slotted/attached cards do not count. Failure costs 2 Energy; cards are not consumed.

## AD. Course Difficulty

Starting side Difficulty is subtracted once from turn Effort. At each boundary use the change in Difficulty on positive carried remainder; installed modifiers, active weather, Conditions, and Event effects apply as specified. Finish extension has no Difficulty.

## AE. Course surfaces / terrain

Read visible side surface, route, setting, elevation, footing, and Difficulty; printed specialist effects apply only to their stated properties. Sore Feet adds 2 Difficulty on Concrete/Asphalt while effective. Rare Brick/Cobblestone/Sand have ordinary Movement counterplay and no new dedicated Effect in v1.4.

## AF. Finish

Course endpoint is 26.0/13.0, not Finish. A positive remaining legal quarter-mile Movement unit crosses the separate 0.2/0.1 extension. Stop immediately and lose unused Movement. Exactly reaching Course endpoint without positive remainder has not finished; Energy may be zero.

## AG. DNF

Only after Energy 0, Will spent, no meaningful legal hand or eligible-slot forward Movement, no legal self-recovery, cycling, reachable Water/Aid route, or successful final assistance path. A received card that can legally recover next turn prevents premature DNF. Mark explicit DNF, preserve position/resources/Conditions/reason, stop turns, assign no place.

## AH. Race end / placing

Finish the round, compare same-round finishers by printed Effort left in hand, then Energy, then unused Will; exact tie shares place. Race ends when every runner is FINISHED or DNF. Resolution seat order never breaks a tie.

## AI. Deck recycling

When a normal draw requires a card and draw pile is empty, shuffle eligible Race discard into draw. Hands, slots, attachments, and staged Event zones remain excluded. If draw and eligible discard both empty, skip; never fabricate or retrieve committed cards.

## AJ. Player-facing quick reference

Round Start choose Pace and form Packs; on your turn draw one if below six, optionally Treat/Prepare once, play up to two cards with normally one Movement, pay Energy/Will, resolve Course/stations/Gut Checks/Finish, End. Decide before installation whether the card can wait through two full turns. Keep attached cards committed until Condition removal.

## v1.3.2 → v1.4 rule change ledger

| Rule | Class | Practical change |
|---|---|---|
| Starting hand/maximum seven → six | MODIFIED RULE | Deal six; draw remains one below six; no minimum. |
| Direct Slot Movement | NEW RULE | Eligible installed Training/Gear may supply printed Effort after two complete runner turns. |
| Slot commitment/age reset | NEW RULE | Installation and replacement begin a two-turn clock. |
| Attached treatment cannot move; discards on complete Condition removal | CLARIFICATION | Attachment is separate from slot and hand, and remains through partial treatment. |
| DNF checks eligible/future slot recovery | MODIFIED RULE | No premature DNF when that path is viable. |
| Race deck recycling and zone exclusion | CLARIFICATION | Draw from eligible discard if draw empty; skip if both empty. |
| Fourteen physical card title edits | CLARIFICATION | Names only; no mechanical Effect change. |
| Nausea `Cannot use Fuel` text | CLARIFICATION | Printed wording changes; Fuel Effect blocked, Fuel Movement legal. |
| Gear category/footwear metadata | CLARIFICATION | `is_footwear` enforces existing one-shoe rule; broad category descriptive. |
| Course physical layout | CLARIFICATION | 13 two-mile cards out and back; simulation stores 26 one-mile lanes. |
| Four Paces, printed costs, Will, stations, Packs, Finish, assistance, targeted Event legality, three pre-race exchanges | UNCHANGED / REAFFIRMED | Prior frozen rules continue. |
| Course inventory and visibility | UNCHANGED / REAFFIRMED | No Course-side mechanics or title field changed. |

The full old/new title ledger is in **DRG-v1.4-Race-Card-Family-Lists.md**; implementation specifics and known open review items are in the report and Rules Review.
