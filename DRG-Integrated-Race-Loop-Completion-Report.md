# DRG Integrated Race Loop Completion Report

Date: 2026-09-26  
Status: **READY FOR SINGLE DETERMINISTIC MARATHON AUDIT**  
Audited marathon runs performed in this pass: **0**

## 1. Race-loop execution map before changes

| Phase/system | Prior state |
|---|---|
| Setup, Course generation, pre-race exchanges | Connected |
| Replenish | Partial: unconditional draw, not draw-toward-seven |
| Pace selection/payment | Partial: no Condition caps, preservation, or Will |
| Pack | Grouping only; Energy preservation disabled |
| Treat/Prepare | Absent |
| Training/Gear/Fuel state | Absent or inert |
| Conditions | Draw and isolated numeric helpers only |
| Events | Four special cases; most mandatory effects bypassed |
| Effective Difficulty/boundaries | Installed elevation Training ignored |
| Gut Checks | Hand total worked; installed modifiers not supplied |
| Finish | Immediate at 26.0/13.0 with sequential ranking |
| Round-end simultaneous finish resolution | Absent |

## 2. Files changed

- `engine/simulate.py`
- `simulation/config.json`
- `simulation/Simulation-Decision-Rules.md`
- `tests/test_foundation.py`
- `tests/test_final_rules.py`
- `tests/test_integrated_race_loop.py` (new)
- `data/race_cards.json`
- `data/Race-Cards.md`
- `DRG-Canonical-Playtest-Rules.md`
- `README.md`
- `DRG-Integrated-Race-Loop-Completion-Report.md` (new)

Historical files under `output/` were not regenerated. Card artwork was not modified.

## 3. Integrated systems added

- Round Start Pace selection, legality caps, staged/global activation, and Pack snapshot.
- Voluntary Pack grouping policy with the canonical 0.5-mile leader limit and live 1-Energy Pace preservation.
- Replenish toward seven with a two-normal-card limit, immediate Condition placement, replacement chains, deterministic discard recycling, and in-play exclusions.
- Treat/Prepare actions for Training installation/replacement, Gear equip/attach/relocation, Fuel, named remedies, and point-for-point Condition treatment.
- Three Training slots; three normal Gear slots; one Footwear restriction; compatible attachments; temporary durations; attached-card effect isolation.
- Base/Current/Effective Severity, zero-severity suppression, rebound, persistent/nonpersistent removal, Anti-Chafe prevention, Fuel restrictions, Pace caps, and extra Pace costs.
- Pace payment after Treat/Prepare; Pack/Training/Gear preservation stacking; Condition/Event additions; Will fallback; unaffordable step-down without Will.
- All installed Training movement, preservation, elevation, and Gut Check effects.
- Gear movement, preservation, heat, Water, Gut Check, prevention, and suppression effects applicable to the current deck.
- All 30 Event slots by canonical timing: current, after Movement, staged OTHER, Course, and Global.
- Effective Difficulty recalculation at every boundary using installed Hill Repeats/Downhill Practice, Conditions, and Sudden Rain.
- Hand-Effort Gut Checks with Strength, Mental Toughness, and Pace Band.
- Positive-movement Finish extension beyond 26.0/13.0 and Round-End simultaneous placement.
- Finish tiebreaks: remaining-hand Effort, Energy, Will, then shared place.
- Round-End High Five awards, Pack cohesion, Course/Global expiry, and finish collection.

The stale EV-023/025/026/030 structured records were synchronized to already-frozen canonical entries. EV-023 is E10 with no extra effect; EV-025 is Wild Goose Chase; EV-026 uses the 0.5-mile cap plus after-Movement Energy; EV-030 is Untied Lace. This restored existing canonical values and effects; it did not introduce a new balance decision.

## 4. Event coverage matrix

| Event slots | Canonical timing/effect | Live path |
|---|---|---|
| EV-001–002 Headwind | OTHER, next round; Race/Push −1 Effort | Integrated staged target/lock/expiry |
| EV-003–004 Tailwind | Current; +1 Direct Movement | Integrated |
| EV-005 Sudden Rain | Course; next mile +1 Difficulty, four rounds | Integrated independent Course state/expiry |
| EV-006 Hot Spell | Global; next-round Push +1 Energy cost | Integrated activation/payment/expiry |
| EV-007 Cool Breeze | After Movement; +1 Energy | Integrated |
| EV-008 Sun Break | Current; Race/Push +1 Effort | Integrated |
| EV-009–010 Congestion | OTHER, next round; −1 Direct Movement | Integrated staged target/lock/expiry |
| EV-011–012 Potholes | OTHER, next round; Movement/Energy choice | Integrated; deterministic target policy logged |
| EV-013 Clear Road | Current; +1 Direct Movement | Integrated |
| EV-014 Good Line | Current; ignore Course Difficulty | Integrated |
| EV-015–016 Crowd Support | After Movement; +1 Energy | Integrated |
| EV-017 Tough Decision | After Movement; cycle up to two | Integrated with Condition replacement chains |
| EV-018 High Five | After Movement; Pack snapshot/self +1 Energy | Integrated at Round End to prevent seat advantage |
| EV-019 Friendly Rival | Current; Race/Push +1 Effort | Integrated |
| EV-020 Helpful Runner | After Movement; transfer self and +1 Energy | Integrated ownership/replay lock/circulation |
| EV-021–022 Second Wind | After Movement; +3 Energy | Integrated |
| EV-023 Perfect Rhythm | Printed E10 only | Integrated; no added effect |
| EV-024 Feeling Good | After Movement; +2 Energy | Integrated |
| EV-025 Wild Goose Chase | OTHER, next round; −1 Movement and +1 Pace cost | Integrated staged target/lock/expiry |
| EV-026 Porta-Potty | Current 0.5-mile cap; after +2 Energy | Integrated |
| EV-027 Dog Escort | Current; +1 Direct Movement | Integrated |
| EV-028 Funny Sign | After Movement; +1 Energy | Integrated |
| EV-029 Free Donut | After Movement; +1 Energy | Integrated |
| EV-030 Untied Lace | OTHER, next round; −1 Movement and no Pack preservation | Integrated staged target/lock/expiry |

Coverage registry: **30/30 physical Event IDs**.

## 5. End-to-end tests added

Eighteen bounded integration tests execute the real `Sim.turn()` / `run_round()` paths:

1. Replenish to seven, two-card limit, and Condition replacement chain.
2. Training installation + Pack preservation + Will + Event + boundary + Direct Movement in one live turn.
3. Pack versus solo Pace cost and Will fallback.
4. Heat-protection Gear and Hydration Belt milestone effect.
5. Gear suppression to Effective Severity zero and rebound after removal.
6. RR-11 Gear relocation simulator policy and card-play budget isolation.
7. Fuel remedy and Effort treatment in Treat/Prepare.
8. Live Gut Check using exact remaining hand, Mental Toughness, and Pace Band.
9. All 30 Event IDs classified in executable coverage.
10. Staged OTHER Event activation/expiry.
11. Course Event state.
12. Global Event activation/payment effect.
13. After-Movement Event Energy.
14. Helpful Runner ownership transfer and replay delay.
15. High Five Pack snapshot and timing-safe Round-End award.
16. Four live elevation-boundary transitions for Hill Repeats/Downhill Practice.
17. Live deck recycling with in-play exclusion.
18. Finish extension plus hand-Effort, Energy, Will, and exact shared tiebreak outcomes.

The prior determinism test was changed from two complete eight-runner marathons to two identical bounded two-runner rounds. This preserves deterministic verification without violating the no-marathon instruction.

## 6. Test results

- Focused rule/movement tests: **34/34 PASS**
- Live-loop integration tests: **18/18 PASS**
- Full suite: **59/59 PASS**
- Full-marathon simulations: **0**

## 7. Validation results

- Python compilation: PASS
- Python tab/indentation lint: PASS
- Archive build and integrity test: PASS
- JSON parsing: PASS (8 files)
- Race cards: 108
- Family counts: Training 20; Gear 20; Fuel 22; Event 30; Condition 16
- Duplicate Race IDs: 0
- Missing Race IDs: 0
- Course cards/sides: 30/60
- Duplicate Course-side IDs: 0
- Missing Course-side IDs: 0
- Course weighted Difficulty: 210
- Course mean Difficulty: 3.5
- Event Markdown/data title and Effort identity: 30/30
- Event executable coverage: 30/30

No dedicated external Python linter is configured in the project. Compilation, `tabnanny`, tests, semantic validation, and archive validation all pass.

## 8. PLAYTEST ASSUMPTIONS retained for non-blocking RR items

- **RR-11:** Gear relocation consumes the Treat/Prepare phase but zero new-card plays; this is simulator policy only.
- **RR-13:** virtual runners consent to the nearest legal same-Pace group within 0.5 mile of the leader; stable player ID resolves policy ties.
- **RR-16:** AI prioritizes an applicable named remedy; Electrolytes remedies Dehydrated when present; Salt Tabs remedies Cramp when present, otherwise a scripted legal Energy choice may be used.
- **RR-17:** a positive legal quarter-mile unit remaining at the Course endpoint is sufficient for the 0.2/0.1 Finish extension; endpoint arrival with no positive remainder does not finish.
- Potholes target policy: lose 1 Energy when possible; at zero Energy take −1 Movement.

These policies are documented only for deterministic simulation and do not resolve the physical-game questions permanently.

## 9. New read-only preflight findings

The actual live path now invokes:

- Will: PASS
- Pack preservation: PASS
- Treat/Prepare: PASS
- Training installation: PASS
- Gear equip/attach/relocation: PASS
- Fuel recovery/remedies: PASS
- Condition treatment: PASS
- Condition suppression/rebound: PASS
- Hill Repeats: PASS
- Downhill Practice: PASS
- Gut Check modifiers: PASS
- Mandatory Event effects: PASS, 30/30 IDs
- Finish extension: PASS
- Same-round tiebreak: PASS

## 10. Remaining blocking implementation mismatch

**None found.**

Historical simulation outputs remain intentionally stale and must not be treated as results from this engine version.

## 11. Readiness

**READY FOR SINGLE DETERMINISTIC MARATHON AUDIT**

The next authorized execution should run exactly one seed and generate a new full audit. Broader batch simulation remains unauthorized.
