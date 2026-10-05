# DRG v1.3.1 — No-helper assistance reason repair

## Original baseline and event

The validated v1.3 baseline is `25b7fa9a019411eabe077acbeaba327eaf93b574` (`main` and `drg-race-card-redesign-v1.3`). Formal Run 06 v1.3 remains historical and unchanged. Its event `EV-006369`, round 50, P5 Pack Runner turn 50, emitted `ASSISTANCE_PARTNER_SELECT` with `helper: null`, `helper_position: null`, but `reason: second_place_if_leading`. P5 was the only eligible active runner. Event `EV-006372` correctly recorded `ASSISTANCE_FAIL` with `reason: no_eligible_active_helper`, and `EV-006380` recorded DNF at 23.0 miles.

## Root cause and correction

`Sim.request_assistance` used a nested reason expression that tested `position == 1` before checking whether a helper existed. With only P5 active, its position was 1, so the reason incorrectly reported the second-place policy despite `helper is None`. The reason is an event payload field. The actual helper selection, swap enumeration, hand transfer, assistance failure, and DNF evaluation use the helper object and did not read that reason value. The v1.3 race state and outcome were unaffected.

The repair changes only the reason expression: check `helper is None` first and emit `no_eligible_active_helper`; otherwise retain `second_place_if_leading` or `current_leader` as before. No eligibility, scoring, action cost, DNF, or gameplay logic changed. Historical Formal Run 06 reports and outputs were not edited.

## Regression

`tests/test_no_helper_reason.py` reproduces P5's round-50 no-helper situation with the recorded seven-card hand, 23.0-mile position, zero Energy, spent Will, and active Cramp and Nausea. It verifies the no-helper branch, corrected reason, absence of a swap, unchanged hand/Energy/position/Will/Conditions and helper state, the existing requester Treat action cost, intended DNF evaluation and retained state, and identical event results in two bounded fixtures. New focused test: 1/1 PASS.

## Validation

- `git diff --check`: PASS.
- v1.3 cleanup tests: 13/13 PASS.
- Run 06 repair: 10/10 PASS.
- Will/closed rules: 13/13 PASS.
- Frozen redesign: 20/20 PASS.
- AI legality: 8/8 PASS.
- AI rationale: 9/9 PASS.
- AI Victory: 12/12 PASS.
- Movement boundaries: 18/18 PASS.
- Integrated race loop: 18/18 PASS.
- Complete suite: 157/157 PASS.

## Files changed

- `engine/simulate.py` — event reason-label expression only.
- `tests/test_no_helper_reason.py` — bounded deterministic regression.
- `DRG-v1.3-No-Helper-Reason-Repair-Report.md` — this repair record.

No Formal Run 06 rerun or balance study was performed.
