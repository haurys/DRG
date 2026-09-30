# DRG Rules — Simulation Baseline

## Authority

See [`DRG-Canonical-Playtest-Rules.md`](../DRG-Canonical-Playtest-Rules.md). The 2026-09-30 frozen `RaceCards.docx` table and explicit redesign rulings govern the Race-card inventory and Effects; the explicit rulings resolve table ambiguity. The Course and unchanged race rules retain their existing authority.

## Encoded

- Seven-card concealed starting hands; Conditions auto-enter play by Severity and draw replacement cards.
- Up to three pre-race exchanges; replacements/acquired cards lock.
- At most two cards per runner-turn and one Event.
- Non-Condition card MOVEMENT mode uses printed Effort and pays per-card Energy by Effort band: 1–3→0, 4–6→1, 7+→2.
- Non-Condition card EFFECT mode uses no Effort and pays no card Movement Energy; Training/Gear/Fuel use Treat/Prepare, Events use Movement.
- Pace icons: `▷`, `▶`, `▶▶`, `▶▶▶`; Movement is `→`; Energy is `⚡`.
- Pace Energy costs and starting Energy 15 remain unchanged.
- Deterministic visible Course, quarter-mile state, Difficulty boundary recalculation, Gut Checks, Pack preservation, Will, and simultaneous same-round Finish remain.

## Source discrepancy report

| Source | Date/version | Used for | Conflict/resolution |
|---|---|---|---|
| Simulation Foundation request | 2026-09-24 | Current setup, pace, layouts, movement table, audit requirements | Highest authority for this package. |
| CARDS.docx | 2026-08-28 | 108-card Race inventory; 30 Course cards | Describes Training/Gear as persistent and embeds Energy-like values in Effect. Inventory retained; only unambiguous standalone recovery is normalized to signed Energy. |
| Course Graphic Descriptions (1) | 2026-08-28 | Course titles/taxonomy | Uses some Country language; later project decision prefers Rural. Structured data uses Rural. |
| Earlier project discussions | Aug–Sep 2026 | Pack, draw, Will, course and component concepts | Used only where restated by current request or not contradicted. |

No newer standalone DRG rules or card-inventory file was found in the current project folder.
