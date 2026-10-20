# v1.4 Gameplay Validation Checklist

## What this document is

The hard pre-study gate for the existing uncommitted v1.4 candidate after the narrow Course/Gear/Nausea/action-budget remediation.

## How to use it

Read the evidence and blockers before deciding whether a separately authorized study may run. Bounded tests establish rule fidelity, not card balance or physical print quality.

## Key takeaways

The source and documentation now distinguish a two-mile physical Course card from its one-mile side records. Footwear and action budgets are explicit. All 192 tests pass; no study was run.

| Check | State | Evidence / reason |
|---|---|---|
| Required refs and pre-existing candidate | **PASS** | HEAD/main/origin/main/v1.3.2 tag all a6603183974311d8f1686582c5a1c9fff10c93bd; initial working tree contained only known candidate and preserved audit temp. |
| Physical Course card = 2 total miles | **PASS** | Canonical Course rules, 30-card inventory, paired-lane list and course mapping agree. |
| Side/data record = 1 mile | **PASS** | 60 JSON side records map to one-mile segments, four quarter-mile positions each. |
| Marathon = 13 connected cards, 26 miles | **PASS** | Bounded mapping test checks 13 unique IDs and 26 one-mile lanes paired outbound/return. |
| Start/Finish placement and direction | **PASS** | Documentation locates anchor at one end; bounded state/mapping test starts at mile 1 and returns to same selected physical card at mile 26. |
| Visible outbound/return and fixed milestones | **PASS** | Opposite sides of selected card map to outbound n/return 27−n; stations and Gut Checks unchanged. |
| Race/Course counts | **PASS** | 108 cards (20 Training, 20 Gear, 22 Fuel, 30 Event, 16 Condition); 30 physical Course cards, 60 sides; no Course values changed. |
| Fourteen current title edits | **PASS** | Six new Gear names plus eight prior candidate edits; data, title-keyed paths, canonical lists and 108-card ledger agree. |
| Mechanical Effect and printed values | **PASS** | All 108 IDs, effect_components, Effort, Movement Energy, Energy, Severity unchanged from v1.3.2. |
| Nausea printed/internal semantics | **PASS** | CO-012 prints `Cannot use Fuel`; bounded test blocks Fuel Effect but permits Effort-3 zero-Energy FU-001 Movement. |
| Footwear metadata and one-shoe rule | **PASS** | All 20 Gear carry is_footwear; six shoe IDs true, Running Socks false; replacement legality tested. |
| Broad categories have no equip rules | **PASS** | Engine checks is_footwear, never descriptive category; test changes a non-shoe category without changing legality. |
| One Treat/Prepare plus two-play budget | **PASS** | Live tests verify new-card Training/Gear/Fuel/treatment uses one of each; relocation and assistance use no new play. |
| Direct Slot Movement budget and delay | **PASS** | New and prior tests verify turn+2 eligibility, one card play, no Treat/Prepare, Effect removal before payment. |
| Hand, draw, deck zones and attachments | **PASS** | Six-card ceiling; single draw below it; recycling excludes slots/attachments; full removal discards attachments. |
| Will, DNF, Paces, assistance, target legality, Finish | **PASS** | Existing bounded and integrated suites pass; no numerical or rule change here. |
| Course coverage decision | **PASS** | All 60 sides mapped; Dirt/Grass/Rolling/technical footing flagged for observation without unapproved printed Effect changes. |
| New v1.4 remediation tests | **PASS** | 9/9 bounded tests; prior v1.4 candidate tests 15/15. |
| Applicable prior focused suites | **PASS** | 168/168 after title/metadata corrections. |
| Complete test suite | **PASS** | 192/192 with bytecode writes disabled. |
| git diff --check | **PASS** | No whitespace errors on final intended source/document changes. |
| Study/repository safety | **PASS** | No study, Formal Run, commit, tag or historical artifact edit; preserve both observed untracked audit temp files. |

## Gate rationale

The earlier v1.4 focused run stopped at a documentation assertion requiring the established phrase “Relocating already-played Gear.” The canonical rule was clarified without changing its meaning; the 192-test focused group and full suite then passed. The prior descriptive Gear-category mismatch is resolved through `is_footwear` and category alignment. The historical direct-Movement boundary-accounting issue remains RULES REVIEW and nonblocking. A future study requires separate authorization and an appropriate frozen baseline. This checklist did not run a seed.

AUTHORIZED FOR MULTI-SEED BALANCE STUDY
