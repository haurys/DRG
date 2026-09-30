# Downtown Running Game — Canonical Playtest Rules

Status: **current designer-frozen playtest specification**, frozen Race Card redesign 2026-09-30. This Markdown remains the human-readable authority. The live race path in `engine/simulate.py` is synchronized for the integrated systems covered by bounded end-to-end tests; files under `output/` remain historical until the authorized single deterministic marathon audit. See [Rules Review](DRG-Rules-Review.md) for unresolved non-blocking physical-game questions and documented simulator policies.

## Authority and vocabulary

The `RaceCards.docx` frozen table and [Race Card Simulation Effect Definitions](DRG-Race-Card-Simulation-Effect-Definitions.md) govern the 108 Race cards. The semantic definitions resolve ambiguous table rendering and earlier card rules. The current Course, Pack, Will, Pace, Finish, turn structure, and Gut Check rules below govern play, including the later designer consolidation. Earlier conflicting mechanics are [superseded](DRG-Superseded-Rules.md). **FROZEN** denotes a current playtest rule; **RULES REVIEW** is unresolved and is not silently made canonical.

Icons: Movement `→` (U+2192); Easy `▷`, Steady `▶`, Race `▶▶`, Push `▶▶▶`; Energy `⚡`. Movement and Pace symbols are distinct.

## Game and physical course

Race formats: marathon 26.2 miles; half marathon 13.1 miles. Primary diagnostic: eight runners; broad intended range 3–20. Course movement uses quarter-mile spaces; a separate Finish extension supplies 0.2 or 0.1 mile. The visible, randomized Course consists of 4 × 6-inch reversible two-mile cards, two one-mile sides, each with four quarter-mile positions. See [Course Rules](DRG-Course-Rules.md) for construction, inventory reference, boundaries, milestones, Finish, and surface taxonomy. Race cards are 2.5 × 3.5-inch portrait cards. Their family colors and icon direction appear in [Race Cards](DRG-Race-Cards.md).

## Simultaneous round — FROZEN

A round represents the **same race-time interval** for all runners; sequential resolution is administrative, not earlier race time. Track `round_start_position`, `current_resolution_position`, and `round_end_position`. Unless an explicit effect overrides it, same-round timing, eligibility, and Finish outcomes are simultaneous.

1. **Round Start:** activate staged Global effects; all runners select Pace simultaneously; form eligible Packs from the established Pace and Round Start positions; snapshot position, Pace, Pack, and other public simultaneous state. Pace locks for the round.
2. **Each runner, sequentially:** Replenish → Treat/Prepare → Movement → End.
3. **Round End:** record Pack cohesion without changing round membership; resolve simultaneous Finish places; expire Global/round effects; cleanup.

## Hand, draw, and card budget — FROZEN

Starting hand: seven non-Condition cards. Hand limit: seven. In Replenish, draw toward seven but at most **two normal Race cards**. A Condition is revealed and placed immediately, does not enter hand or count toward that two-card draw, and prompts replacement drawing until the required normal draws are complete. It is active that turn. No generic End-turn Draw 1. At most **two cards played** per runner-turn; normally at least one must be committed to mandatory Movement. Normal structures: two Movement; one Treat/Prepare plus one Movement; or one Movement. Two Treat/Prepare and zero Movement, or zero cards, require an explicit override. A Treat/Prepare card adds zero Movement Effort. Relocating already-played Gear occupies the sole Treat/Prepare action for that turn but does not play a new Race card; the remaining card-play allowance may be used normally for Movement. No second Treat/Prepare action is allowed that turn. If no payable Movement/Effect card and no legal Treat/Prepare path exists after Will is unavailable, the simulator records the forced zero-card fallback; it creates no new gameplay action.

## Family use — FROZEN

Every non-Condition card is used in exactly one mode. **MOVEMENT:** use printed Effort, pay the printed Effort-band Movement Energy cost per card, and ignore its Effect. **EFFECT:** resolve the Effect, use no printed Effort, and pay no Movement-card Energy cost. Training/Gear/Fuel Effects resolve in Treat/Prepare; Event Effects resolve in Movement at their stated timing and still count as one of the two plays and the one-Event limit. Conditions print Severity, automatically enter play on draw, and cannot be played for Movement. Installed Training/Gear can instead be used as Movement cards only before installation; one physical card performs one role.

The deck has 108 physical cards: 20 Training, 20 Gear, 22 Fuel, 30 Event, 16 Condition. Running Jacket takes the second Hydration Belt slot; Cold Snap replaces EV-010 Congestion; Cold Chills takes the second Dehydrated slot; Gashed Knee replaces Stomach Trouble. See [Training](DRG-Training.md), [Gear](DRG-Gear.md), [Fuel](DRG-Fuel.md), [Events](DRG-Events.md), and [Conditions](DRG-Conditions.md).

## Pace, Energy, and Will — FROZEN

| Pace | Effort modifier | Base Pace Energy cost |
|---|---:|---:|
| Easy | +0 | 0 |
| Steady | +1 | 1 |
| Race | +2 | 1 |
| Push | +3 | 2 |

Starting and maximum Energy: **15**. Energy persists; Effort is immediate movement-performance input. No generic Energy-to-Movement conversion. Movement cards have the separate printed Energy cost listed below. Final Pace cost = base cost + mandatory additional costs − applicable preservation, floored at zero. Determine and pay the full legal turn cost before resolving Movement; event gains during/after Movement cannot finance it. Each runner starts with one Will, usable once per race. Calculate the otherwise-legal turn's total payable Pace and Movement-card Energy after Pack, Training, Gear, Condition, and other applicable cost reductions/preservation. Spend stored Energy first. If insufficient, Will covers the **exact remaining shortfall**, whether Pace, one or more Movement cards, or both; mark Will spent. Will does not add stored Energy or grant Effort, Movement, Difficulty relief, a higher legal Pace, Pack membership, Condition treatment, or Gut Check benefit. Without Will, an unaffordable Pace steps down to a legal affordable Pace; an unaffordable Movement card remains illegal. Energy stays within 0–15 and a runner may finish at 0.

## Effort, Movement, and Course — FROZEN

| Printed Effort | Energy paid for MOVEMENT use |
|---:|---:|
| 1–3 | 0 |
| 4–6 | 1 ⚡ |
| 7+ | 2 ⚡⚡ |

Two Movement cards each pay their cost independently after Pace payment; EFFECT use pays no card Movement cost. A Movement card is payable if stored Energy plus an available Will can cover its cost after Pace and other legal reductions. Pace preservation applies to Pace cost, not a card’s printed Movement cost. Will pays only the resulting exact shortfall and does not replenish the track.


**1 Movement = 0.25 mile.** Direct +1/−1 Movement adds/removes one quarter-mile after converting Effort. Approximately 2 Effort per Movement is a **design-valuation heuristic only**, never a gameplay conversion. Sum printed Effort from the one or two Movement cards (Treat/Prepare contributes zero); apply Effort modifiers; add Pace modifier; subtract starting Course Difficulty once; apply Condition/Effort penalties; convert final integer result through Movement Model A; apply direct signed Movement; floor at zero and cap at two miles unless an explicit override; traverse Course and resolve boundaries/milestones. Positive direct Movement can make a base-zero result advance 0.25 mile. Normal final turn movement never exceeds 2 miles. Porta-Potty Effect is −1 direct Movement and +2 Energy after Movement; the ordinary two-mile cap remains.

| Calculated Effort result | Base miles |
|---|---:|
| ≤0 | 0 |
| 1–2 | 0.25 |
| 3–4 | 0.50 |
| 5–6 | 0.75 |
| 7–8 | 1.00 |
| 9–10 | 1.25 |
| 11–12 | 1.50 |
| 13–14 | 1.75 |
| ≥15 | 2.00 |

At each one-mile boundary, stop, debit **2 integer Movement Result per completed quarter-mile**, and carry only positive remainder. Difficulty change = new Difficulty − previous Difficulty. Adjusted remainder = remainder − Difficulty change; do not charge full new Difficulty again. A nonpositive adjusted remainder stops at the boundary. Easier terrain does not create movement if there was no positive remainder on arrival. Repeat across multiple boundaries without resetting Effort or the two-mile turn cap. Direct Movement enters available movement before traversal and uses the same boundary system. The exact representation of direct Movement in the carried integer remainder is [RULES REVIEW](DRG-Rules-Review.md) where the two accounting methods would differ.

## Events and targeting — FROZEN

Events may be played only during Movement. Their MOVEMENT mode uses printed Effort and ignores Effect; their EFFECT mode resolves Effect and contributes no printed Effort. No more than one Event. Timing categories: `CURRENT_MOVEMENT`, `AFTER_MOVEMENT`, `NEXT_ROUND_STAGED`, `COURSE`, `GLOBAL`. Staged/Course/Global cards remain in their appropriate area until resolution/expiration, then discard. Targets include SELF, OTHER, COURSE, GLOBAL, and beneficial interaction. **OTHER Target Lock:** choose one eligible opponent; an opponent already targeted by a staged/active OTHER Event cannot receive a second OTHER Event until the first resolves/expires. SELF, COURSE, GLOBAL, and non-OTHER beneficial interactions do not acquire that lock merely by mentioning a runner. The full 30-slot current Event inventory is [here](DRG-Events.md).

## Conditions, Training, Gear, Fuel — FROZEN

Condition state has immutable Base Severity, permanently treated Current Severity, and Effective Severity after temporary suppression (minimum zero). All penalties/restrictions apply only when Effective Severity is positive. Hot Spot, Side Stitch, and Dead Legs subtract 1 direct Movement at Race/Push while active; Gashed Knee subtracts 1 direct Movement unconditionally; Sore Feet adds 2 Difficulty on Concrete/Asphalt while active. Named remedies set Current Severity to zero; Aid remedies Nausea/Gashed Knee and reduces Twisted Ankle Severity by 3 or Heat Exhaustion by 4. Nonpersistent Conditions at zero discard; persistent ones remain managed. Gear suppression changes only Effective Severity and rebounds when removed. Anti-Chafe prevents only a new Hot Spot.

Training has two slots. Persistent remains until replaced; Temporary(N) occupies a slot for N runner turns, with installation turn = Turn 1 and legal same-turn benefit. Replacing uses Treat/Prepare. Training never attaches. Gear has two normal Equipped slots, at most one Equipped Footwear, and compatible attachments outside normal slots, one job per physical card and normally one attached Gear per Condition. Moving existing Gear between equipped/attached consumes a Treat/Prepare action, not a new card play. Temporary Gear counts installation turn as Turn 1; removed suppression rebounds. Fuel returns to eligible discard after Effect use and provides either +2 Energy or its printed remedy/Severity branch, never both. Active Nausea prohibits Fuel Effect use. Training Condition reductions occur once on installation to one eligible active Condition, and on later acquisition under the existing stacking rule. Hydration Belt gains +1 Energy at each applicable Water opportunity, not each runner-turn. Hot Spell and Cold Snap stage a one-round 1-Energy loss for the playing runner; matching equipped weather protection prevents that loss, and Pack preservation does not affect it. Helpful Runner gives another Runner +1 Energy without transferring the card. Detailed per-card entries are in the linked family files.

## Pack — FROZEN

At Round Start after Pace selection, runners with the same Pace may form a Pack only within 0.5 mile of its leader, measured directly without chaining. If multiple legal Packs are available, choose the nearest leader; an exact distance tie uses stable leader runner ID. A Pack requires at least two runners; equal-position leaders are co-leaders. Membership is fixed for that round, with no separate mid-round voluntary exit; eligibility and membership are reevaluated at the next Round Start. Round End cohesion is observational. Pack preserves **1 Pace Energy**, stacking with Training/Gear preservation to a floor of zero. A runner may voluntarily stop at a legal quarter-mile position to preserve future cohesion; unused movement is lost. No timer, anchor, cooldown, size cap, or breakaway penalty. Zero-cost Steady/Race/Push and preservation stacking are **BALANCE WATCH**, not defects.

## Gut Checks and milestones — FROZEN

At a crossed Gut Check, pause traversal and total printed Effort on all Race cards remaining in hand, plus active Strength +1, Mental Toughness +3, and Pace Band +2. Committed cards do not count; empty hand is zero; no card is consumed. Pass at or above the threshold; failure costs 2 Energy. Resume legal remaining Movement. Marathon PLAYTEST thresholds: mile 10/18/23 = 25/30/35. Half thresholds remain mile 6/11 = 9/11.

## Pre-race and Finish — FROZEN

Construct and reveal Course before trading. A one-for-one trade costs one move for each participant; giving and receiving are not charged separately. Each runner has three total moves/exchanges. A Deck Exchange costs one move. Acquired cards remain locked under the existing rule. Mulligan 3 is superseded.

Finish threshold is 26.2 or 13.1 miles; Course ends at 26.0 or 13.0. Finish has no Difficulty. A runner reaching exactly the Course endpoint with no positive legal Movement left has not finished. One positive legal quarter-mile Movement unit after the endpoint crosses the 0.2-mile Marathon or 0.1-mile Half Marathon extension, which has no Difficulty; stop immediately and lose unused movement. Finish the entire round before assigning simultaneous same-round placement: compare (1) sum of printed Effort in remaining hand after finishing turn, (2) remaining Energy, (3) unspent Will, then (4) share place. Movement-used cards are absent from hand; Conditions contribute no Effort. Seat order is not a tiebreak.

## Audit and playtest controls

Seed all Course selection/orientation, shuffles, draws, and deterministic policy tie-breaks; log hands privately for designer audit but never expose opponents' concealed cards or future draws to virtual runners. Record the Round Start snapshot, every Replenish/Condition chain, two-card budget, installed/attached states, selected Pace and cost/preservation/Will, plays and mandatory Event effects, target locks, movement conversion/direct modifiers/boundary remainder, milestones, Energy/waste, Pack cohesion, Finish comparison, and decision options/rationale. Track Event activation/play rate, direct Movement, Tough Decision replacements/Condition exposure, preservation stacking, and hand congestion. A competitive marathon around 25–35 rounds (center ~30), average ~0.85–1.0 miles per turn, and exceptional two-mile turns are **BALANCE WATCH targets**, not executable rules. No balance change follows from this documentation pass.

## Approved test-baseline preparation changes

Two active Training slots and two normal Equipped Gear slots apply. A third installation replaces one chosen card to eligible discard; compatible attached Gear occupies no normal Gear slot. Fuel Treat/Prepare recovery is +2 for every Fuel card. Electrolytes chooses exactly one of +2 Energy or Remedy Dehydrated; Salt Tabs chooses exactly one of +2 Energy or Remedy Cramp. Energy is legal without the named Condition; remedy is legal only while that Condition is active. Banana and Water Bottle choose +2 Energy or Severity −2 to their named Condition. Installed Training resistance reduces starting Current Severity when a matching Condition is acquired; installation also reduces one eligible active Condition once. Distinct acquisition reductions stack and floor at zero. See the family inventories.

## AI Victory Directive — approved simulator policy

The virtual runner's primary objective is to finish ahead of all opponents in the fewest practical turns. Legal Pace and complete-turn plans are compared by expected forward progress, estimated remaining turns, competitive position, and sustainable Energy. Training, Gear, Fuel, Condition relief, Packs, and card retention serve that objective. Resource efficiency alone does not justify delaying progress. Will is a payment resource for the fastest sustainable finishing line, not a reserve to protect for its own sake; it may be exhausted at the Finish. Setup/replacement considers immediate Movement opportunity cost, the displaced installed card, and a remaining-distance-discounted future benefit. A zero-Movement plan is strongly disfavored when legal forward progress is available, except for material survival or severe Condition relief. Profile style has secondary precedence and cannot override the Victory Directive. See [Simulation Decision Rules](simulation/Simulation-Decision-Rules.md) for deterministic AI scoring and information limits. The scorer uses the frozen printed Movement Energy costs and compares effect-mode plans against paid Movement alternatives.
