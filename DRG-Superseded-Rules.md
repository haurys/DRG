# DRG superseded rules and source discrepancies

These historical concepts are **not current playtest rules**. Preserve older sources for provenance, but never use the following behaviors in a new integrated simulation. Highest authority: the 2026-09-25 master, supplemental, and consolidation designer freezes.

| Historical behavior/source | Current decision |
|---|---|
| Same-card/same-Pace **automatic** Pack, Pack timer/anchor/cooldown/hard-size cap/breakaway penalty; older foundation auto-forms exact-position groups with no benefit. | Voluntary consent, same Pace, direct ≤0.5 mile behind leader, preserve 1 Pace Energy; round-start decision/round-end cohesion. |
| Pace chosen independently during each runner turn or older Pace values. | Simultaneous Round Start selection; Easy +0/0, Steady +1/1, Race +2/1, Push +3/2. |
| Draw 1 each turn/end turn; automatic refill assumptions; Mulligan 3; maximum three Conditions/overflow discard. | Replenish toward seven, max two **normal** draws; Conditions replace, no cap; open trading and Deck Exchange up to three moves. |
| Generic Effort **OR** Energy/Effect mode for Events; Events in Treat/Prepare; Event effect sacrificed for Effort; activating on draw/hold/discard; two Events in Movement; proposed `Locked In` Event. | Event only in Movement, Effort **and** mandatory Effect, maximum one Event, no activation before/without play. `Locked In` not in current 30-slot deck. |
| EV-017 Pace Buddy / “Gain Pack +1,” and later exactly-two wording. | EV-017 Tough Decision E6 cycles up to two other hand cards after Movement, one normal replacement each. |
| EV-025 Goose Chase and old choose +1 movement/−1 Energy. | EV-025 Wild Goose Chase E8, OTHER staged: target next round −1 Movement **and** +1 Pace Energy cost. |
| EV-030 Wrong Playlist / Pace step change. | EV-030 Untied Lace E5, OTHER staged: target next round −1 Movement and no Pack Energy benefit. |
| Perfect Rhythm E8 with +2 Pace Effort or proposed Pace Energy preservation. | EV-023 Perfect Rhythm E10 with **no additional Effect**. |
| Porta-Potty unqualified `Stop; +2 Energy`. | EV-026 E4 contributes; max 0.5 mile this turn (PLAYTEST VALUE); gain 2 Energy **after** Movement. |
| Fixed-effect Condition `Treat N` without Base/Current/Effective Severity; max three active; older per-turn overflow. | Severity model and current per-card Base/persistence; unlimited active Conditions; printed older fixed penalties do **not** resolve “Severity applies” scaling. |
| Gear and Training share three Preparation slots, or assume all are persistent. | Separate three Training slots and three Equipped Gear slots; specified Temporary durations; attached Gear outside slots, one job per physical card. |
| Fuel and Event use same Either-Or family architecture; Energy gain on Movement Fuel; no distinction between Effect text and printed Energy. | Fuel Either-Or across Treat/Prepare versus Movement; Event Effort plus mandatory Effect. Separate printed Energy only if source independently verifies it. |
| Old Movement that subtracts full new segment Difficulty repeatedly, resets turn cap, or converts direct Movement into Effort. | Debit 2 integer result per quarter, carry positive remainder, adjust by **difference** in Difficulty, no cap reset; direct Movement after conversion. |
| Seat-order Finish tiebreak; instant victory at 26.0 miles. | Complete same round; 26.2/13.1 threshold; remaining-hand printed Effort, Energy, unspent Will, then shared place. |
| Older half Course six cards, or old automatic Pack/Will proposals. | Half uses seven cards, 13 active miles + 0.1 Finish; Pack/Will as frozen in main rules. |

## Card and Course source discrepancies requiring traceability

- `CARDS.docx`/legacy JSON: Running Cap → current Cap; Compression Sleeves → current Compression; Strength Training → Strength; Downhill Practice → Downhill Training; Energy Chews → Chews. Preserve source aliases, do not infer changed Effort for these matched variants.
- Gear: old duplicate Socks GE-004, Cap GE-007, Sunglasses GE-011, Anti-Chafe GE-015, GPS Watch GE-017 are superseded. Those IDs now belong respectively to Cushioned Shoes E6, Tempo Shoes E7, Carbon Racers E8, Lightweight Singlet E5, and Recovery Sleeves E5.
- Older Course aggregate 10/12/8/11/5/8/1/5 is superseded by the stored distribution 9/14/9/12/5/7/1/3.
- Tight Turn EV-014 is superseded by Good Line E4: ignore Course Difficulty this Movement.
- Event: old EV-017/023/025/026/030 data explicitly conflicts with newer designer decisions above. Current `data/race_cards.json` is not yet synchronized.
- Course: designer prompt states Difficulty distribution `10,12,8,11,5,8,1,5` for D1–D8 and “~3.6” average; existing 60-side JSON is `9,14,9,12,5,7,1,3` and mean 3.5. The prompt counts themselves imply 3.7. This is **RULES REVIEW**, not a balancing opportunity. The per-side values have not been changed.
- `CARDS.docx` has no separate signed Energy column. Its effect-area recovery/loss symbols cannot be silently copied into a universal printed-Energy field. Phase 2A `energy: null` findings remain data-accuracy warnings where no later explicit printed Energy decision exists.
