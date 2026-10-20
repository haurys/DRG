# v1.4 Candidate Implementation Report

## What this document is

A record of the uncommitted v1.4 candidate implementation, audit, validation, and repository boundary.

## How to use it

Review gameplay changes first, then the evidence and complete changed-file ledger. The eleven companion documents explain play and every physical card and Course side.

## Key takeaways

At baseline `a6603183974311d8f1686582c5a1c9fff10c93bd`, this candidate changes hand economy and legal slot liquidation without changing printed card effects or Course data. The post-remediation 192-test full suite passes. It has no commit or tag and has run no balance study or Formal Run.

## Baseline and scope

Repository: `/workspace/scratch/DRG-Balance-Study-v1.3.2`; branch `main`. The initial v1.4 task began with clean HEAD/main/origin/main/tag at `a6603183974311d8f1686582c5a1c9fff10c93bd`. At this remediation preflight those refs still matched while the known v1.4 candidate and one preserved audit temp file were already uncommitted. Earlier v1.3.1/v1.3/v1.2 tags remained at their prior SHAs. All work is uncommitted; origin/main and tags did not move.

## Implemented rulings

- **Hand and deck:** starting hand/maximum six rather than seven, no minimum, one normal draw when below maximum, replacement draw through revealed Conditions, eligible-discard recycle when draw empty, and skipped draw if neither pile contains an eligible card. Three pre-race exchanges persist.
- **Slots:** Training and normal equipped Gear carry installation runner-turn. Installing/replacing uses Treat/Prepare, old card discards, and new Effect begins immediately. Only after two complete runner turns may a card leave its normal slot directly for Movement. It never returns to hand or consumes Treat/Prepare; it consumes one of two card plays and pays printed Movement Energy. Remove persistent Effect before installed Energy, Pace/payment, Course and Condition calculation. AI preview/rationale model the same source removal. Temporary expiration and removal end eligibility.
- **Will:** unchanged exact legal Energy shortfall payment, now applicable to slot-derived card cost.
- **Attachments:** compatible Gear attached to a Condition remains outside the hand and equipped slots; cannot relocate or trade, does not qualify for Movement or DNF continuation, stays through partial treatment/persistent zero, and discards on complete Condition removal, including station/remedy. Preview mirrors removal.
- **DNF:** legal current or next-turn slot Movement joins established hand, recovery, draw, station and final assistance paths. Zero Energy and spent Will alone remain insufficient.
- **Event/audit:** existing targeted Event and assistance legality remain unchanged. `SLOT_SACRIFICE`, play source, plan sources, draw failure and `GEAR_DETACH` destination make v1.4 decisions auditable. Event schema describes fields.
- **Player count and Pace:** 4–12, preferably 6–8; Easy/Steady/Race/Push and their modifiers/costs remain unchanged. Fixed stations and Finish unchanged.

## Card and Course audit

108 physical Race cards: Training 20, Gear 20, Fuel 22, Event 30, Condition 16. Fourteen title-only physical copies changed: TR-013/014 Pacing Practice → Pace Practice; TR-015/016 Trail Training → Trail Runs; GE-001/002 Running Shoes → Road Trainers; GE-004 Cushioned Shoes → Cushion Trainers; GE-007 Tempo Shoes → Tempo Trainers; GE-006 Running Cap → All-Weather Cap; GE-009 Running Shorts → Split Shorts; GE-010 Sunglasses → Glare Shades; GE-013 Running Jacket → Weather Shell; GE-016 GPS Watch → Pace Watch; GE-020 Insoles → Support Insoles. Mechanical card Effect changes: **none**. Wording-only printed Effect text changes: **one**, CO-012 Nausea `No Fuel Allowed` → `Cannot use Fuel`, with unchanged Fuel Effect restriction and legal Fuel Movement. Duplicate diversification: **none**. Printed values, 30 Course cards, 60 sides, and fixed stations were not altered. The Course matrix flags Dirt (12), Grass (8), Rolling (18), Uneven (10), and rarer difficult surfaces for observation. Some route/elevation specialists already overlap; inventory frequency alone gives no observed Movement deficit or justified effect magnitude, so no Option C mechanic changed.

The prior descriptive Gear category conflict is **resolved**: GE-003 now Apparel (not footwear), GE-007 and GE-011 now Footwear, and all 20 Gear cards explicitly carry `is_footwear`. Only this boolean affects the existing one-shoe rule; broad categories add no mechanics. A historical direct-Movement boundary-accounting review item remains nonblocking and unchanged.

## Narrow remediation pass — decisions and evidence

- **Physical model:** 13 physical two-mile cards join long-side to long-side from Start/Finish for a full marathon. Each has a four-space outbound one-mile lane and an opposite four-space return lane. The existing engine already maps 13 selected card IDs to 26 one-mile side/data records (position 1 gives miles 1/26, position 13 gives 13/14). Canonical, format, Course, data inventory, and review documentation now distinguish physical cards from side records. Course numbers and station/Gut Check mileage did not change.
- **Titles:** six further title-only Gear changes are itemized above. All active card lists, title-keyed duration/watch logic, tests and review ledgers use the new names; historical reports were not edited. The legacy audit event key `GPS_WATCH_TICK` remains for GE-016 Pace Watch schema continuity.
- **Footwear:** explicit `is_footwear` replaces title membership for equipment legality, aligned with descriptive category on GE-003/007/011. Road Trainers (two cards), Cushion Trainers, Trail Shoes, Tempo Trainers and Carbon Racers count; Running Socks do not. No other category restriction exists.
- **Nausea:** CO-012 printed wording is exactly `Cannot use Fuel`. The pre-existing mechanical interpretation remains: Fuel EFFECT blocked while effective; otherwise legal Fuel MOVEMENT permitted with printed Effort/cost.
- **Treat/Prepare:** clarified one opportunity per turn, new hand card also uses one of two card plays, including installation/equipping, Fuel Effect, new-card treatment/attachment. Legal relocation and assistance use Treat/Prepare without a new card play. Direct Slot Movement uses a play without Treat/Prepare; existing live logic already enforced these budgets.
- **Course coverage:** Dirt 12 (five Trail-route) and Grass 8 (four Trail-route) merit specific later measurement. Gravel 2 overlaps inclines/one Trail; Brick 2 and Sand 1 overlap incline; Cobblestone 1 is Rolling. Rolling and uneven/technical footing have no dedicated printed specialist. General Effort/Pace/Will/Good Line remain possible; no measured v1.4 race outcomes establish a needed new effect. **No mechanical card Effect changed**, and no Course-side value changed.

## Validation and stop history

- Earlier candidate tests: **15/15 PASS**. New bounded `tests/test_v14_remediation.py`: **9/9 PASS**, covering title/data consistency, footwear/category semantics, Nausea modes, card/action budgets, and 13-card outbound/return pairing.
- First post-remediation focused group: **191/192 PASS**, with one canonical-document phrase assertion (`Relocating already-played Gear`) failing after prose was condensed. The phrase was restored without changing the rule. Resumed focused group: **192/192 PASS**.
- Applicable prior focused suites: **168/168 PASS**. Complete suite: **192/192 PASS** with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`.
- `git diff --check`: **PASS**. No balance or Formal Run seed executed. No commit or tag.

## Exact intended files changed or created

- `DRG-Canonical-Playtest-Rules.md`
- `DRG-Conditions.md`
- `DRG-Course-Rules.md`
- `DRG-Gear.md`
- `DRG-Race-Card-Simulation-Effect-Definitions.md`
- `DRG-Race-Cards.md`
- `DRG-Rules-Review.md`
- `DRG-Superseded-Rules.md`
- `DRG-Training.md`
- `DRG-v1.4-Annotated-Example-Race.md`
- `DRG-v1.4-Balance-Metrics-Specification.md`
- `DRG-v1.4-Candidate-Implementation-Report.md`
- `DRG-v1.4-Card-Economy-and-Zone-Model.md`
- `DRG-v1.4-Course-Card-List.md`
- `DRG-v1.4-Course-Interaction-Matrix.md`
- `DRG-v1.4-Executive-Gameplay-Summary.md`
- `DRG-v1.4-Gameplay-Rules-List.md`
- `DRG-v1.4-Gameplay-Validation-Checklist.md`
- `DRG-v1.4-Legality-and-Edge-Case-Matrix.md`
- `DRG-v1.4-Race-Card-Family-Lists.md`
- `DRG-v1.4-Turn-and-Action-Flow.md`
- `README.md`
- `data/Component-Manifest.md`
- `data/Course-Cards.md`
- `data/Race-Cards.md`
- `data/race_cards.json`
- `data/rules_config.json`
- `engine/ai_rationale.py`
- `engine/simulate.py`
- `rules/DRG-Rules.md`
- `rules/Race-Formats.md`
- `simulation/Simulation-Configuration.md`
- `simulation/Simulation-Decision-Rules.md`
- `simulation/Simulation-Event-Schema.md`
- `simulation/Simulation-State.md`
- `simulation/config.json`
- `tests/test_approved_baseline.py`
- `tests/test_final_rules.py`
- `tests/test_foundation.py`
- `tests/test_frozen_redesign.py`
- `tests/test_integrated_race_loop.py`
- `tests/test_run06_repair.py`
- `tests/test_v14_candidate.py`
- `tests/test_v14_remediation.py`

## Deliberately unchanged

No card Effort, Energy, Severity, mechanical Effect, count, AI scoring weight, profile identity, Course side data, Pace value, stations, player-count expansion, or Mulligan count was revised. The card-text and descriptive metadata corrections above are the only additional data edits. The pre-existing untracked audit temp file was present at remediation preflight and not touched. A second untracked audit temp file appeared during validation; it was not edited or removed by this task. Both remain outside intended changes. Historical v1.2/v1.3/v1.3.1 outputs and prior workspace were not modified. No commit or tag was created; a later study requires separate authorization.
