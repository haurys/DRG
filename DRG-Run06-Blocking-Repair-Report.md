# DRG Run 06 blocking repair and Victory Directive verification

**Baseline:** `drg-race-card-redesign-v1.1` / `1924ea771eff85107bda67eaf3f5d3de26266050`
**Scope:** bounded fixtures and implementation repair. No marathon execution. No commit or tag.

## Preserved evidence

`DRG-Marathon-Audit-Run-06.md` and `output/Run-06/` were not edited. The interrupted attempt remains seed `20260930`, 17 complete rounds, 139 complete turns, and no finishers. Its last event is EV-002927 (P4's round-18 Replenish).

## P4 round 18: actual legality and root cause

| Field | Recorded state after EV-002927 |
|---|---|
| Runner / position | P4 Course Planner; 38 quarter-mile spaces (9.5 miles) |
| Energy / Pace / maximum | 0 / Easy / Race |
| Hand | GE-008 Tech Shirt (Effort 4, cost 1); FU-005 Energy Chews (6, 1); FU-016 Electrolytes (4, 1); FU-017 Electrolytes (6, 1); FU-004 Energy Chews (4, 1); FU-007 Banana (5, 1); GE-018 Pace Band (6, 1) |
| Active Conditions | Nausea 4; Cold Chills 5; Dead Legs 5; Cramp 2; Gashed Knee 5 (Current/Effective Severity) |
| Installed | Strength Training TR-011; Pacing Practice TR-014; Running Shoes GE-002 |
| Pack / Will | no Pack / Will available |

Active Nausea prohibited every Fuel Effect, including Banana and Electrolytes. Tech Shirt and Pace Band were legal Gear preparation options, but each left only Movement cards costing at least 1 Energy. Neither Gear supplied immediate Energy on this Course/Pace. No Event was in hand, and no card had zero Movement cost. Will pays an unaffordable **Pace** cost, not a Movement-card cost. Easy Pace cost 0; changing Pace could not make a Movement card affordable. Thus there was no legal normal complete turn with a Movement card. The no-candidate fallback is a forced state, not evidence that the enumerator discarded an executable normal Movement plan. A no-card turn uses the engine's already existing forced fallback path; the canonical text says zero-card turns require an explicit override but does not define a new action for this case.

`choose_turn_plan()` correctly reached its no-candidate branch, but its fallback omitted `card_modes` and `movement_energy_cost`. `turn()` accessed `card_modes` while emitting AI_TURN_PLAN and raised `KeyError`. The fallback now includes empty `card_modes`, zero card cost, and every other field returned by a normal candidate. The P4 fixture executes through TURN_END with zero Movement and zero Energy. The change does not modify candidate enumeration, legality, or scoring.

## Audit serialization defect

`Sim.new_runner()` creates `runner['locked_ids']` as a Python `set`; setup adds exchanged card IDs to it. The separate Run 06 observer attempted to serialize `sim.runners` directly in its optional final-state export. `json.dumps()` rejected that set after the interrupted trace and metadata had already been saved. New `audit/run_output.py` makes a recursive audit-only copy and converts sets/frozensets to stable sorted lists. It leaves simulation state and event semantics unchanged. A regression test checks exact sorted IDs, repeatable JSON, and absence of mutation. The failed Run 06 output is preserved, not regenerated.

## Scoring terms reviewed

The existing `plan_score()` and `choose_pace()` implementation uses these terms. No weights changed.

| Term | Role in Victory Directive | Energy-conservation risk and proximity |
|---|---|---|
| Immediate Movement: `(12 + up to 2 for leader gap) × quarter-miles`; remaining distance `/8`; estimated turns `×0.15` | Direct progress and expected finish-time proxies; relative position raises progress weight | Primary score; favors progress over small Energy differences. |
| Positive legal Finish | `+1000` | Dominates reserve preferences; permits a 0-Energy finish. |
| Movement-card affordability; Pace preview/payment | Legal filter before scoring and actual projected Energy | Required sustainability; no standalone Pace-spending penalty beyond projected Energy. Will can cover Pace, never card cost. |
| Projected remaining Energy: `0.8 × first 5` plus `0.15 × excess`; 0-Energy penalty `4` while distance remains | Coarse future Movement sustainability proxy | It does reward reserve independently of an explicit future-turn simulation. Maximum reserve reward is 5.5, plus up to 4 avoiding the zero penalty. It is not distance-discounted before Finish. Bounded tests show it does not reverse a one-quarter clearly faster sustainable plan or the +1000 Finish result. Its strategic calibration remains a balance question, not a proven directive violation. |
| Energy Conservative profile: up to `1.5` from Energy | Profile preference, secondary to Movement | Independent reserve preference; not distance-discounted, but bounded below a one-quarter progress advantage. No profile definition changed. |
| Fuel recovery; Event Energy gain; installed Energy | Increase projected Energy, potentially funding future Movement | Fuel occupies a play and loses immediate Effort; recorded P1 round 5 Fuel funded a cost-1 Movement card from Energy 0. At full Energy a bounded Fuel fixture rejects recovery. No independent Fuel reward. |
| Training/Gear setup | Visible Effort, Difficulty, Pace preservation, installed/future Energy, Water/weather, resistance, Gut Check modifier; horizon `min(remaining,24)/24`, duration factor, setup penalty | Models future payoff against the immediate lost card play. Energy-related setup terms are horizon-discounted and decrease toward Finish. Existing opportunity-cost tests remain green. |
| Condition relief | Severity reduction and cap removal, discounted by remaining distance | Models restoration of legal Pace/Fuel or Movement, not pure reserve. |
| Pack | Preserves Pace Energy; Pack Runner profile `+0.4`; Pace chooser Pack proximity `+0.4` | May improve sustainable speed. Profile preference is small and separate; no broad Pack policy change. |
| Held hand Effort | At most `1.0`, scaled by remaining distance; Gut Check penalty predicted on crossing | Retains useful movement/Gut Check options; approaches zero at Finish. |
| Will expenditure | `-3` when consumed | Preserves a future Pace fallback; a legal faster Finish still dominates. |
| Aggressive/Front Runner Pace | `+0.55 × Pace index` | Secondary speed style. Course Planner training `+0.2`; Opportunist Event gain `+0.2`; Pack Runner `+0.4`. These are profile terms, not replacements for race objective. |

**Energy-related conclusions:** The residual-Energy and Energy Conservative bonuses represent coarse sustainability proxies, but are also independent reserve rewards. They do not explicitly taper in the final few miles. No tested deterministic fixture demonstrated that they could defeat a clearly faster sustainable line; one quarter of progress contributes at least 12 points before turn and position effects, versus at most 11 points from reserve/zero-energy/profile terms. The Finish bonus is 1000. Equivalent-progress plans may prefer Energy as the allowed secondary preference. Because no Victory Directive violation was established, no evaluator correction was made. This is a limited conclusion about the tested score comparisons, not proof over every possible combination of setup, Conditions, and profile state.

## Preserved Run 06 decisions

- **P1 round 1:** Energy 15; GE-016 + TR-019 both Movement; Effort 17, four card Energy, projected 2.00 miles, WIN_SPEED. A bounded first-turn reproduction still selects the exact plan.
- **P1 round 5:** Energy 0; FU-011 Water Bottle recovery plus EV-006 Movement; recovery permits the otherwise unaffordable cost-1 card and projects 0.75 mile. The recorded ENERGY_SUSTAINABILITY label is tied to progress, not simply the zero balance.
- **P4 round 14:** Energy 0; no positive legal alternative in the recorded AI decision; zero-Movement Strength Training replacement was selected. **P4 round 17:** no positive legal alternative; EV-008 Effect projected zero Movement. These do not establish a scoring preference for zero Movement over a legal positive line.
- **P4 round 18:** no normal candidate; fallback schema defect as above.

## Regression coverage and determinism

`tests/test_run06_repair.py` adds nine tests covering the exact P4 hand/Conditions and forced fallback execution; schema completeness and legal Fuel candidate survival; repeatable P4 and low-Energy turns; JSON-safe final-state export; faster sustainable score comparisons; zero-Energy Finish; Fuel/setup opportunity cost; speed-sensitive Pace selection; and the unchanged P1 round-1 plan. P4 and low-Energy fixtures repeat with identical selected plan, modes, Movement, Energy, score, rationale, and player event payloads. The final-segment fixture repeats with identical finish plan, Movement, Energy, and player events. These are bounded fixtures, not a marathon.

| Suite | Result |
|---|---:|
| New Run 06 regression / directive | 9/9 PASS |
| Frozen redesign | 20/20 PASS |
| AI legality | 8/8 PASS |
| AI rationale | 9/9 PASS |
| AI victory | 12/12 PASS |
| Full suite, including new tests | 129/129 PASS |

`git diff --check` passed. No Race Card data, Pace/Movement Energy cost, starting Energy, Course data, thresholds, rules, profiles, or balance values changed.

## Files in this repair

- `engine/simulate.py` — complete forced-fallback plan schema.
- `audit/run_output.py` — deterministic audit-only JSON conversion.
- `tests/test_run06_repair.py` — bounded regression and Victory Directive tests.
- `DRG-Run06-Blocking-Repair-Report.md` — this report.

The earlier `DRG-Marathon-Audit-Run-06.md` and `output/Run-06/` remain untracked, unchanged evidence. No commit was made.
