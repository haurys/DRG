# DRG Run 04 — Threshold-Aware AI Setup Evaluator Audit

**Scope:** Read-only review of the baseline at commit `8ca92d605fcfefcab9f49932e0434018fcb8cec0`. No race, alternate seed, rule/data edit, AI scoring edit, or rebalance was performed.

**Sources:** [Run-04 chronological audit](DRG-Marathon-Audit-Run-04.md), [bounded counterfactual analysis](DRG-Run04-Targeted-Counterfactual-Economy-Analysis.md), `engine/simulate.py`, `engine/ai_rationale.py`, `simulation/Simulation-Decision-Rules.md`, and the canonical Training/Gear/Movement rules. Calculations below distinguish the information available to the AI **at its decision** from the later realized Run-04 trajectory.

## 1. Executive summary

1. The evaluator converts **the complete current turn** through the actual integer Movement table and visible Course boundaries. It removes the installed card from the current hand, enforces the two-card limit, applies installation-turn bonuses and Pace preservation, and accounts for replaced effects. Immediate setup opportunity cost is therefore genuinely modeled.
2. Its **future setup term is a continuous proxy**, not a quarter-mile forecast. It averages Effort/Difficulty changes over up to six visible Course sides at the **current Pace**, multiplies by a remaining-distance and duration fraction, and adds small score points. It does not model later starts, Pace changes, threshold crossings, boundary cascades, future hand contents, or physical-card recycling.
3. The GPS Watch rejection was correct **despite**, rather than because of, a threshold-aware future estimate. The proxy credits a +1 Effort average on all six sampled sides based on P8's *current* Pace change. The three later observed Pace changes yielded zero additional quarter-miles at their recorded starts. Those future changes were unknowable to P8 at round 6.
4. Hill Repeats receives **some credit** for two visible Inclines, but the credit averages away any discrete next-boundary effect. A previous linked calculation assumed P6 could play TR-020 in round 8 after the setup plan used it in round 7. Its availability would depend on an unknown intervening draw/recycle. With only cards retained from the round-7 decision, a legal no-draw comparison does **not** show guaranteed payback.
5. The P1 Mile-10 Gut Check retention alternative **was enumerated and scored**. It still crossed Mile 10, avoided two Energy loss, and sacrificed 0.25 mile. The scorer preferred the faster plan by 12.4975 score points. The earlier concern that the AI did not explicitly compare this trade was incorrect.
6. The evaluator has a genuine **modeling blind spot** for future threshold-sensitive setup payoffs, but these six observed rejections do not prove a material wrong decision that can be corrected without assumptions about unseen future cards. Under the stated recommendation gate, **do not change scoring before Run 05**. Keep Run 05's approved AI baseline and add targeted read-only post-run comparisons.

## 2. Current evaluator: code and formula

| Component | Source | Actual inputs and output | Conversion/limitation |
|---|---|---|---|
| Pace timing | `Sim.start_round` and `choose_pace`, `engine/simulate.py` | For each Condition-legal Pace, preview the best complete plan from the **pre-Replenish hand**. Prior Pack is cleared in the preview; a Pack Runner receives a small nearby-runner style estimate. Pace locks before draws and Pack formation. | No future draw or actual newly formed Pack is known to this Pace preview. |
| Legal plans | `legal_treat_prepare`, `treat_candidates`, `movement_candidates`, `choose_turn_plan` | Enumerate no preparation, install/replace Training, equip/replace Gear, attachment, Fuel, treatment, and up to the remaining two Movement cards; filter slots, footwear, Fuel, Event and target legality. | Preparation consumes one play; the installed card is unavailable as current Movement. |
| Preparation preview | `preview_preparation` | Deep-copy runner state; remove the setup card from hand; replace old installed card if needed; install new card with its actual temporary-turn counter. | Correct for the **current** plan; there is no subsequent-turn hand/deck projection. |
| Pace payment preview | `preview_payment`, `pace_cost` | Recalculate cost and legal Will/step-down consequences after preparation, including Pack and installed preservation. | Exact current-state estimate. |
| Current Movement preview | `preview_movement`, `resolve_movement`, `movement` | Sum actual selected cards and current installed/Pace/Event modifiers, subtract Condition penalties and starting Effective Difficulty; convert integer result, traverse boundaries with Effective Difficulty changes, include Direct Movement and cap. | **Discrete threshold and boundary aware for the current turn**. Same-turn Training/Gear effect is already credited. |
| Base objective | `plan_score` | Let `q` be projected quarter-miles and `u` remaining Course quarters. `progress_weight = 12 + min(2, max(0, leader_gap_quarters)/16)`; `turns = u/max(2,q or 2)`; base score `= progress_weight*q - u/8 - 0.15*turns`; legal Finish adds 1000. | Values immediate converted quarters heavily and knows public leader gap. |
| Setup horizon | `plan_score` | `h = min(u,24)/24` **after the plan**, times `min(1,N/6)` for a Temporary(N) card. Persistent cards have no N factor. | The 24 is **quarters (six miles)**, not 24 miles or forecast turns. N/6 is a scalar duration discount; it does not enumerate the N active runner-turns. |
| Future setup proxy | `plan_score` | Sample `self.course[current_side_index:][:6]`. At the current Pace, average `movement_effort_bonus(prepared,side)-movement_effort_bonus(runner,side)` and `effective_difficulty(old)-effective_difficulty(new)`. Also compute **current** Pace-cost reduction. Add `h*(2*clamp(mean Effort,−3,3)+2*clamp(mean Difficulty reduction,−3,3)+2*Pace-cost reduction)` and subtract `1−0.6h`. | **Continuous score points.** Does not call the Movement converter for a later turn, predict later start spaces/Paces, or account for future card draws. Current Pace and `previous_pace` are reused across every sampled side. |
| Other setup terms | `plan_score` | Add discounted Training acquisition resistance, Gut Check modifier if a checkpoint remains, Hydration Belt Water potential, and Anti-Chafe prevention. | Gut modifier is a direct score term, not a future threshold pass probability; other terms do not enumerate future Conditions. |
| Resources and hand | `plan_score` | Preview current Event Energy, current-turn crossing Gut Checks using cards left in hand, Energy with cap/floor, Will use, a small retained-hand Effort term, and bounded profile preferences. | Current crossing checks are explicit. Future Gut Check retention and future hand circulation are not forecast. |
| Selection | `choose_turn_plan` | Select max legal score, with deterministic tie fields; exclude projected zero-Movement plans when a positive plan exists unless low Energy/severe Condition permits full comparison. | No separate setup-first rule overrides Victory priority. |
| Rationale diagnostics | `engine/ai_rationale.py: _detail` | Report best two-card Movement alternative, immediate difference in quarters, visible six-side means and horizon, projected score and turns. | `estimated_turns_to_recover_setup = remaining_after/max(2,current_plan_quarters)` estimates **turns to finish at the current projected rate**. Despite its name it does **not** calculate setup break-even activations or payback turns. |

Replacement removes the old installed effect in `preview_preparation`, so both current conversion and the future mean compare the new setup with the actual displaced setup. The rationale's `immediate_movement_opportunity_cost_quarters` is an observation relative to the best logged no-preparation two-card plan, including an Event if applicable; the scorer does not subtract that field a second time. The current Movement difference already enters its base score. Some rationale score components are not separately emitted, but the formulas above are present in code.

## 3. Information boundary

**Legitimately available after Replenish:** own current hand and its physical IDs/printed Effort; locked Pace; Energy/Will; active Conditions; installed Training/equipped and attached Gear; current quarter-mile position; the full revealed marathon Course with elevations, routes and surfaces; active staged/Course/Global effects; round Pack state; public opponent positions/finished flags; and remaining distance. The AI can evaluate legal retained-card combinations without knowing a subsequent draw. Before Replenish, Pace selection uses the then-current hand and no newly drawn cards.

**Unavailable:** order or identity of future deck draws, unseen Conditions/Events, future opponents' choices, future Pack formation, future own Pace changes, and whether a currently discarded physical card will circulate back at a particular time. The existing scorer does not inspect future deck order in these setup calculations. An alternative evaluator may use the known deck composition only through a declared distribution; it must never treat the realized future draw as decision-time knowledge.

**Important distinction:** The entire Course is visible, but the runner's future *start* on a given Course side and integer Movement result are not. An observable Incline is not a guaranteed two-quarter gain.

## 4. Hill Repeats — P6 round 7

P6 was at **mile 9.0**, Energy 12, Easy Pace, Course side C-19-A (mile 10, printed/effective Difficulty 3), with 17.0 Course miles remaining. The best two-card Movement plan played FU-013 (Effort 3) and TR-009 Hill Repeats (Effort 7), projected **1.00 mile**, score **46.350**. The best logged Hill installation played TR-009 as setup and TR-020 Mental Toughness (Effort 9) as Movement, projected **0.75 mile**, score **33.408**. Its immediate cost was **one quarter**, and its score deficit was **12.942**.

The six sides sampled by the future proxy are miles **10–15**: mile 10 Rolling Difficulty 3; mile 11 Incline 8; mile 12 Incline 3; miles 13–15 not Incline. Hill Repeats reduces miles 11 and 12 by 2 each, so the scorer records **mean Difficulty reduction 4/6 = 0.667** and horizon 1.00. Its direct future setup addend is `2*(2/3) − 0.4 = 0.933` score points before shared score terms. The next visible harder boundary is mile 11, from Difficulty 3 at mile 10 to an installed Difficulty 6; the effect can also reevaluate at the next Incline boundary.

The scorer therefore **partially values Hill Repeats**, but averages the reductions and does not ask whether a known next-turn card/Pace result reaches another quarter. The bounded report's fixed R8 start at mile 10.0 found a **+0.75-mile marginal response** to Hill. That observation is diagnostic, not a decision-time expectation.

**Correction to the earlier linked payback claim:** The Hill setup plays TR-020 as Movement in R7. The actual R8 Movement also uses TR-020, plus newly acquired GE-004. In the setup branch TR-020 has been discarded and may be reused in R8 **only if a future recycle/draw returns it**. Neither that draw nor GE-004 was known at the R7 decision. Keeping the actual R8 cards while moving the R7 starting position is therefore not a rules-faithful guaranteed counterfactual.

A conservative **known-retained-hand, no-new-draw** check illustrates the risk without predicting the next draw: after the Hill setup P6 retains EV-017:6, FU-004:4, GE-003:4, FU-013:3 and EV-001:5. Both EV-017 and EV-001 are Events and cannot form a legal two-Event pair; the largest printed legal pair is 10. With the current Easy Pace and the visible Course, a bounded next-turn calculation from the setup endpoint 9.75 ends at **10.25**. Without setup, P6 retains TR-020:9 and EV-017:6, a legal 15-Effort pair; from the selected endpoint 10.00 it ends at **11.00**. This is a no-draw scenario, **not a forecast that R8 would choose those plans**. It proves only that the visible R7 hand did not guarantee near-term setup payback.

**Assessment:** Continuous averaging misses the *possibility* of a large boundary threshold effect, but the decision-time hand comparison does not demonstrate that the AI rejected a materially superior legal plan. Classification: **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** for this particular decision. A threshold-specific diagnostic is warranted; a scoring correction is not yet warranted.

## 5. Trail Shoes — P6 round 2

P6 was at mile **2.0** on C-09-A (mile 3, Trail route, Difficulty 5), Race Pace, Energy 15, with 24.0 Course miles remaining. The selected GE-020 + EV-014 plan projected **0.75 mile** and scored **27.350**. Equipping GE-005 Trail Shoes and playing EV-014 projected **0.25 mile**, scored **−0.133**, and sacrificed **two quarters**. Its **same-turn Trail +2 Effort is already included** in that 0.25-mile projection; the card's Effort 7 is unavailable for Movement.

The future proxy samples miles **3–8**. Only mile 3 is Trail, hence mean Effort gain **2/6 = 0.333**, horizon 1.00, direct future addend `2/3 − 0.4 = 0.267` score points. The entire Course is visible, including later Trail sides at miles 9, 14, 18 and 24; this particular six-side mean does not look far enough to value a later compatible start. A *visible side* is not a guaranteed Movement start. The bounded prior report found a fixed-state **+0.50 mile** at P6's actual later mile-14 Trail start, equal to the setup's immediate cost, but that is not a guaranteed payoff.

`preview_preparation` correctly removes GE-005 from the hand now and retains it in the equipped zone; it does **not** model subsequent deck circulation. In the actual trajectory P6 used that same physical GE-005 as Movement in rounds 3 and 6. Those observed plays would be unavailable after equipping it in round 2, and subsequent hands/draws would diverge. The future six-side mean does not convert +2 Effort into quarter-miles.

**Assessment:** The proxy can miss distant Trail opportunities and their threshold impact, but the realized fixed-state +0.50 mile relies on a future state inconsistent with known card circulation. Classification: **INSUFFICIENT EVIDENCE** for a wrong decision; the immediate equip comparison itself is sound.

## 6. GPS Watch — P8 round 6 negative control

P8 was at mile **9.0**, Energy 14, Push Pace after changing from Race, with 17.0 Course miles remaining. Selected GE-016 GPS Watch (Effort 8) + TR-005 as Movement: **1.25 miles**, score **57.348**. Equip GE-016 + move TR-005: **1.00 mile**, score **46.000**. Installation costs **one quarter** and the scorer gives the same-turn +1 Effort because the Pace changed.

The six-side future sample records **mean +1 Effort** and horizon 1.00, making the direct setup proxy `2*1−0.4 = 1.600` score points. This is **not** a sound future Pace forecast: `movement_effort_bonus(prepared, side)` is called six times with P8's same current `previous_pace != pace` state, so all six Course sides appear eligible. GPS Watch actually checks for a change at each later Round Start, which was unknown in R6.

The subsequent observed Pace changes occurred in **R10, R11 and R14**. At their recorded Movement starts, adding one Effort to result **10→11**, **11→12** and **18→19** added **0, 0, 0 quarters**, respectively, including boundary/cap behavior. This is an ex-post negative control only; P8 could not know those draws, Paces or integer results in R6. Equipping also changes physical-card circulation, although both R6 plans leave the same other card IDs in hand after using TR-005.

**Assessment:** The **rejection** was appropriate on the observed trajectory, but it happened **despite an optimistic continuous future proxy**, not because the scorer anticipated nonconverting activations. Classification: **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** for this decision, with a specifically identified GPS forecasting defect in the proxy.

## 7. Temporary setup cards

Installation is Turn 1 in the canonical duration and the exact current-turn preview. For **future** value, the scorer scales its six-side current-Pace mean by `N/6`; it does not enumerate Turn 2 through Turn N or infer their Paces and hands.

| Case | Logged current comparison | Current future proxy (score addend) | Bounded realized diagnostic; not decision-time knowledge | Assessment |
|---|---|---|---|---|
| **Intervals** TR-007, P8 R1 | Setup + EV-023: 1.50 miles, score 67.725; selected two-card Movement: 2.00, score 92.425; **2 quarters lost**. | Temporary(3): current Push assumed for six sampled sides; mean +1 Effort and current Pace preservation 1. `h=3/6=0.5`; addend `0.5*(2+2)−0.7=1.300`. Current-turn installation benefit and cost payment are separately previewed. | R2 Race, R3 Push; R3's +1 at its recorded result yields **0 quarters**. Round-1/3 preservation may be capped by Event Energy gains. | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** for rejection. Future Pace and thresholds are not explicitly modeled. |
| **Carbon Racers** GE-011, P3 R2 | Setup + FU-015: 0.75 miles, score 30.075; selected GE-011 + FU-015: 2.00, score 94.900; **5 quarters lost**. | Temporary(3), current Race +2 Effort across six sampled sides; `h=0.5`; addend `0.5*4−0.7=1.300`. No enumeration of the two future active turns. | Observed R3 Push and R4 Race each gain one fixed-state quarter, **0.50 mile total**, below 1.25 lost. | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** for rejection. |
| **Tempo Shoes** GE-007, P5 R4 | Setup + EV-003: 1.00 mile, score 44.329; selected GE-007 + EV-003: 1.75, score 81.964; **3 quarters lost**. | Temporary(5), current Race +1 on all six sampled sides; `h=5/6`; addend `(5/6)*2−0.5=1.167`. Actual future Paces unknown. | Observed R5–R8 were Race but +1 yielded **0 quarters on all four fixed starts**. | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** for rejection. |

For each, the current-turn Movement forecast is threshold-aware, including the installed benefit. The future value is **neither duration-window exact nor threshold-aware**. The three rejections were supported by large immediate costs and are not evidence that the proxy caused a wrong choice.

## 8. Bounded visible-information alternative

This is a **diagnostic comparator**, not a replacement scoring formula or a proposal to run another race:

1. Preserve current legal-plan enumeration, immediate exact Movement preview, Energy payment, Event/Gut effect, replacement and finish score.
2. For each setup plan, record its exact **current** endpoint and retained physical IDs. Never allow an equipped/installed or played card to appear in a future retained-hand plan merely because Run 04 later redrew it.
3. Take the first one or two remaining *active runner-turns* for temporary effects, or the next one or two plausible visible Course starts for persistent effects. Use the public Course, current Conditions, Energy and legally available Paces. From the **known retained hand alone**, enumerate legal one/two-card Movement pairs. Treat unknown replenishment as an uncertainty interval, not a specific card.
4. At each bounded start, compute the difference in converted quarter-miles from the card's actual Effort or Effective Difficulty modifier, including immediate boundary reevaluation and caps. For GPS Watch, count +1 only in a scenario with a legal **new Pace change**. For terrain Effort, apply it only at that Movement's starting side. For temporary cards, stop after their remaining active turns.
5. Track three outcomes: **known-hand lower bound**, **plausible visible-state scenarios** with explicitly stated future-card uncertainty, and **maximum feasible threshold response**. Report a material advantage only when it survives the changed current endpoint, card removal, and legal two-card/Event limits. Do not assign probabilities to unseen draws without an approved distribution.
6. Compare quarter-mile and effective Energy ranges against the current immediate deficit. If ranges overlap or future draws decide the result, mark the plan **undetermined** and retain the current decision; this is a diagnostic abstention, not a new weight.

The method can catch a locally robust next-boundary payoff while refusing to “predict” the actual R8 P6 draw or P8's later Pace changes. It also exposes when a continuous +1 Effort forecast is worth zero quarters over the known scenarios. It remains intentionally bounded rather than perfect lookahead.

## 9. Current versus alternative, using decision-time evidence

| Case | Current estimate and choice | Visible-information comparator | Would it reverse the choice? | Classification |
|---|---|---|---|---|
| Hill Repeats P6 R7 | −1 current quarter; six-side mean Difficulty −0.667, setup addend +0.933 score; **reject**. | Next Incline is visible, but R7 setup consumes TR-020. Known-hand/no-draw legal next-turn comparison does not repay; unknown draws could create a threshold cascade. | **No justified reversal.** | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE**; threshold structure is missed, not a proven material error. |
| Trail Shoes P6 R2 | −2 quarters; six-side mean +0.333 Effort, addend +0.267; **reject**. | Later Trails visible, actual starts/draws unknown; GE-005 cannot also be Movement in R3/R6 after equip. | **Undetermined; retain current rejection.** | **INSUFFICIENT EVIDENCE**. |
| GPS Watch P8 R6 | −1 quarter; mean +1 Effort, addend +1.600; **reject**. | No known future Pace change, and +1 does not guarantee a converted quarter. Realized R10/R11/R14 sensitivity zero. | **No reversal.** | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE** outcome; proxy is optimistic. |
| Intervals P8 R1 | −2 quarters; mean +1 Effort/+1 current Pace preservation, `h=.5`, addend +1.300; **reject**. | Only two future active turns; Paces and replenishment unknown, known current deficit large. | **No justified reversal.** | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE**. |
| Carbon Racers P3 R2 | −5 quarters; mean +2 Effort, `h=.5`, addend +1.300; **reject**. | Only two future active turns; actual compatible fixed-state gain was two quarters, not known in R2. | **No justified reversal.** | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE**. |
| Tempo Shoes P5 R4 | −3 quarters; mean +1 Effort, `h=5/6`, addend +1.167; **reject**. | Four future active turns, Pace unknown; no guaranteed threshold gain from known cards. | **No justified reversal.** | **CURRENT EVALUATOR APPROXIMATE BUT ACCEPTABLE**. |

“No justified reversal” is the conservative output of a comparator with uncertainty bounds, **not** a claim that a changed scorer would produce a specific numeric score or that these installations could never win under other draws.

## 10. Gut Check retention evaluator — P1 Mile 10

At P1 R7, the AI knew its hand after Replenish, Easy Pace, Energy 12, mile 9.0, current mile-10 Difficulty 3, checkpoint threshold 25, and available legal Movement pairs. It enumerated **81 legal complete plans**, including the following two:

| Plan | Projected Movement | Hand Effort at Mile 10 | Gut result | Projected post-Event/check Energy | Existing score |
|---|---:|---:|---|---:|---:|
| Selected GE-011:8 + EV-022:9 | 1.25 mi, endpoint 10.25 | 19 | FAIL; −2 Energy | 13 after Second Wind +3 and failure | **57.4725** |
| Rejected FU-010:2 + EV-022:9, retain GE-011 | 1.00 mi, endpoint 10.00 | 25 | PASS; no loss | 15 after Second Wind +3 | **44.9750** |

`preview_movement` establishes that the alternative still reaches the checkpoint; `plan_score` checks the hand *after committed cards* at every crossed Gut Check, floors Energy loss, and gives a small retained-hand Effort benefit. The comparison is therefore **REPRESENTED**, not absent or merely partial. The rationale includes this exact rejected pair.

The score gap **12.4975** reconciles from the code: one extra selected quarter gives **+12.3125** position-weighted progress; one fewer remaining quarter gives **+0.125**; the current-rate remaining-turn term contributes **+0.510**; the alternative's two extra Energy are worth **−0.300** to the selected plan; and its six extra retained Effort is worth **−0.150**. Sum: **12.4975**. The estimated turns (12.6 vs 16.0) are current-plan-rate heuristics, not predicted future draws. A 0.25-mile lead versus two Energy and a stronger hand has no proven finish-time winner in the one observed race. The scorer explicitly valued the trade and chose speed.

This finding supersedes the narrower prior report's suggestion that P1's retention comparison might be missing. It does **not** imply the existing Energy weight is optimal; that would require evidence about finish-time conversion.

## 11. Evidence-supported recommendations

The prescribed scoring-change gate is **not met**:

1. **Material missed value:** the future setup proxy demonstrably ignores discrete later threshold outcomes and misuses the current Pace-change state for GPS Watch across six sides. But no studied rejection establishes a robust, superior setup from *decision-time* legal cards and states. The previous Hill near-payback counterfactual depended on reusing a played card through an unknown draw.
2. **Visible estimability:** a bounded known-hand, visible-Course threshold diagnostic is feasible. Precise future payback is not, absent a declared draw/Pace uncertainty model.
3. **No hidden knowledge:** the alternative above stays within this boundary.
4. **Positive and negative controls:** Trail Training's zero-cost installation was already selected and produced threshold-sensitive benefits; GPS Watch was correctly rejected despite optimistic proxy credit. A scoring correction has not been shown to improve both.

**Recommendation: do not modify AI weights or rules on this evidence.** For any subsequent authorized implementation pass, first add diagnostic-only bounded fixtures at Hill's visible boundary and GPS Watch's Pace-change condition, and verify card-ID conservation and no-draw vs possible-draw bounds. The diagnostic should compare *converted* quarters, never simply count raw Effort. Reassess weights only if a legitimately visible case yields a material, robust payoff that the current scorer rejects and the negative control remains rejected.

## 12. Run 05 disposition

**Run 05 may proceed with the current AI unchanged** if the objective is another controlled observation. Pre-register the six setup cards as cases, preserve full legal-plan rationales, and post-process each compatible activation into actual quarter-mile gain, current-vs-future hand availability, and duration remaining. Continue logging every crossing Gut Check with the best legal same-turn passing alternative. Do not interpret Run 05 as a validation of a scoring correction; none was made here.

**Limits:** Future draws and opponent/Pack decisions are unknowable at earlier choices. The negative-control and realized threshold calculations describe Run 04, while the alternative comparator is deliberately abstaining where a future draw determines the outcome. A single race cannot establish optimal AI scoring across the deck.
