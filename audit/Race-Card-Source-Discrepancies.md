# DRG Phase 2A — Source Discrepancies

## Authority order used

1. Most recent explicit designer decisions (2026-09-23 through 2026-09-25).
2. Current Foundation data/specification, version 1.
3. `CARDS.docx` (2026-08-28).
4. Prototype artwork and older discussions.

## Discrepancies

| ID | Card/system | Field | Source A | Source B | Assessment |
|---|---|---|---|---|---|
| SD-001 | Entire deck | Energy placement | `CARDS.docx` places lightning notation in Effect/Played Effect cells and has no Energy column. | Later explicit anatomy requires a separate signed Energy field below Effort. | Newer anatomy controls. Standalone signed entries plus three Electrolytes leading signed values establish 28 values; all other printed Energy values remain null. |
| SD-002 | Training/Gear | Persistence | `CARDS.docx` says Training should generally persist and Gear generally occupies one of three Preparation slots. | Current simulator implements neither persistence nor Preparation slots. | RULES REVIEW. Source wording is incomplete and simulator behavior is not canonical. |
| SD-003 | Events | Timing | `CARDS.docx` says Events primarily Play or React. | Current preferred architecture says Events normally enter hand and are voluntarily played; simulator has no reaction system. | RULES REVIEW for React classification and timing. |
| SD-004 | Conditions | Maximum/overflow | Simulator configuration caps active Conditions at three and discards overflow. | No inspected canonical source establishes that maximum or overflow behavior. | Simulator-only assumption; RULES REVIEW. |
| SD-005 | Conditions | Data structure | `CARDS.docx` separates consequence and Treatment columns. | Current JSON concatenates both into `effect_text`. | Structural discrepancy; no canonical data changed in this audit. |
| SD-006 | Tempo Run | Effort/Effect | Older prototype artwork extraction shows an apparent `11` and Race-Pace `+2 Effort`. | `CARDS.docx` and current data use Effort 6 and `Steady +1 Effort`. | Objectively resolved in favor of later `CARDS.docx`; artwork is obsolete prototype evidence. |
| SD-007 | Goose Chase | Title | Prototype card-image extraction reads `Wild Goose Chase`. | `CARDS.docx` and current data use `Goose Chase`. | Same-period artifact conflict; title alignment remains COSMETIC RULES REVIEW. |
| SD-008 | Footwear | Title/model | Prototype artifact extraction includes `High Performance Shoes`. | Current inventory uses `Running Shoes`. | Insufficient evidence that artwork supersedes the inventory; COSMETIC RULES REVIEW. |
| SD-009 | Structured Effects | Semantics | Human-readable Effect text exists for 63 unique designs. | Every structured Effect field in current JSON is null; engine applies only selected signed Energy and ignores Effect text. | No executable semantics may be inferred. |

## Resolved without design interpretation

- Family totals and physical quantities reconcile.
- Current Effort values match the latest textual inventory and were not changed.
- Standalone `+N⚡` notation is Energy, not Effect, under the later explicit anatomy decision.
- Conditional, targeted, or environmental lightning references remain Effect text; they were not converted into printed Energy.
