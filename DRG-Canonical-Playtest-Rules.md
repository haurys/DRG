# Downtown Running Game — Canonical Playtest Rules

Status: **current designer-frozen playtest specification**, 2026-09-25. This Markdown remains the human-readable authority. The live race path in `engine/simulate.py` is synchronized for the integrated systems covered by bounded end-to-end tests; files under `output/` remain historical until the authorized single deterministic marathon audit. See [Rules Review](DRG-Rules-Review.md) for unresolved non-blocking physical-game questions and documented simulator policies.

## Authority and vocabulary

Precedence: (1) current designer decisions in the 2026-09-25 consolidation prompt and the immediately preceding integrated/supplemental freezes; (2) most recent explicit DRG designer decision; (3) Simulation Foundation; (4) `CARDS.docx`; (5) Course-description Markdown; (6) Phase 2A audit; (7) prototype artwork; (8) exploratory discussions. Earlier conflicting rules are [SUPERSEDED](DRG-Superseded-Rules.md). **FROZEN** means the current playtest rule, not an invitation to rebalance; **PLAYTEST VALUE** means configurable numeric trial value; **BALANCE WATCH** means observe, not change; **RULES REVIEW** means no authoritative answer. Do not substitute zero for unknown data.

Source set inspected: 2026-09-25 current designer prompts; the existing `DRG-Simulation` rules/data/simulation/engine/tests and Phase 2A audit; `CARDS.docx` (Library upload 2026-08-28); `DRG_Initial_Course_Deck_Graphic_Descriptions(1).md` (2026-08-28); prototype card artwork. Per-card physical IDs and older printed values came from `data/race_cards.json` and `CARDS.docx` only where compatible with the newer freezes. This is a **documentation pass**: no source JSON, engine, test, or simulation output has been altered.

## Game and physical course

Race formats: marathon 26.2 miles; half marathon 13.1 miles. Primary diagnostic: eight runners; broad intended range 3–20. Course movement uses quarter-mile spaces; a separate Finish extension supplies 0.2 or 0.1 mile. The visible, randomized Course consists of 4 × 6-inch reversible two-mile cards, two one-mile sides, each with four quarter-mile positions. See [Course Rules](DRG-Course-Rules.md) for construction, inventory reference, boundaries, milestones, Finish, and surface taxonomy. Race cards are 2.5 × 3.5-inch portrait cards. Their family colors and icon direction appear in [Race Cards](DRG-Race-Cards.md).

## Simultaneous round — FROZEN

A round represents the **same race-time interval** for all runners; sequential resolution is administrative, not earlier race time. Track `round_start_position`, `current_resolution_position`, and `round_end_position`. Unless an explicit effect overrides it, same-round timing, eligibility, and Finish outcomes are simultaneous.

1. **Round Start:** activate staged Global effects; all runners select Pace simultaneously; all make voluntary Pack decisions using Round Start state; snapshot position, Pace, Pack, and other public simultaneous state. Pace locks for the round.
2. **Each runner, sequentially:** Replenish → Treat/Prepare → Movement → End.
3. **Round End:** recalculate Pack cohesion; resolve simultaneous Finish places; expire Global/round effects; cleanup.

## Hand, draw, and card budget — FROZEN

Starting hand: seven non-Condition cards. Hand limit: seven. In Replenish, draw toward seven but at most **two normal Race cards**. A Condition is revealed and placed immediately, does not enter hand or count toward that two-card draw, and prompts replacement drawing until the required normal draws are complete. It is active that turn. No generic End-turn Draw 1. At most **two cards played** per runner-turn; normally at least one must be committed to mandatory Movement. Normal structures: two Movement; one Treat/Prepare plus one Movement; or one Movement. Two Treat/Prepare and zero Movement, or zero cards, require an explicit override. A Treat/Prepare card adds zero Movement Effort. An already-played Gear relocation uses a Treat/Prepare action but is **not a new card play**; interaction with the two-card budget is [RULES REVIEW](DRG-Rules-Review.md).

## Family use — FROZEN

| Family | Movement | Treat/Prepare | Resolution |
|---|---|---|---|
| Training | Printed Effort only | Install/use | Persistent or Temporary(N) as listed; two Training slots. |
| Gear | Printed Effort only | Equip/attach/use | Two Equipped slots, one Equipped Footwear; attached Gear occupies no normal slot and performs one role. |
| Fuel | Printed Effort only | Use for Energy/remedy; discard normally | Consumable; no double-dipping. |
| Event | Printed Effort **and mandatory Effect**, if any | **Forbidden** | At most one Event per turn, included in two-card play limit. |
| Condition | Not voluntarily played | Managed/treated | Automatically enters play on draw, with replacement draw. |

Drawing, holding, or discarding an unplayed Event never activates its Effect. A played Event without an Effect (Perfect Rhythm) is legal. See [Training](DRG-Training.md), [Gear](DRG-Gear.md), [Fuel](DRG-Fuel.md), [Events](DRG-Events.md), and [Conditions](DRG-Conditions.md).

## Pace, Energy, and Will — FROZEN

| Pace | Effort modifier | Base Pace Energy cost |
|---|---:|---:|
| Easy | +0 | 0 |
| Steady | +1 | 1 |
| Race | +2 | 1 |
| Push | +3 | 2 |

Starting and maximum Energy: **15**. Energy persists; Effort is immediate movement-performance input. No generic Energy-to-Movement conversion or Energy-per-card cost. Final Pace cost = base cost + mandatory additional costs − applicable preservation, floored at zero. Pay **before Movement**. Event Energy gained during/after Movement cannot retroactively finance that payment. If unable to pay, the runner may spend its one Will token, pay all remaining Energy (possibly to zero), and use the selected otherwise-legal Pace as fully paid. Without Will, step down to an affordable legal Pace. Apply preservation before testing affordability. Will adds no Energy/Effort/Movement, does not raise the cap, treat Conditions, override maximum-Pace restrictions, negate Difficulty, grant Pack, activate cards, or affect Gut Checks. Gains over 15 are wasted; Energy cannot fall below zero.

## Effort, Movement, and Course — FROZEN

**1 Movement = 0.25 mile.** Direct +1/−1 Movement adds/removes one quarter-mile after converting Effort. Approximately 2 Effort per Movement is a **design-valuation heuristic only**, never a gameplay conversion. Sum printed Effort from the one or two Movement cards (Treat/Prepare contributes zero); apply Effort modifiers; add Pace modifier; subtract starting Course Difficulty once; apply Condition/Effort penalties; convert final integer result through Movement Model A; apply direct signed Movement; floor at zero and cap at two miles unless an explicit override; traverse Course and resolve boundaries/milestones. Positive direct Movement can make a base-zero result advance 0.25 mile. Normal final turn movement never exceeds 2 miles. Porta-Potty imposes its separate **0.5-mile PLAYTEST VALUE** cap.

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

Events may be played only during Movement: printed Effort contributes and Effect is mandatory if present. No more than one Event. Timing categories: `CURRENT_MOVEMENT`, `AFTER_MOVEMENT`, `NEXT_ROUND_STAGED`, `COURSE`, `GLOBAL`. Staged/Course/Global cards remain in their appropriate area until resolution/expiration, then discard. Targets include SELF, OTHER, COURSE, GLOBAL, and beneficial interaction. **OTHER Target Lock:** choose one eligible opponent; an opponent already targeted by a staged/active OTHER Event cannot receive a second OTHER Event until the first resolves/expires. SELF, COURSE, GLOBAL, and non-OTHER beneficial interactions do not acquire that lock merely by mentioning a runner. The full 30-slot current Event inventory is [here](DRG-Events.md).

## Conditions, Training, Gear, Fuel — FROZEN

Condition state has immutable Base Severity, permanently treated Current Severity, and Effective Severity after temporary suppression (minimum zero). All penalties/restrictions apply only when Effective Severity is positive. Hot Spot, Side Stitch, and Dead Legs subtract Effective Severity Effort at Race/Push; Sore Feet adds Effective Severity Difficulty on Concrete/Asphalt. Named remedies set Current Severity to zero; Aid removes Twisted Ankle. Nonpersistent Conditions at zero discard; persistent ones remain managed. Gear suppression changes only Effective Severity and rebounds when removed. Anti-Chafe prevents only a new Hot Spot.

Training has two slots. Persistent remains until replaced; Temporary(N) occupies a slot for N runner turns, with installation turn = Turn 1 and legal same-turn benefit. Replacing uses Treat/Prepare. Training never attaches. Gear has two normal Equipped slots, at most one Equipped Footwear, and compatible attachments outside normal slots, one job per physical card and normally one attached Gear per Condition. Moving existing Gear between equipped/attached consumes a Treat/Prepare action, not a new card play. Temporary Gear counts installation turn as Turn 1; removed suppression rebounds. Fuel returns to eligible discard after use and gives either Movement Effort or Treat/Prepare Energy/remedy, never both. Detailed per-card entries are in the linked family files.

## Pack — FROZEN

Pack membership is voluntary: at least two consenting runners, same Pace, each no more than 0.5 mile behind the farthest participating runner (leader), measured directly, no chaining. Equal-position leaders are co-leaders; multiple Packs may exist. Pack preserves **1 Pace Energy**, including when stacking with Training/Gear preservation; cost cannot go below zero. Pack decisions use the Round Start snapshot. Mid-round separation does not dissolve a Pack immediately. At Round End remove members more than 0.5 mile behind the leader and dissolve groups below two. A runner may voluntarily stop at a legal quarter-mile position to preserve cohesion; unused movement is lost. No timer, anchor, cooldown, size cap, or breakaway penalty. Zero-cost Steady/Race/Push and preservation stacking are **BALANCE WATCH**, not defects.

## Gut Checks and milestones — FROZEN

At a crossed Gut Check, pause traversal and total printed Effort on all Race cards remaining in hand, plus active Strength +1, Mental Toughness +2, and Pace Band +1. Committed cards do not count; empty hand is zero; no card is consumed. Pass at or above the threshold; failure costs 2 Energy. Resume legal remaining Movement. Marathon PLAYTEST thresholds: mile 10/18/23 = 25/30/35. Half thresholds remain mile 6/11 = 9/11.

## Pre-race and Finish — FROZEN

Construct and reveal Course before trading. A one-for-one trade costs one move for each participant; giving and receiving are not charged separately. Each runner has three total moves/exchanges. A Deck Exchange costs one move. Acquired cards remain locked under the existing rule. Mulligan 3 is superseded.

Finish threshold is 26.2 or 13.1 miles; Course ends at 26.0 or 13.0. Finish has no Difficulty. Any positive legal movement sufficient for the remaining Finish extension finishes; stop immediately and lose unused movement. Finish the entire round before assigning simultaneous same-round placement: compare (1) sum of printed Effort in remaining hand after finishing turn, (2) remaining Energy, (3) unspent Will, then (4) share place. Movement-used cards are absent from hand; Conditions contribute no Effort. Seat order is not a tiebreak.

## Audit and playtest controls

Seed all Course selection/orientation, shuffles, draws, and deterministic policy tie-breaks; log hands privately for designer audit but never expose opponents' concealed cards or future draws to virtual runners. Record the Round Start snapshot, every Replenish/Condition chain, two-card budget, installed/attached states, selected Pace and cost/preservation/Will, plays and mandatory Event effects, target locks, movement conversion/direct modifiers/boundary remainder, milestones, Energy/waste, Pack cohesion, Finish comparison, and decision options/rationale. Track Event activation/play rate, direct Movement, Tough Decision replacements/Condition exposure, preservation stacking, and hand congestion. A competitive marathon around 25–35 rounds (center ~30), average ~0.85–1.0 miles per turn, and exceptional two-mile turns are **BALANCE WATCH targets**, not executable rules. No balance change follows from this documentation pass.

## Approved test-baseline preparation changes

Two active Training slots and two normal Equipped Gear slots apply. A third installation replaces one chosen card to eligible discard; compatible attached Gear occupies no normal Gear slot. Fuel Treat/Prepare recovery is +1 for every Fuel design, with Electrolytes and Salt Tabs choosing either +1 Energy or their named remedy. Installed Training resistance reduces starting Current Severity only when a matching Condition is acquired; distinct reductions stack and floor at zero. See the family inventories.

## AI Victory Directive — approved simulator policy

The virtual runner's primary objective is to finish ahead of all opponents in the fewest practical turns. Legal Pace and complete-turn plans are compared by expected forward progress, estimated remaining turns, competitive position, and sustainable Energy. Training, Gear, Fuel, Condition relief, Packs, and card retention serve that objective. Resource efficiency alone does not justify delaying progress. Setup/replacement considers immediate Movement opportunity cost, the displaced installed card, and a remaining-distance-discounted future benefit. A zero-Movement plan is strongly disfavored when legal forward progress is available, except for material survival or severe Condition relief. Profile style has secondary precedence and cannot override the Victory Directive. See [Simulation Decision Rules](simulation/Simulation-Decision-Rules.md) for deterministic AI scoring and information limits. This policy does not alter any physical game value or rule.
