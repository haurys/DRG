# DRG integrated playtest — source discovery and validation gate

Date: 2026-09-25. Status: **SIMULATION BLOCKER — no integrated race run**.

The 2026-09-25 master prompt and subsequent **DRG Supplemental Frozen Rules** have highest authority. Their explicit decisions supersede contradictory older documents and executable baseline behavior. This report does not alter the canonical card inventory, engine, configuration, or prior output; those files still represent the earlier simulation baseline and must not be mistaken for the frozen integrated ruleset.

## Source discovery

| Source inspected | Apparent date | Relevant material | Limitation |
|---|---|---|---|
| Master designer prompt | 2026-09-25 | Round structure, Event architecture and effects, Pace, Pack, Will, Gut Checks, Finish, pre-race, movement, card budget | Supersedes the old foundation. |
| Supplemental Frozen Rules | 2026-09-25, subsequent | Condition Base Severity and persistence, Training and Gear lifecycles, Fuel recovery/remedies, Pack, Will, Gut Check | Five new Gear designs lack printed Effort; several Condition penalties say only “Severity applies,” without identifying the quantity modified. |
| `DRG-Simulation/rules`, `data`, `simulation`, `engine`, `tests`, `audit`, `output` | 2026-09-24 to 2026-09-25 | 108 physical Race cards; 30 physical Course cards / 60 sides; seed 20260924; movement boundary tests; Phase 2A audit | Earlier baseline; does not implement the frozen integrated rules. No later integrated foundation was found. |
| `CARDS.docx` | Library upload 2026-08-28 | Race and Course inventory; Condition consequence and Treat numbers; Training/Gear/Fuel/Event printed texts | No separate Energy column; no Severity fields or per-card lifecycle classifications. Older Event texts and names are superseded where the prompt explicitly changes them. |
| `DRG_Initial_Course_Deck_Graphic_Descriptions(1).md` | 2026-08-28 | Course titles and environment terminology | Graphic-description source, not an integrated mechanics specification. |
| Phase 2A Race-card audit and Rules Review | 2026-09-25 | 89 design / 108 copy mapping, missing Energy and effect-execution gaps | Historical findings; several are now resolved by the current prompt, while other gaps remain. |
| Prototype artwork | August 2026 | Visual corroboration of individual card anatomy/name | Below the prompt and written inventory in source authority; not a complete current ruleset. |

The available Library DRG folder has the foundation ZIP, `CARDS.docx`, Course description Markdown, and prototype images, but no newer integrated canonical rules file. The supplemental designer message supplies current definitions that override older sources. Earlier discussions retrieved as context contain obsolete proposals and cannot establish the remaining missing values.

## Data checks

- Old inventory copies: Training 20, Gear 20, Fuel 22, Event 30, Condition 16; total **108**. The supplemental Gear distribution also totals **20**, but its five newly named designs have no Effort values.
- Course: **30** physical cards, **60** one-mile sides.
- The current JSON retains 30 Events but has obsolete `Pace Buddy`, `Goose Chase`, `Wrong Playlist`, Perfect Rhythm Effort 8/effect `+2 Pace Effort`, and Porta-Potty `Stop; +2 Energy`. The prompt explicitly supersedes all five records/behaviors. These are identified conflicts, not open design questions.
- The current JSON has `energy: null` for many designs. This is not zero. The new Event architecture defines their effects independently of the old Effort-or-Energy/Effect mode, but it does not establish missing printed Energy fields for Training/Gear or Salt Tabs.
- The existing 25 unit tests pass, including 18 boundary cases, but assert the old executable rules. This is **not** a passing integrated validation gate. No new integrated validation test or full marathon was run.

## Resolved by supplemental freeze

The supplement now explicitly provides all 12 Condition Base Severities and persistence states, named Gear suppression amounts, Training duration for the Temporary cards, Fuel recovery values, three separate Training/Equipped Gear slots, Pack preservation, Will, Gut Checks, Water +1, and Aid +2. The earlier report's broad absence claims for these areas are **superseded**, not still-open blockers. Training's Downhill Practice/Downhill Training and Strength Training/Strength names, and several Gear/Fuel display names, need an explicit alias mapping in canonical data, but their effects are now known where stated.

## Remaining simulation blockers — exact designer inputs required

1. **Printed Effort for five new Gear designs.** The current 20-copy distribution replaces five duplicate copies with `Cushioned Shoes`, `Tempo Shoes`, `Carbon Racers`, `Lightweight Singlet`, and `Recovery Sleeves`. None occurs in the old 20-card Gear inventory, and the supplement gives none a printed Effort value. Their Effort cannot be inferred from effects, names, or nearby Gear cards. The 108-card canonical Race deck and legal Movement/Gut Check options cannot be constructed without these five values. `RULES REVIEW` and **SIMULATION BLOCKER**.
2. **Meaning of “Severity applies.”** For Hot Spot, Side Stitch, Sore Feet, and Dead Legs, the supplement supplies Base Severity and an activation condition but does not say what the numeric Effective Severity modifies: Effort, Difficulty, Movement, or another quantity. The older printed texts describe a fixed `-1 Effort` or `+1 Difficulty`, which cannot be silently combined with the new Severity model. Exact behavior at partial treatment and at Effective Severity 0 is therefore not executable. `RULES REVIEW` and **SIMULATION BLOCKER**.
3. **Remedy effect on Severity.** Water, Aid, Electrolytes, and Salt Tabs may “remedy” named Conditions, but neither prompt states whether this sets Current Severity to 0, reduces it by a defined amount, discards a nonpersistent Condition outright, or otherwise modifies it. The persistent-at-zero rule does not define the amount of a remedy. This affects the legal state after milestones and Fuel consumption. `RULES REVIEW` and **SIMULATION BLOCKER**.

These are **SIMULATION BLOCKERS**, not silent PLAYTEST ASSUMPTIONS. The designer explicitly directs the current definitions and forbids inventing missing card values or rules. A race that ignores these cards/penalties or defaults a missing Effort to zero would not be a legitimate integrated playtest.

## Other RULES REVIEW and potential playtest assumptions

- **RULES REVIEW:** Tough Decision if fewer than two other cards remain after Movement; mandatory effect has no specified failure/legality resolution. An AI can avoid that play, but legal player actions still need definition before complete Event validation.
- **RULES REVIEW:** Sudden Rain and Tight Turn placement if no full Course mile remains ahead, and duration/stacking when multiple Course modifiers affect one mile.
- **RULES REVIEW:** High Five's `nearby` range and whether/when a runner at Finish can receive delayed Energy; Helpful Runner's legal recipient/transfer timing when no recipient is available.
- **RULES REVIEW:** Pack consent/formation ordering within the simultaneous Round Start when more than one compatible grouping is possible, and the precise voluntary-stop declaration timing.
- **PLAYTEST ASSUMPTION candidate (configurable):** discard recycling/deck exhaustion. The old engine shuffles discards into the deck; this remains an assumption unless a newer rule is supplied.
- **PLAYTEST ASSUMPTION candidate (configurable):** deterministic AI valuations and tie-breaking for trades, card decisions, targets, Gut Check card choice, and voluntary Pack stops. These are policy, not player powers or canonical rules.

## Superseded executable dependencies found

`engine/simulate.py` still selects Pace during individual turns; draws one each turn; offers zero-card turns; uses Effort OR Energy/Effect for Events; ignores almost all card/Condition/milestone effects; auto-forms Packs at exact position with no benefit; caps Conditions at three and discards overflow; assigns finish by seat-order arrival at 26.0 without the 0.2 extension or same-round tiebreak. `simulation/config.json` records those assumptions. These are **DEFECTS relative to the frozen prompt**, not canonical current rules. They were not changed because the integrated gate is blocked by missing authoritative card definitions.

## Gate result and next input

- Integration: **FAIL** (not implemented; blocked at source reconciliation).
- Validation: **FAIL** for the integrated rules; legacy baseline tests **25/25 pass** only for the old engine.
- Simulation: **BLOCKED**. No new seed, finish order, playtest metrics, or hashes exist.
- Determinism: **not evaluated for integrated rules**. The old engine's deterministic test passes, which does not establish integrated determinism.
- Balance: no changes and no conclusions.

Minimum input: provide the five new Gear printed Effort values; specify what Effective Severity numerically modifies for Hot Spot, Side Stitch, Sore Feet, and Dead Legs (including partial treatment); and specify the exact Severity/removal effect of each named remedy. Then update the rules/data/engine, add the specified integration tests, and run exactly one seeded eight-runner marathon.

Unmodified baseline SHA-256: `data/race_cards.json` `abe3330610c4803598d20f6ef3cc97b3653aa569ad4a504e54f9733515dc8f13`; `engine/simulate.py` `c72be8e30e24759b62c9be01fc1a64c260417e5657ad082bfa5e73ec8e66fa0d`; `simulation/config.json` `bdde079628600d3e01feabd567f7e7a467ed94f056cb6c9997a2422c87cf31ef`.
