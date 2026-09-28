# DRG Run 04 — Targeted Counterfactual Economy Analysis

**Scope:** Read-only, bounded calculations on the single preserved Run 04 (seed `20260924`, baseline `8ca92d605fcfefcab9f49932e0434018fcb8cec0`). No race was rerun, no random draw was made, and no code, rule, card, Course, or AI weight was changed.

**Source provenance:** [Run-04 audit](DRG-Marathon-Audit-Run-04.md), its 142 chronological AI rationales and Movement/Milestone events, the canonical Movement table and card inventories in this checkout. The separately named `DRG-Run04-Strategy-Economy-Audit.md` was not present in this checkout and was not found as an exact saved-file match. Its prior written findings—especially the selected setup cases and priority questions—are secondary context, not a substitute for the Run-04 event data.

## 1. Executive summary

- A setup card's Effort bonus is worth **zero** movement on many otherwise compatible turns. An additional Effort point crosses an ordinary Movement-table step only at certain integer results; a Course boundary can amplify its distance effect. Persistent duration alone does not establish payback.
- **GPS Watch, P8 round 6:** equipping sacrificed 0.25 mile. Its three later observed Pace changes (rounds 10, 11, 14) each yielded **zero additional movement** when +1 Effort was applied to the recorded Movement result and Course state. The observed-trajectory rejection is probably correct. Different future card/Pace choices could alter that conclusion; the AI did not know them.
- **Temporary cards:** P8's Intervals recovered zero movement on its one compatible later turn; P3's Carbon Racers recovered a fixed-state 0.50 mile against 1.25 sacrificed; P5's Tempo Shoes recovered zero later miles against 0.75 sacrificed. Their windows did not rescue those particular setup plays.
- **Hill Repeats, P6 round 7:** a fixed-position calculation suggests +0.75 mile at the next incline. Linking the install turn's 0.25-mile loss changes the next turn's start, and P6 reaches **the same mile 11.0 position after round 8** as in Run 04. That is repayment by the next turn, but not an observed lead or earlier finish.
- Among **18 failed Gut Checks**, five have a legal one-card printed-Effort swap that reaches the threshold on paper. Four of those swaps prevent the runner from reaching that checkpoint in the same turn. The one same-turn pass is P1 at Mile 10: 0.25 mile sacrificed to avoid two actual Energy lost. At Mile 23, **none** of eight failures can pass by one immediate card-retention swap.
- These findings support **no immediate rule/card/scoring change**. The best next investigation is whether threshold-aware, position-linked setup and retention valuation changes decisions in a controlled future run.

## 2. Break-even method and limits

The canonical Base Movement table converts integer Movement result `R` to quarter-miles: `R≤0→0`; `1–2→1`, `3–4→2`, ..., `13–14→7`, and `R≥15→8`. `R` includes printed Effort, installed/Event/Pace Effort, Condition Effort penalties, and starting Effective Difficulty. Direct Movement is separate. At each one-mile boundary the remaining integer result changes by **new Effective Difficulty − previous Effective Difficulty**; the normal turn cap is two miles. These calculations use that conversion and the logged Course, current position, result, direct Movement and boundaries.

**Immediate cost** is the best logged two-card Movement projection minus the best logged legal setup + Move projection, both at the existing chosen Pace. Same-turn installation benefit is already included in the setup projection. A score gap is recorded for context; it cannot be converted to miles because score components and future draws are not fully exposed.

**Fixed-state future marginal** applies the card's benefit to each compatible *recorded* future Movement starting state, converts it through the table and Course boundaries, and caps it as the run did. It is a sensitivity measurement, **not a replay of an alternate race**. Installing a card changes the current position, hand/deck circulation, potentially Pack membership, later draws, and future choices. Consequently future marginal miles cannot generally be summed into a finish-time prediction. Where material, a linked two-turn calculation updates the next turn's starting position using the same recorded cards and Pace. No hidden information is attributed to the AI.

For persistent cards, a counted activation means the observed Pace/route/elevation condition was compatible at a Movement start; terrain Difficulty also reevaluates at boundaries. For temporary cards, the installation turn is Turn 1. An “activation required” is a **quarter-mile threshold gain**, not simply one Effort modifier. If the recorded compatible turns did not cross enough thresholds, break-even requires changed future card/state choices. The fixed-state check reproduces the logged Movement on the studied turns; two unrelated P4 turns elsewhere had other unmodeled state modifiers and are excluded from these comparisons.

## 3. Training break-even table

| Opportunity | Remaining / setup cost | Effect and observed compatible opportunities | Threshold result on fixed observed future states | Classification / AI diagnosis |
|---|---:|---|---|---|
| **Intervals** TR-007, P8 R1 | 26.0 mi / **0.50 mi** (2 quarters); setup 1.50 vs two-card Move 2.00 | Temporary(3); Push +1 Effort and preserve 1 Pace Energy. Push on installation R1 and R3; R2 Race. Discount 0.50; score gap 24.70. | R3 result 10→11 yields **0 quarters**. Setup already includes R1 benefit. Up to one effective Energy could be preserved in each Push turn, but P8's Energy was at its 15 cap amid Event gains, so retained Energy benefit is uncertain. Needs 2 quarters of future distance, got 0. | **UNLIKELY TO BREAK EVEN; AI PROBABLY CORRECT.** |
| **Hill Repeats** TR-009, P6 R7 | 17.0 mi / **0.25 mi** (1 quarter); 0.75 vs 1.00 | Persistent; Incline −2 Difficulty, Steep Incline −1. Observed later starts: R8 mile 11 Incline, R9 mile 12 Incline, R17 mile 24 Steep Incline, R18 mile 26 Incline; intervening boundary effects included. Discount 1.00; score gap 12.94. | Fixed-position R8 has **+0.75 mi**; other recorded starts add zero. Linked R7–R8 calculation gives equal position at mile 11.0 by R8's end (details below). | **BREAKS EVEN PLAUSIBLY**, without an observed net lead; **AI VALUATION QUESTIONABLE** as a near-term threshold case, not proven wrong. |
| **Base Miles** TR-003, P3 R6 | 17.0 mi / **0.50 mi** (2 quarters); best setup 0.75 vs 1.25 | Persistent Easy +1 Effort and acquisition resistance to Dead Legs/Tight Calf. Easy at R6 and R16; no matching future Condition acquisition. Score gap 23.23. | R16 result 8→9 gains **0**. R10's observed Movement uses the same TR-003, which could not be played if installed. Needs 2 quarters; none measured. | **UNLIKELY TO BREAK EVEN; AI CORRECT** for the observed opportunities. |
| **Long Run** TR-002, P3 R4 | 20.5 mi / **1.00 mi** (4 quarters); 0.75 vs 1.75 | Persistent Race preservation of 1 Pace Energy and resistance to new Dead Legs. P3 has five observed Race turns at/after R4 with a positive Pace payment; no later Dead Legs. Score gap 49.34. | No direct Movement modifier. Up to **5 Energy** could be spared before caps/trajectory changes; P3 finished with 4 Energy and no Will use. No demonstrated way to turn those savings into four quarters or an earlier finish. | **UNLIKELY TO BREAK EVEN in Movement; AI PROBABLY CORRECT.** |
| **Mental Toughness** TR-019, P7 R3 | 23.0 mi / **0.75 mi** (3 quarters); 0.50 vs 1.25 | Persistent +2 Gut Check. Three future checks: observed 26/25, 30/30, 29/35. Score gap 40.95. | Modified totals 28, 32, 31: **no result flips and no Energy saved**. | **UNLIKELY TO BREAK EVEN; AI CORRECT.** |
| **Strength Training** TR-012, P8 R6 | 17.0 mi / **0.25 mi**; 1.00 vs 1.25 | Persistent +1 Gut Check plus acquisition resistance. Later check totals 26, 27, 27 before modifier; P8 drew no Condition in this race. Score gap 11.30. | +1 changes no pass/fail and gains no movement. | **UNLIKELY TO BREAK EVEN; AI CORRECT** in this bounded case. |
| **Downhill Practice** TR-018, P2 R10 | 10.5 mi / **0.25 mi**; 1.00 vs 1.25 | Persistent Descent −2, Steep Descent −1 Difficulty. R12 starts on mile 19 Descent; score gap 12.31. | R12's fixed result and Course traversal gain **0 quarters**. R13's observed Movement uses this physical card, an installation/hand collision. | **UNLIKELY TO BREAK EVEN; AI PROBABLY CORRECT.** |
| **Trail Training** TR-015, P4 R11 | 12.75 mi / **0.00 mi**; selected 0.75 vs 0.75 | Persistent Trail +1 Effort; actual installation. Three recorded activations (R11, R15, R19). | Removing +1 at each fixed start lowers Movement by 0.25, 0.75, 0.75 mile respectively; these are **separate marginal sensitivities**, not additive finish-time gains. | **BREAKS EVEN QUICKLY**: no upfront distance lost; positive R11 threshold gain. Positive control for the method. |

The linked **Hill Repeats** calculation matters. Without installation, P6 goes 9.00→10.00 in R7 and 10.00→11.00 in R8. The logged setup candidate projects R7 9.00→9.75. With Hill installed, R8 would start at 9.75 on Difficulty 3 rather than mile 11's Difficulty 8; using R8's recorded cards/Pace and applying the −2 when it reaches the Incline gives 9.75→11.00. Thus it repays the R7 quarter-mile by R8's end, while the temporary R7 gap and changed Pack/hand consequences remain unquantified.

## 4. Gear break-even table

| Opportunity | Remaining / setup cost | Effect and observed compatible opportunities | Threshold result on fixed observed future states | Classification / AI diagnosis |
|---|---:|---|---|---|
| **GPS Watch** GE-016, P8 R6 | 17.0 mi / **0.25 mi**; 1.00 vs 1.25 | Persistent +1 Effort if Pace changed this Round Start. R6 installation-turn Pace changed; later R10, R11, R14 also changed. Score gap 11.35. | On R10/R11/R14, +1 gives **0/0/0 quarters**. R6 setup projection already includes its same-turn effect. Needs one future quarter, got zero. | **MARGINAL in principle; AI PROBABLY CORRECT** on the observed trajectory. |
| **Carbon Racers** GE-011, P3 R2 | 24.0 mi / **1.25 mi** (5 quarters); 0.75 vs 2.00 | Temporary(3) Footwear, Race/Push +2 Effort; R2 Race, R3 Push, R4 Race. Discount 0.50; score gap 64.82. | R3 +0.25, R4 +0.25 = **0.50 mi** on fixed future starts; R2 included in setup projection. At least three more quarters needed, with no duration left. | **UNLIKELY TO BREAK EVEN; AI CORRECT.** |
| **Tempo Shoes** GE-007, P5 R4 | 20.25 mi / **0.75 mi** (3 quarters); 1.00 vs 1.75 | Temporary(5) Footwear, Steady/Race +1 Effort. R4–R8 observed Race. Discount 0.833; score gap 37.64. | R5–R8 each gain **0 quarters**. R4's +1 is included in setup projection; +1 on the original R4 Move plan would cross one quarter, but that is **not** an additional post-setup gain. | **UNLIKELY TO BREAK EVEN; AI CORRECT.** |
| **Trail Shoes** GE-005, P6 R2 | 24.0 mi / **0.50 mi** (2 quarters); 0.25 vs selected two-card 0.75 | Persistent Footwear, Trail-route +2 Effort. Recorded Trail starts R2, R3, R11, R17. Discount 1.00; score gap 27.48. | Fixed future: R3 0, R11 **+0.50 mi**, R17 0. However R3 and R6 actually use GE-005 as Movement, impossible if it was equipped in R2; deck/hand and positions would diverge. | **MARGINAL / INSUFFICIENT EVIDENCE** for true payoff; **AI VALUATION QUESTIONABLE**, not proven incorrect. |
| **Pace Band** GE-018, P4 R7 | 16.75 mi / **0.50 mi** (2 quarters); 0.50 vs 1.00 | Persistent +1 Gut Check. P4's relevant actual check totals are 27/25, 22/30, 23/35. Score gap 27.71. | 28 pass, 23 fail, 24 fail: **no result flips**. | **UNLIKELY TO BREAK EVEN; AI CORRECT.** |
| **Anti-Chafe** GE-014, P7 R3 | 23.0 mi / **0.25 mi**; 1.00 vs 1.25 | Temporary prevention of a *new* Hot Spot; discount 0.667; score gap 13.74. | P7 already had a Hot Spot; no later Hot Spot was acquired. No observed protection benefit. | **UNLIKELY TO BREAK EVEN; AI CORRECT** in this race. |

Temporary setup is **not structurally more viable on this evidence**: its limited window magnifies immediate two-play cost when compatible turns fail to cross quarter-mile thresholds. A persistent card can wait for a later suitable Course/Pace state, though later draws and card collisions make its true value uncertain.

## 5. GPS Watch deep dive

P8 entered R6 at mile 9.0 on Push, with 17.0 Course miles remaining. The best recorded GPS Watch equip plan projected **1.00 mile**, compared with **1.25 miles** for the selected Move + Move; existing score gap **11.35**, remaining-distance discount **1.00**. GPS Watch is Effort 8, and its installation uses one of two card plays. The setup projection includes a same-turn +1 because P8 changed Pace at R6; it still moves a quarter-mile less.

| Later Pace change | Course start | Logged Movement result | Result with +1 | Actual fixed-state mile increment |
|---|---|---:|---:|---:|
| R10: Push→Easy | 15.75, C-29-A | 10 | 11 | 0.00 |
| R11: Easy→Push | 17.00, C-23-A | 11 | 12 | 0.00 |
| R14: Push→Race | 22.75, C-01-A | 18 | 19 | 0.00; two-mile cap applies |

**Lower-bound realized value:** zero future miles. **Observed-trajectory sensitivity:** zero future miles across all three eligible starts, so no recovery of the installation quarter. **Optimistic mathematical bound:** with these same three start spaces/Course sides but different integer Movement results, +1 could add at most **1, 3, and 3 quarter-mile units** respectively under the boundary calculation, or **1.75 miles in total**. That bound does **not** establish that those alternate results were attainable with P8's legal cards or that the runner would keep the same starts, Pace changes, Pack, or finish round. The minimum useful future activation is **one that actually adds at least one quarter**, not merely one that grants +1 Effort. None of the three recorded activations meets it.

**Diagnosis:** AI **PROBABLY CORRECT** to reject this particular equip. The six-visible-segment mean-Effort setup estimate could miss threshold effects in some other state, but this case does not demonstrate underpricing.

## 6. Temporary and terrain checks

- **Intervals:** Installation Turn 1 gives its Push effect but leaves a 0.50-mile Movement deficit. Of the next two duration turns, only R3 is Push; result 10→11 adds no quarter. Its one-Energy preservation can be valuable in general, but this P8 window had capped Energy and Event gains. It does not repay the lost distance on observed cards.
- **Carbon Racers:** Two compatible *later* turns add one quarter each after conversion. The three-turn lifetime ends with a 0.75-mile unrecovered setup deficit.
- **Tempo Shoes:** Four later compatible Race turns each add +1 Effort and zero distance. Five compatible Pace choices are not five useful Movement activations.
- **Hill Repeats:** Future Incline starts at miles 11 and 12 and late steep/ordinary inclines at miles 24 and 26 exist for P6. Boundary reevaluation makes the next incline important. The linked R7–R8 position calculation reaches equality; no later fixed-state gain establishes a lead.
- **Trail Shoes:** The future mile-14 Trail start yields a two-quarter fixed-state gain, enough to match its R2 cost; the observed reuse of the physical card as Movement in R3/R6 makes this an unstable counterfactual. Entering Trail mid-Movement does **not** create its Effort benefit until the next Movement.
- **Base Miles:** P3's Easy starts offer no later threshold gain; its acquisition resistance has no matching future Condition in this race.
- **Downhill Practice** is an additional small-cost control: P2 R10 loses 0.25 mile to install, while the later observed Descent start at mile 19 gains zero movement from its −2 Difficulty. This remains Difficulty reduction, not Effort.

## 7. Gut Check retention: every failed crossing

Each hand lists **physical ID:printed Effort** at the exact crossing. “Used” identifies committed Movement cards; a Treat/Prepare card, if any, is already absent from the crossing hand. A swap retains the stated used card and plays the listed held card instead. The alternative recalculates the original turn's Effort, applicable changed Event/direct effect, Course boundaries and legal Event count at the **same starting state**. “End” is the resulting position. Actual Energy lost is used, including zero-floor clipping. A paper pass that ends short of the checkpoint **does not pass a Gut Check in that turn**. Future draws after such a change are unknown.

| Mile | Runner | Hand / threshold | Hand at crossing | Used immediately before crossing | Smallest threshold-reaching one-card swap, if any | Actual loss |
|---:|---|---:|---|---|---|---:|
| 10 | P1 R7 | 19 / 25 | FU-008:4, FU-021:3, FU-010:2, EV-009:4, GE-012:6 | GE-011:8, EV-022:9 | GE-011→FU-010; hand +6; movement −0.25; **end 10.00, pass** | 2 |
| 10 | P2 R6 | 23 / 25 | FU-011:4, FU-006:3, FU-016:4, TR-017:4, TR-007:8 | FU-019:5, EV-023:10 | FU-019→FU-006; hand +2; movement −0.25; **end 9.75, no crossing** | 2 |
| 10 | P3 R6 | 21 / 25 | EV-029:2, EV-018:3, EV-020:5, TR-011:5, TR-003:6 | FU-014:5, EV-027:6 | EV-027→EV-029; hand +4; movement −0.75 including lost Tailwind direct Movement; **end 9.50, no crossing** | 2 |
| 18 | P1 R13 | 16 / 30 | FU-008:4, FU-021:3, FU-010:2, EV-009:4, FU-013:3 | TR-009:7, TR-012:5 | No passing one-card swap; highest legal single-swap total 21 | 2 |
| 18 | P2 R11 | 22 / 30 | FU-011:4, FU-006:3, FU-016:4, GE-015:5, EV-024:6 | FU-022:8, TR-004:8 | None; maximum 27 | 0 |
| 18 | P3 R11 | 21 / 30 | EV-029:2, EV-018:3, EV-020:5, EV-008:3, EV-025:8 | GE-009:5, EV-022:9 | None; maximum 28 | 2 |
| 18 | P4 R15 | 22 / 30 | EV-011:5, EV-005:5, EV-028:3, EV-007:4, GE-006:5 | FU-005:6 | None; maximum 25 | 2 |
| 18 | P5 R12 | 22 / 30 | GE-010:4, FU-001:3, EV-006:6, GE-017:5, TR-017:4 | GE-013:6, GE-016:8 | None; maximum 27 | 2 |
| 18 | P6 R13 | 25 / 30 | EV-017:6, FU-004:4, EV-001:5, EV-010:6, GE-008:4 | TR-019:9, GE-011:8 | TR-019→FU-004; hand +5; movement −0.50; **end 17.50, no crossing** | 2 |
| 18 | P8 R11 | 27 / 30 | EV-026:4, EV-030:5, TR-006:6, GE-020:6, TR-003:6 | TR-014:6, GE-001:7 | GE-001→EV-026; hand +3; Porta-Potty caps movement; **end 17.50, no crossing** | 2 |
| 23 | P1 R17 | 19 / 35 | FU-008:4, FU-010:2, EV-009:4, FU-013:3, GE-013:6 | GE-019:5, TR-003:6 | None; maximum 23 | 2 |
| 23 | P2 R15 | 24 / 35 | FU-011:4, FU-006:3, FU-016:4, GE-015:5, TR-004:8 | GE-007:7, GE-001:7 | None; maximum 28 | 1 |
| 23 | P3 R14 | 19 / 35 | EV-029:2, EV-018:3, EV-020:5, EV-008:3, TR-014:6 | FU-009:7, EV-002:7 | None; maximum 24 | 2 |
| 23 | P4 R18 | 23 / 35 | EV-005:5, EV-028:3, FU-017:6, FU-021:3, TR-013:6 | EV-007:4, GE-003:4 | None; maximum 24 | 0 |
| 23 | P5 R14 | 24 / 35 | GE-010:4, FU-001:3, TR-017:4, FU-014:5, GE-016:8 | GE-017:5, TR-018:5 | None; maximum 26 | 2 |
| 23 | P6 R16 | 25 / 35 | EV-017:6, FU-004:4, EV-001:5, EV-010:6, GE-008:4 | TR-020:9, EV-014:4 | None; maximum 30 | 2 |
| 23 | P7 R16 | 29 / 35 | FU-002:5, FU-007:5, EV-019:7, EV-013:7, FU-019:5 | EV-004:6, FU-022:8 | None; maximum 32 | 2 |
| 23 | P8 R14 | 27 / 35 | EV-026:4, EV-030:5, GE-020:6, FU-012:6, TR-005:6 | TR-019:9, TR-008:8 | None; maximum 32 | 0 |

**Classification by checkpoint:**

- **Mile 10:** P1 is **RETENTION PLAUSIBLY WORTHWHILE**: it saves two actual Energy and preserves an Effort-8 card while still crossing, at a real 0.25-mile immediate cost. Finish-time advantage is not established. P2 and P3 are **RETENTION NOT WORTHWHILE as same-turn passes**: their threshold-reaching substitutions defer the crossing and give up 0.25 and 0.75 mile, respectively. Their next-turn outcomes are **INSUFFICIENT EVIDENCE**.
- **Mile 18:** P8 and P6 have **RETENTION NOT WORTHWHILE as same-turn passes**, because their passing swaps end short of Mile 18. P1, P2, P3, P4 and P5 are **PASS IMPOSSIBLE WITH ONE-CARD RETENTION CHANGE**. P2's actual loss was already zero, further weakening an Energy-only reason to retain.
- **Mile 23:** all eight are **PASS IMPOSSIBLE WITH ONE-CARD RETENTION CHANGE** at the crossing. P4 and P8 lost zero Energy due to the floor; P2 lost one, the others two. Earlier multi-turn hoarding or installed modifiers remains **INSUFFICIENT EVIDENCE**, not a demonstrated free pass.

## 8. Mile-23 structure

All eight Mile-23 hands contained five Race cards, with printed totals **19–29**, against threshold 35. The strongest was P7's 29; its immediate one-card substitution reaches at most 32. The maximum three available installed Gut modifiers together would be +4 (Strength +1, Mental Toughness +2, Pace Band +1), and even **29+4=33**. Thus no observed hand could pass on modifiers alone. A realistic pass would require a materially different retained hand **and possibly** specialist installation. A five-card hand averaging 7 printed Effort could theoretically reach 35; it is not an impossible rule threshold. The observed play gives no proof that assembling such a hand would preserve competitive Movement or that an installed build would repay its card-play cost.

**Run-04 interpretation:** Mile 23 acted as a **near-certain tax under the observed fast-play policy**, with a possible specialist-build reward untested. “Unreachable under ordinary optimal play” is not established from one trajectory. No threshold change is recommended.

## 9. AI valuation diagnosis

| Rejection | Diagnosis | Reason |
|---|---|---|
| P8 GPS Watch R6 | **AI PROBABLY CORRECT** | Three later observed compatible starts give zero quarter-miles, against a 0.25-mile cost. Other future cards could change thresholds. |
| P8 Intervals R1 | **AI PROBABLY CORRECT** | Later compatible Push produces zero distance; uncertain Energy preservation cannot demonstrate repayment of 0.50 mile. |
| P3 Carbon Racers R2 | **AI CORRECT** | Two remaining compatible future turns add 0.50 mile, below 1.25 lost. |
| P5 Tempo Shoes R4 | **AI CORRECT** | Four compatible later turns add zero distance, below 0.75 lost. |
| P6 Hill Repeats R7 | **AI VALUATION QUESTIONABLE**, not proven erroneous | Boundary effects repay the 0.25-mile loss by the next turn in a position-linked calculation; no observed advantage remains afterward and the R7 temporary gap matters. The six-segment mean Difficulty input does not explicitly represent this linked threshold payoff. |
| P6 Trail Shoes R2 | **INSUFFICIENT EVIDENCE** | Fixed future mile-14 gain equals upfront cost, but installation changes the deck/hand because this physical card was later played for Movement. |
| P3 Base Miles / Long Run; P7 Mental Toughness; P4 Pace Band; P8 Strength; P2 Downhill Practice; P7 Anti-Chafe | **AI CORRECT or PROBABLY CORRECT** for the named states | No recorded pass flip or sufficient threshold movement, or Energy preservation had no demonstrated finish-time conversion. |
| P1 Mile-10 retention (Movement choice, not setup) | **AI VALUATION QUESTIONABLE** | A legal same-turn alternative saves two Energy for 0.25 mile lost. The resulting finish-time value is unresolved; the rationale does not expose that alternative's full comparative score. |

No case warrants **AI LIKELY UNDERVALUING FUTURE BENEFIT** on current evidence. The scorer samples at most six visible Course segments and discounts future setup value; the log exposes means, not a full numeric score decomposition. This is a targeted evaluator **question**, not grounds to change weights now.

## 10. Economy diagnosis

**Training:** The leading observed cause of noninstallation is immediate Movement opportunity cost, amplified by the high printed Effort of several setup cards and the two-play limit. Pace/terrain compatibility and Movement thresholds add substantial variance. Duration hurts Intervals, while Gut-only Mental Toughness fails to flip P7's observed checks. Hill Repeats is the exception worth deeper position-linked scrutiny. The data do not isolate “effect magnitude too small” from Course/Pace luck well enough to rank it over opportunity cost.

**Gear:** The same immediate card-play/printed-Effort cost dominates the observed rejections. Carbon Racers and Tempo Shoes were Pace-compatible but too short-lived or ineffective at their actual Movement thresholds. GPS Watch was compatible three later times but gained no recorded quarter. Trail Shoes has a plausible later threshold gain, countered by physical-card circulation changes. Footwear/slot restrictions were not the cause of these named legal rejections. AI future-value discounting is a secondary question, not an established primary cause.

The common pattern is **Movement conversion and timing**, not an assumption that +1 or +2 Effort must be weak or that low installation frequency proves a rule defect. One selected Trail Training shows a persistent effect can earn meaningful marginal distance when setup does not delay the turn.

## 11. Smallest evidence-supported candidates

These are **investigations, not proposed implemented changes**:

1. **Position-linked setup evaluation check:** Recalculate P6 Hill Repeats R7/R8 and similarly small-cost terrain candidates with start-position carryover, while holding only visible cards/Pace fixed. Problem: a six-segment mean Difficulty may hide a next-boundary payoff. Benefit: separate a real AI valuation issue from a correct position preference. Risk of any later scoring change: overcrediting counterfactual turns or hidden future draws.
2. **Threshold-aware Gear check:** For GPS Watch and Trail Shoes, record legal future compatible starts *and* the quarter-mile threshold gain, including Course boundaries and physical-card collisions. Problem: mean Effort ignores threshold and circulation. Benefit: avoids both unjustified installation and unjustified dismissal. Risk: assigning knowledge of unseen future cards to the AI.
3. **Gut Check retention comparison:** Compare P1's legal Mile-10 card swap with the selected turn using actual two-Energy saved, 0.25 mile lost, potential Pack/position impact, and future hand consequences. For Mile 18/23, distinguish same-turn pass from deferring the checkpoint. Risk of later policy change: hoarding high cards could sacrifice much more Movement than the check saves.

No card-value, Pace, threshold, action-budget, Pack, or AI-weight change is supported directly by these calculations.

## 12. What Run 05 should test

If a future Run 05 is authorized, pre-register **one** hypothesis and keep the baseline comparison controlled:

1. Capture each setup plan's immediate miles, first compatible activation, actual quarter-mile gained, physical-card reuse conflict, and position-linked payback round. Include Hill Repeats, GPS Watch, Trail Shoes, Intervals, Carbon Racers and Tempo Shoes.
2. At each Gut Check, record the best legal *same-turn crossing* retention alternative and its actual movement, Energy and finish-position consequences; separately flag a deferred crossing.
3. Distinguish gross Effort/Difficulty benefits from converted miles and effective Energy saved. Keep paired source/rule/data checksums and compare against Run 04 only after the future design choice is explicitly approved.

This report does **not** perform Run 05 or recommend a broad rebalance.

## Evidence limitations

The named strategy-audit Markdown file was unavailable, so its prior prose findings were cross-checked against Run 04 rather than read as a second saved source. Fixed future states are sensitivity checks and can conflict with an equipped card's later observed Movement use. Position-linked calculations hold future cards, Pace and opponent actions fixed solely to isolate a local threshold effect. Event effects and the checkpoint are accounted for in immediate Gut swaps, but changed later draws and strategy are unknowable without another race, which was prohibited here.
