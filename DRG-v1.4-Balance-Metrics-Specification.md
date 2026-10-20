# v1.4 Balance Metrics Specification

## What this document is

The measurement contract to use **before** any later authorized multi-seed study.

## How to use it

Collect per runner-turn events and final summaries, stratify by format, player count, profile and seed, then inspect distributions and causal traces. Do not infer an outcome from these proposed metrics.

## Key takeaways

Hand depletion, slot timing and attachment lock-up are the new v1.4 questions; rules fidelity and deterministic replay are prerequisites to balance interpretation.

## Race length

| Metric | Capture | What it tells us |
|---|---|---|
| Rounds | Round End count until all finish/DNF | Very long races may expose resource deadlock; compare by format and roster size. |
| Active turns | Turns actually taken by participating runners | Separates long race length from runner inactivity. |
| First/last finisher and spread | First and last finish round and position/order difference | Large spread may indicate pacing disparity; include DNFs separately. |

## Completion

| Metric | Capture | What it tells us |
|---|---|---|
| Finishers/DNFs | Counts and percentage per seed/profile | High DNF rate warrants card-economy and legal-path inspection. |
| DNF reasons | Reason, state, hand/slot/Will, attempted recovery | A DNF with a viable slot or station route signals implementation error. |

## Movement

| Metric | Capture | What it tells us |
|---|---|---|
| Average Movement | Quarter-miles per active turn, by phase/profile | Compare sustained progress, not only peak turns. |
| Zero-Movement turns | Count and cause, including recovery/forced fallback | Persistent zero turns may reveal hand shortage or AI errors. |
| Movement source | Hand+hand, hand+slot, slot+slot, single source and Event mode | Shows whether delayed Effort is useful. |

## Energy

| Metric | Capture | What it tells us |
|---|---|---|
| Spent/gained | Pace/card/Condition/Gut costs; Fuel/station/Event/installed gains separately | Distinguish sustainable pace from emergency Will. |
| Exhaustion/final Energy | Turns at zero and Finish/DNF resources | Ending on zero can be strategically sound, not an automatic defect. |

## Hand economy

| Metric | Capture | What it tells us |
|---|---|---|
| Average hand size | Post-draw and turn-end separately | Measure actual liquidity, not just starting six. |
| Turns at 0/1/2 cards | Distribution by runner/phase | Repeated empty turns may indicate overcommitment or deck congestion. |
| Skipped draws/reshuffles | No eligible card, full hand, discard recycle frequency | Distinguish empty supply from voluntary holding. |

## Slots

| Metric | Capture | What it tells us |
|---|---|---|
| Training/Gear installations and occupied-slot rate | By type, round and runner | Are slots genuinely used? |
| Install duration/eligibility | Time from install to exit; count reaching turn +2 | Whether two-turn investment pays off. |
| Sacrifices/combos/Effort | Slot→Movement count, slot+slot, hand+slot, printed Effort | Measure delayed liquidity and card-play mix. |
| Unused Effects | Installations without a meaningful triggered Effect before loss | May reveal poor AI timing or weak specialist match. |

## Condition treatment

| Metric | Capture | What it tells us |
|---|---|---|
| Attachments/duration | Count, origin, turns locked, Effort removed from circulation | Quantify opportunity cost. |
| Partial/complete/station remedies | Counts and Severity delta with attached card disposition | Detect stranded attachments or one-condition station defects. |

## Pace

| Metric | Capture | What it tells us |
|---|---|---|
| Easy/Steady/Race/Push usage | Counts by phase, profile, Energy and Course | A Pace unused everywhere may be dominated or AI-overlooked. |
| Pace changes and preservation | Round-to-round choices, Pack/slot cost modifiers | Distinguish tactical adjustment from cost exploit. |

## Course interaction

| Metric | Capture | What it tells us |
|---|---|---|
| Specialist timing | Installed before relevant side, held through it, sacrificed after it | Test whether visible planning matters. |
| Counterplay gaps | Property/Difficulty/Conditions on zero-Movement and DNF episodes | Rare unsupported sides should be judged by outcomes. |

## Fuel

| Metric | Capture | What it tells us |
|---|---|---|
| Mode/branch/use | Energy vs remedy vs Movement, Nausea blocking | Check opportunity cost and legal Fuel recovery. |

## Will

| Metric | Capture | What it tells us |
|---|---|---|
| Spend and timing | Shortfall, source, turn, Finish distance | Too-early waste or systematic hoarding may indicate AI concern. |

## Events

| Metric | Capture | What it tells us |
|---|---|---|
| Draw/play/mode/target | Event by ID, active targets, invalid plan count | Invalid target Effects indicate implementation defect. |

## Assistance

| Metric | Capture | What it tells us |
|---|---|---|
| Requests/swaps/rescues | Opportunity, partner, cards, immediate/next-turn path | Meaningless swaps or ignored rescue indicate AI/legality issue. |

## Packs

| Metric | Capture | What it tells us |
|---|---|---|
| Formation/size/preservation | Membership snapshots and saved Pace Energy | Measure benefit and stability, not just gross membership. |

## Gut Checks

| Metric | Capture | What it tells us |
|---|---|---|
| Threshold/pass/fail | Hand Effort, bonuses, Energy loss by mile | Measure whether six-card economy changes check difficulty. |

## Stations

| Metric | Capture | What it tells us |
|---|---|---|
| All-eligible treatment | Water/Aid visits, each eligible Condition before/after, Energy separately | Any eligible condition left untreated is an implementation concern. |

## Conditions

| Metric | Capture | What it tells us |
|---|---|---|
| Exposure/severity/duration | By ID, effective vs current Severity, removal reason | Identify sticky penalties and treatment lock-up. |

## Profile performance

| Metric | Capture | What it tells us |
|---|---|---|
| Finishes/places/DNFs | By runner profile and seed with comparable seat/course | Repeated rank pattern may suggest balance or AI bias. |

## Physical Course and lane context for every Movement record

Record the **physical `course_card_id`** and selected physical position (1–13 in a marathon), the **one-mile side ID** (`C-xx-A/B`), whether it is **outbound or return**, assigned race mile, surface, route/terrain, elevation, footing, printed Difficulty, Effective Difficulty and active modifiers. For a marathon, mile `n` and mile `27-n` use opposite lanes of the same physical card at position `n`. Keep separately the quarter-mile space and Start/Finish extension state. Group outcomes by lane and physical card rather than treating 60 side records as 60 physical cards. This permits testing whether a specialist was installed before its relevant visible lane and sacrificed afterward, and whether difficulty/Conditions on paired outbound/return lanes affect progress differently. These are measurement fields, not new Course mechanics.

## Interpretation protocol

- **Healthy gameplay:** legal, deterministic completion with meaningful choices among Pace, card zones and recovery, no recurring forced empty turns, and specialists sometimes paying for their commitment. This is a qualitative pattern, not a new balance threshold.
- **Possible balance concern:** repeated profile gaps, systematic unusable card families, frequent stranded attachments or severe hand scarcity across varied seeds after legality checks. Inspect distributions and traces before changing numbers.
- **AI concern:** legal alternatives exist but deterministic selection routinely ignores a stronger line, for example moving a slot card before its Course benefit or overlooking a rescue. Correct policy or evaluation rather than changing printed cards.
- **Implementation concern:** illegal target, missed station treatment, wrong slot age, duplicate card ID/zone, false DNF, nonrepeatable seed, or impossible Energy payment. Stop a study at such a failure; preserve evidence.
- **Insufficient evidence:** isolated rare side, one seed, different roster sizes mixed together, or outcome without event-level context. Seek an authorized, bounded follow-up rather than inventing a new balance value.

Record numerator, denominator, event schema version, seed, roster, Course orientation, and missing-data reason for each aggregation. Preserve raw logs and a machine-readable rollup so another reviewer can reproduce every count. This specification authorizes no run and sets no new balance values.
