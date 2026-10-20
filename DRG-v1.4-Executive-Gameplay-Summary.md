# v1.4 Executive Gameplay Summary

## What this document is

The front door to the candidate rules and the complete card and Course review.

## How to use it

Read this before the standalone Gameplay Rules List; follow the linked inventories for every physical card and Course side.

## Key takeaways

DRG is a race to the exact Finish. Six-card starts, one normal draw below six, two committed turns for slot liquidation, and committed Condition attachments create deliberate card-economy choices.

## The race in a minute

Four to twelve runners (six to eight preferred) race on a visible out-and-back Course. For a marathon, connect 13 physical two-mile Course cards long-side to long-side from the Start/Finish card at one end. Each card carries a one-mile outbound lane and an opposite one-mile return lane, each with four quarter-mile arrows/spaces. Runners start at Start, travel out along one side, turn, and return along the other to finish at the Start/Finish end. The 30-card inventory has 60 one-mile side records in simulation data; a side record is not a whole physical card. All lanes are visible for Pace, Training/Gear, treatment, station approach, slot retention, and sacrifice planning. Everyone chooses a Pace at Round Start, Packs form, then runners take sequential turns within the same race-time round. Replenish one normal card if below six, optionally use the **one Treat/Prepare opportunity**, then commit at most **two Race-card plays**; a new card installed or used for Fuel/treatment spends both Treat/Prepare and one card play, usually leaving one Movement play; normally one Movement card is mandatory. Printed Effort and Pace overcome current Course Difficulty and Conditions. Each Movement unit advances a quarter mile, up to two miles per normal turn. The first runner across the 26.2-mile marathon or 13.1-mile half marathon extension wins, subject to simultaneous same-round placement.

Energy pays Pace and each Movement card separately. Easy/Steady/Race/Push add 0/1/2/3 Effort and have base Energy costs 0/1/1/2. Effort 1–3 costs zero Movement Energy, 4–6 costs one, and 7+ costs two. Energy starts at 15, never passively regenerates; one Will per race can pay the exact otherwise-legal shortfall. Going to zero Energy is not itself DNF.

## Cards and the visible Course

Training supplies persistent or timed help in two slots; Gear equips into two normal slots, with at most one footwear. Install through Treat/Prepare **and one Race-card play**; Effects begin immediately. Broad Gear categories are descriptive; `is_footwear` alone enforces the one-equipped-shoe limit, and Running Socks do not count. After the installation turn and the following complete runner turn, an installed card may instead be sacrificed directly from its slot on the next turn: remove its Effect **before** computing Energy and Movement, pay its printed Movement cost, use its Effort as one of the two card plays, and discard. Hand+hand, hand+slot, and slot+slot are possible. The six-card hand is a maximum, not a refill target. Fuel Effect uses Treat/Prepare and one card play for Energy **or** printed remedy. Nausea prints `Cannot use Fuel`: active Nausea blocks the Fuel **Effect**, not legal Fuel **Movement**. Events use Movement-phase Effect or printed Effort, not both; targeted Effects require an eligible active other runner. Conditions arise automatically on draw and modify the runner while effective.

The entire Course is revealed before pre-race exchanges: 30 selectable two-mile physical cards, represented by 60 one-mile data lanes. Routes, surfaces, elevations, and Difficulty make installed specialists and Pace matter. There is no hidden routing choice or new Course Effect in v1.4. Fixed Water and Aid stations treat every eligible active Condition. Water resolves Dehydrated; Aid resolves Nausea, Gashed Knee, Twisted Ankle, and Heat Exhaustion as printed in the canonical rules. Energy at stations is separate. Gut Checks compare printed Effort still in hand with a threshold; failing costs two Energy.

## Other runners and survival

Same-Pace runners within 0.5 mile of a Pack leader may form a Pack at Round Start; membership locks for the round and saves one Pace Energy. A stranded runner may spend their one Treat/Prepare action requesting a one-for-one hand swap with any eligible active helper. It consumes no Race-card play and charges the helper no action debt. Simulation chooses leader/second place deterministically and evaluates legal rescue swaps; this is not a physical-game partner restriction. A card received immediately may support legal remaining Movement or next-turn preparation. DNF requires exhausting meaningful hand/eligible-slot Movement, Will, recovery, reachable stations, cycling, and final assistance. Finishers keep same-round tie-breaks; DNF runners receive no place.

## What changed and what is next

Starting hand maximum fell from seven to six; draw remains one, with eligible-discard recycling. Two-turn Direct Slot Movement and committed attachments now define card circulation. Fourteen physical card titles got running terminology edits, Nausea received a wording-only clarification, and Gear category metadata now agrees with established footwear legality; no printed values or card Effects changed. The full 108-card ledger, 60-side inventory, and Course coverage rationale are in the companion lists and matrix. The next **authorized** multi-seed evaluation should measure hand starvation, slot liquidity and commitment, attachment lock-up, Pace choices, DNF rescue, and performance by profile. This candidate has not run that study and draws no balance conclusion from an inventory or unit test alone.
