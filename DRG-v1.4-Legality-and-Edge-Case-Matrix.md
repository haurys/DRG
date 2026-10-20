# v1.4 Legality and Edge Case Matrix

## What this document is

Short rulings for resource and timing boundaries.

## How to use it

Look up a “What happens if…” row, then consult the standalone rules for the full sequencing.

## Key takeaways

The mode, zone, action, and Energy checks are separate; DNF is evaluated after viable recovery routes.

| What happens if… | Legal? | What happens? | Why? |
|---|---|---|---|
| Hand = 0 | Yes | Replenish one normal card if available, otherwise consider eligible slot, future draw, legal recovery or assistance. | No minimum and no synthetic refill. |
| Hand = 1 | Yes | Draw one if below six; one or two legal cards may be committed. | Six is maximum, not a target reached in one turn. |
| Draw pile empty | Yes | Shuffle eligible discard for the required normal draw. | Exclude all occupied and staged zones. |
| Draw and eligible discard empty | Yes | Skip required draw; no card appears. | Committed cards remain committed. |
| Newly installed slot | Install yes; sacrifice no | Effect starts now; first slot Movement eligibility is installation turn +2. | Two complete runner turns must elapse. |
| One-turn-old slot | Sacrifice no | Keep Effect or replace/discard it legally. | Turn 11 after turn 10 installation is still committed. |
| Eligible two-turn slot | Yes | Remove Effect first; pay printed Movement Energy; use printed Effort and discard. | Turn 12 after turn 10 installation is first eligible turn. |
| Hand + slot / slot + slot | Yes if eligible/payable | Each Movement card consumes one of two plays. | Source does not change card budget. |
| Sacrificed slot suppresses a Condition | Yes, recalculate | Suppression ends immediately; active penalty can apply to this very Movement. | Cannot take both Effect and Effort from same slot card. |
| Zero Energy, Will unused | Sometimes | Will covers exact affordable-to-Will shortfall of an otherwise-legal plan; zero-cost Movement may work without it. | Will is payment, not regeneration. |
| Zero Energy, Will spent | Sometimes | Try zero-cost hand/slot Movement, legal recovery, future draw, reachable station and rescue before DNF. | Zero plus spent Will alone is insufficient. |
| Nausea + Fuel | Movement yes; Fuel Effect no | A Fuel card such as Effort-3 Energy Gel can move at zero Energy. | Nausea restricts Effect mode only. |
| Gear attached to a Condition | No Movement/trade | It stays committed through partial treatment or persistent zero. | Attachment is not a slot or hand card. |
| Water removes treated Condition | Yes | Resolve all Water Conditions; when complete removal occurs, discard attachments. | No return to hand/slot. |
| Aid removes treated Condition | Yes | Resolve all Aid-eligible Conditions; complete removal discards attachments. | No single-Condition selection. |
| Event needs another runner; none active | Effect no; Movement maybe | Filter Effect from legal plans; Movement remains if otherwise legal. | Finished/DNF runners are not targets. |
| Exactly one other active runner | Effect yes if otherwise legal | That active runner is the eligible target, subject to the Effect’s lock/other rules. | Target must be another active participant. |
| Every other runner FINISHED / DNF / mixed | Effect no; Movement maybe | No target-required Effect candidate survives. | Neither state is ACTIVE. |
| Pack position changes mid-round | Existing membership stays | Observe at Round End; re-form from next Round Start snapshot. | No mid-round breakaway recalculation. |
| Exactly marathon mile 26.0 or half mile 13.0 | Not finished yet | Need positive legal remaining quarter-mile Movement to cross the 0.2/0.1 extension. | Endpoint is before Finish. |
| Reachable station at zero Energy | No premature DNF | Evaluate viable approach using affordable Movement/recovery, then station treatment. | Practical continuation precedes DNF. |
| Eligible slot before DNF | No premature DNF | Count its legal forward Movement, with current Condition and payment after Effect ends. | Installed Effort can be the only path. |
| Assistance available | Yes if rescue-capable | Spend requester’s Treat/Prepare, swap one-for-one; helper has no debt. | Next-turn recovery can suffice to prevent DNF. |
| Finish with zero Energy | Yes | Cross with legal paid Movement or Will; zero stored Energy is permitted. | No positive final Energy requirement. |
| Two-card budget exhausted | No extra play | A slot sacrifice and Event each count one; assistance is budget-free but consumes Treat/Prepare. | No third card; no extra Treat/Prepare after swap. |
| Replaced Gear / Training | Yes to replacement | Old card discards, new one is installed and age resets. | No free hand retrieval. |
| Persistent Condition at zero | Yes, remains | Keep its attached card committed until actual complete Condition removal. | Severity zero and removal are distinct. |

| Install Training then Movement | Yes | New Training consumes Treat/Prepare and card play 1; one remaining legal Movement card may be played. | An installation has a real turn cost and no Movement Effort. |
| Equip Gear then Movement | Yes | New Gear consumes Treat/Prepare and card play 1; one remains for Movement. | Equipping is a new-card Effect use. |
| Treat/remedy Condition then Movement | Yes if treatment legal | New treatment card consumes Treat/Prepare and card play 1; the remaining play may move. | The same card cannot treat and provide printed Effort. |
| Fuel Effect then Movement | Yes without active Nausea | Fuel Effect consumes Treat/Prepare and card play 1; one remaining play may move. | Effect mode adds no printed Effort. |
| Assistance then Movement | Yes if rescue and Movement legal | Requester spends Treat/Prepare, zero card plays; received card enters hand now and may use remaining legal card plays. | No helper action debt or extra Treat/Prepare. |
| Relocation then Movement | Yes if relocation legal | Treat/Prepare spent, zero new plays; up to two legal Movement cards remain. | Already-played Gear is moved, not played again. |
| Slot sacrifice after installation delay | Yes on install turn +2 | One card play, zero Treat/Prepare; installed Effect terminates first. | Two complete runner turns of continuous installation are required. |
| Nausea + Fuel Effect | No while effective | `Cannot use Fuel` forbids the printed Fuel Effect, including +2 Energy or remedy. | No blanket Fuel-card prohibition. |
| Nausea + Fuel Movement | Yes if otherwise legal | FU-001 Effort 3 costs zero Movement Energy; it may advance legally. | Fuel in Movement mode ignores the Fuel Effect. |
| One footwear Gear already equipped | Second shoe needs replacement | Road Trainers, Cushion Trainers, Trail Shoes, Tempo Trainers and Carbon Racers use `is_footwear`; replace the old shoe. | Only one equipped footwear card, regardless of broad category. |
| Running Socks with a shoe | Socks are not second footwear | Socks may attach to Blister under treatment rules and do not consume the footwear limit. | `is_footwear` is false for Running Socks. |
| Two shoe-type Gear cards simultaneously | No | A new shoe replaces the current shoe if otherwise legal; two cannot coexist. | One-footwear restriction, not an apparel/accessory restriction. |
| Outbound/return boundary | Yes, same physical row | After mile 13 on a marathon, turn onto the opposite lane of physical position 13 for mile 14; then travel back toward Start/Finish. | Each selected physical card contributes an outbound and return mile; side data are one-mile records. |

A legal option still needs all other normal checks: active status, timing, card budget, affordability, target lock, and current Course. The matrix does not grant an otherwise illegal extra action.
