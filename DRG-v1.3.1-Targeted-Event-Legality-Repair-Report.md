# DRG v1.3.1 Targeted Event Legality Repair

## 1. Baseline

- Repository: `/workspace/scratch/c44187d30dd1/DRG-Formal-Run-06-v1.2-fresh`
- Branch: `main`
- Pre-repair HEAD, `main`, and `drg-race-card-redesign-v1.3.1`: `4cc7016e113f4f4c4ced6ead7e6ddbeaada18c18`
- Pre-repair tracked files: clean. Historical Run 06 reports and outputs and the balance-study outputs were untracked.

## 2–3. Preserved failure evidence and exact Event

Seed `20261001` completed. Seed `20261002` stopped during round 49, P8's runner turn 49. P1–P7 were `FINISHED`; P8 was `ACTIVE` at 18.5 miles and 0 Energy. Event `EV-006403 AI_TURN_PLAN` selected `EV-015` Crowd Support in `EFFECT` mode. Event `EV-006409 PLAY` recorded that play, immediately followed by the exception in `resolve_event_play`: `ValueError: Event requires another Runner`. The exception arose before the Event Effect could resolve. The seed's partial event log, trace, final-state snapshot, and `Simulation-Error.txt` are preserved.

## 4. Root cause

`movement_candidates` did check for a target before including target-required Effect plans. `choose_turn_plan` calls it with a deep-copied preview runner (`preview_preparation`); round-start Pace evaluation also uses a copy. `beneficial_target` and `event_target` excluded the source with `runner is not source`. A preview copy is a different Python object from its corresponding live runner, so P8 was incorrectly counted as an eligible *other* runner. The AI scored and selected the impossible Effect plan. The live resolver received the real P8 object, found no other active runner, and raised the exception. Thus candidate preview and live resolution disagreed; finished runners were not counted in the failing case. The invalid self-match was the cause.

## 5. Frozen legality ruling

A target-required Event Effect is legal only when an eligible other active runner exists. FINISHED, DNF, and finish-pending runners are excluded. High Five requires an eligible Pack member when the source is packed; when solo, it can choose another active runner. OTHER Target Lock remains in effect for its applicable Events. An Event card can still be used for Movement when that use is otherwise legal. The live resolver retains a defensive exception for an impossible direct Effect invocation.

## 6. Targeted Events audited

| IDs | Event | Required target and selection |
|---|---|---|
| EV-001, EV-002 | Headwind | Active unlocked other runner |
| EV-011, EV-012 | Potholes | Active unlocked other runner |
| EV-015, EV-016 | Crowd Support | Active other runner |
| EV-018 | High Five | Active other runner; current Pack member when packed |
| EV-019 | Friendly Rival | Active other runner; beneficial staged target |
| EV-020 | Helpful Runner | Active other runner |
| EV-025 | Wild Goose Chase | Active unlocked other runner |
| EV-030 | Untied Lace | Active unlocked other runner |

All other Event Effects in the 30-slot inventory are self, course, global, or otherwise do not require an additional runner. No Event data or Effect values changed.

## 7. Implementation

`engine/simulate.py` identifies the eleven target-required Event IDs and filters Effect-mode candidates through a shared eligible-target check. Target lookup now excludes the source by stable `player_id`, including when the source is a preview copy. High Five applies its Pack snapshot restriction when packed and selects an active other runner when solo. The live resolver uses the same eligibility check for missing required targets while retaining its explicit invalid-target and conditional Pack validations. Movement candidates are added before Effect eligibility is checked and remain available.

## 8. Regression tests

`tests/test_targeted_event_legality.py` adds 11 tests: active Crowd Support target and preview copy; all-finished P8 AI turn with Movement fallback and no exception; all-DNF and mixed inactive fields; exactly one active target; the full target-required inventory, including beneficial and negative Events; High Five Pack and solo eligibility; OTHER Target Lock; AI plan filtering; and defensive live resolution without state mutation.

## 9. Validation

- New focused suite: 11 tests passed.
- Existing requested focused suites (`test_v13_cleanup`, `test_no_helper_reason`, `test_ai_legality`, `test_ai_rationale`, `test_ai_victory`, `test_integrated_race_loop`): 61 tests passed.
- Complete test suite: 168 tests passed.
- `git diff --check`: passed.
- No marathon or balance-study seed was run during this repair.

## 10–12. Files, preserved artifacts, repository safety

Intended files changed or created: `engine/simulate.py`, `tests/test_targeted_event_legality.py`, and this report. The completed `output/Balance-Study-v1.3.1/20261001/` and interrupted `output/Balance-Study-v1.3.1/20261002/` directories were only read; they remain unchanged. Historical Run 06 artifacts were preserved. No commit or tag was created. The intended repair remains uncommitted.
