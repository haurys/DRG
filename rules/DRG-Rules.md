# DRG Rules — Simulation Baseline

## Authority

1. The 2026-09-24 Simulation Foundation specification supplied by the designer.
2. `CARDS.docx` (2026-08-28) for Race inventory and numeric Course data.
3. `DRG_Initial_Course_Deck_Graphic_Descriptions(1).md` (2026-08-28) for normalized Course naming and setting language.

Later explicit decisions override older discussion. Unknown rules are not canonicalized.

## Encoded

- Seven-card concealed starting hands; Conditions excluded from setup deal.
- Up to three pre-race exchanges; replacements/acquired cards lock.
- Draw one and voluntarily play zero to two cards each turn.
- Effort Mode ignores Energy/Effect. Energy/Effect Mode ignores Effort.
- Drawn Conditions become active and trigger a replacement draw.
- Shared Easy/Steady/Race/Push Pace; Turn 1 lock; redeclare from Turn 2.
- Randomized, oriented visible Course; quarter-mile state.
- Fixed race-position milestones.
- Deterministic seeded randomness and chronological events.
- Movement Model A: one or two Effort-mode cards; Difficulty subtracted once; quarter-mile conversion; stop at each Difficulty boundary, carry positive excess, and adjust by the Difficulty difference; two-mile turn cap.

## Source discrepancy report

| Source | Date/version | Used for | Conflict/resolution |
|---|---|---|---|
| Simulation Foundation request | 2026-09-24 | Current setup, pace, layouts, movement table, audit requirements | Highest authority for this package. |
| CARDS.docx | 2026-08-28 | 108-card Race inventory; 30 Course cards | Describes Training/Gear as persistent and embeds Energy-like values in Effect. Inventory retained; only unambiguous standalone recovery is normalized to signed Energy. |
| Course Graphic Descriptions (1) | 2026-08-28 | Course titles/taxonomy | Uses some Country language; later project decision prefers Rural. Structured data uses Rural. |
| Earlier project discussions | Aug–Sep 2026 | Pack, draw, Will, course and component concepts | Used only where restated by current request or not contradicted. |

No newer standalone DRG rules or card-inventory file was found in the current project folder.
