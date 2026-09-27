# DRG Phase 2A — Race Card Energy & Effect Audit

## Audit conclusion

**C — SUBSTANTIAL RULES REVIEW REQUIRED BEFORE IMPLEMENTATION**

The physical inventory, unique IDs, quantities, families, titles, and Effort values reconcile. Separate Energy data is complete for only 28 of 108 physical cards. No card Effect currently has structured executable semantics.

## Sources inspected

- Current `DRG-Simulation-Foundation.zip`, version 1.
- `CARDS.docx`, dated 2026-08-28.
- `data/Race-Cards.md` and `data/race_cards.json`.
- `rules/DRG-Rules.md` and `rules/Rules-Review.md`.
- Simulation configuration, decision rules, event schema, engine, and tests.
- Available DRG card artwork and extracted text, including Tempo Run, Friendly Rival, Hydration Belt, Banana, Cramp, and generic card-image artifacts.
- Most recent explicit DRG decisions: separate Effort/Energy/Effect anatomy; mutually exclusive Effort and Energy/Effect modes; Conditions auto-place and replace-draw.

## Verified inventory

| Family | Physical cards | Unique designs |
|---|---:|---:|
| Training | 20 | 12 |
| Gear | 20 | 13 |
| Fuel | 22 | 22 |
| Event | 30 | 30 |
| Condition | 16 | 12 |
| **Total** | **108** | **89** |

A unique design is defined by family, title, Effort, Energy entry, and source Effect text. Identically printed duplicates consolidate into one row; different-Effort copies remain separate designs.

## Energy completeness

`CARDS.docx` does not provide a separate Energy column. Under the later canonical anatomy decision, standalone signed lightning entries—and a signed leading value clearly separable from remaining Effect text—can be separated from Effect text. Conditional or targeted lightning references remain Effects and are not converted into the card’s printed Energy value.

| Energy state | Physical cards | Unique designs |
|---|---:|---:|
| positive | 28 | 28 |
| zero | 0 | 0 |
| negative | 0 | 0 |
| explicitly no Energy | 0 | 0 |
| unknown/null | 80 | 61 |

### Energy distribution by family

| Family | Positive physical/designs | Unknown physical/designs |
|---|---:|---:|
| Training | 0/0 | 20/12 |
| Gear | 0/0 | 20/13 |
| Fuel | 20/20 | 2/2 |
| Event | 8/8 | 22/22 |
| Condition | 0/0 | 16/12 |

No explicit zero or negative printed Energy values were established. Negative lightning references occur inside conditional/targeted Effect text and were not reclassified as printed Energy. The 28 known positive values include three Electrolytes designs where `+1 Energy` is separable from `Treat Dehydrated`.

## Effect completeness

| Effect state | Physical cards | Unique designs |
|---|---:|---:|
| No Effect after separating standalone Energy notation | 27 | 26 |
| Fully executable Effect | 0 | 0 |
| Partially executable Effect | 0 | 0 |
| Text-only Effect | 81 | 63 |
| Requires Rules Review | 83 | 64 |

Placement of a Condition and its replacement draw are executable system behavior, not execution of the Condition’s printed consequence. All structured Effect fields are null in the current card data.

## Execution status

Status counts overlap where appropriate.

| Status | Physical cards | Unique designs |
|---|---:|---:|
| READY | 25 | 25 |
| PARTIAL | 83 | 64 |
| TEXT ONLY | 81 | 63 |
| ENERGY MISSING | 80 | 61 |
| CONFLICT | 3 | 2 |
| RULES REVIEW | 83 | 64 |

The 25 READY designs are standalone positive-Energy cards with no additional Effect after Energy notation is separated. The three Electrolytes designs have known +1 Energy but retain unresolved `Treat Dehydrated` Effect text.

## Master audit table

| ID | Physical IDs | Title | Family | Qty | Effort | Energy | Effect Text | Current Execution | Status | Rules Review |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| RD-001 | TR-001, TR-002 | Long Run | Training | 2 | 7 | null | — | Effort Mode available. Energy/Effect Mode unavailable because energy is null. | ENERGY MISSING, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? |
| RD-002 | TR-003 | Base Miles | Training | 1 | 6 | null | Easy +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-003 | TR-004 | Negative Split | Training | 1 | 8 | null | Race +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-004 | TR-005, TR-006 | Tempo Run | Training | 2 | 6 | null | Steady +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-005 | TR-007, TR-008 | Intervals | Training | 2 | 8 | null | Push +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-006 | TR-009, TR-010 | Hill Repeats | Training | 2 | 7 | null | Incline +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-007 | TR-011, TR-012 | Strength Training | Training | 2 | 5 | null | Gut Check +1 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-008 | TR-013, TR-014 | Pacing Practice | Training | 2 | 6 | null | Steady +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-009 | TR-015, TR-016 | Trail Training | Training | 2 | 5 | null | Trail +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-010 | TR-017 | Form Drills | Training | 1 | 4 | null | Flat +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-011 | TR-018 | Downhill Practice | Training | 1 | 5 | null | Descent +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-012 | TR-019, TR-020 | Mental Toughness | Training | 2 | 9 | null | Gut Check +2 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-013 | GE-001, GE-002 | Running Shoes | Gear | 2 | 7 | null | Asphalt +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, CONFLICT, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-014 | GE-003, GE-004 | Running Socks | Gear | 2 | 4 | null | Blister Treat -2 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-015 | GE-005 | Trail Shoes | Gear | 1 | 7 | null | Trail +2 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-016 | GE-006, GE-007 | Running Cap | Gear | 2 | 5 | null | Heat effects -1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-017 | GE-008 | Tech Shirt | Gear | 1 | 4 | null | Heat effects -1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-018 | GE-009 | Running Shorts | Gear | 1 | 5 | null | Steady +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-019 | GE-010, GE-011 | Sunglasses | Gear | 2 | 4 | null | Sun effects ignored | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-020 | GE-012, GE-013 | Hydration Belt | Gear | 2 | 6 | null | Water +1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-021 | GE-014, GE-015 | Anti-Chafe | Gear | 2 | 5 | null | Ignore first Hot Spot | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-022 | GE-016, GE-017 | GPS Watch | Gear | 2 | 8 | null | Pace +1 Effort once/Round | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-023 | GE-018 | Pace Band | Gear | 1 | 6 | null | Gut Check +1 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-024 | GE-019 | Compression Sleeves | Gear | 1 | 5 | null | Cramp Treat -2 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-025 | GE-020 | Insoles | Gear | 1 | 6 | null | Concrete +1 Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-026 | FU-001 | Energy Gel | Fuel | 1 | 3 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-027 | FU-002 | Energy Gel | Fuel | 1 | 5 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-028 | FU-003 | Energy Gel | Fuel | 1 | 7 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-029 | FU-004 | Energy Chews | Fuel | 1 | 4 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-030 | FU-005 | Energy Chews | Fuel | 1 | 6 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-031 | FU-006 | Banana | Fuel | 1 | 3 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-032 | FU-007 | Banana | Fuel | 1 | 5 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-033 | FU-008 | Snack Bar | Fuel | 1 | 4 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-034 | FU-009 | Snack Bar | Fuel | 1 | 7 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-035 | FU-010 | Water Bottle | Fuel | 1 | 2 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-036 | FU-011 | Water Bottle | Fuel | 1 | 4 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-037 | FU-012 | Water Bottle | Fuel | 1 | 6 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-038 | FU-013 | Sports Drink | Fuel | 1 | 3 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-039 | FU-014 | Sports Drink | Fuel | 1 | 5 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-040 | FU-015 | Sports Drink | Fuel | 1 | 7 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-041 | FU-016 | Electrolytes | Fuel | 1 | 4 | 1 | Treat Dehydrated | Effort Mode available. Energy/Effect Mode applies +1 Energy. Effect text is not executed. | TEXT ONLY, PARTIAL, RULES REVIEW | What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-042 | FU-017 | Electrolytes | Fuel | 1 | 6 | 1 | Treat Dehydrated | Effort Mode available. Energy/Effect Mode applies +1 Energy. Effect text is not executed. | TEXT ONLY, PARTIAL, RULES REVIEW | What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-043 | FU-018 | Electrolytes | Fuel | 1 | 8 | 1 | Treat Dehydrated | Effort Mode available. Energy/Effect Mode applies +1 Energy. Effect text is not executed. | TEXT ONLY, PARTIAL, RULES REVIEW | What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-044 | FU-019 | Salt Tabs | Fuel | 1 | 5 | null | Treat Cramp | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-045 | FU-020 | Salt Tabs | Fuel | 1 | 7 | null | Treat Cramp | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-046 | FU-021 | Orange Slice | Fuel | 1 | 3 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-047 | FU-022 | Gummy Bears | Fuel | 1 | 8 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-048 | EV-001 | Headwind | Event | 1 | 5 | null | Target -1 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-049 | EV-002 | Headwind | Event | 1 | 7 | null | Target -1 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-050 | EV-003 | Tailwind | Event | 1 | 4 | null | +1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-051 | EV-004 | Tailwind | Event | 1 | 6 | null | +1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-052 | EV-005 | Sudden Rain | Event | 1 | 5 | null | +1 Difficulty next mile | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-053 | EV-006 | Hot Spell | Event | 1 | 6 | null | -1 Energy at Push | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-054 | EV-007 | Cool Breeze | Event | 1 | 4 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-055 | EV-008 | Sun Break | Event | 1 | 3 | null | +1 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-056 | EV-009 | Congestion | Event | 1 | 4 | null | Target -1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-057 | EV-010 | Congestion | Event | 1 | 6 | null | Target -1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-058 | EV-011 | Potholes | Event | 1 | 5 | null | Target chooses -1 movement or -1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-059 | EV-012 | Potholes | Event | 1 | 7 | null | Target chooses -1 movement or -1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-060 | EV-013 | Clear Road | Event | 1 | 7 | null | +1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-061 | EV-014 | Tight Turn | Event | 1 | 4 | null | -1 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-062 | EV-015 | Crowd Support | Event | 1 | 5 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-063 | EV-016 | Crowd Support | Event | 1 | 7 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-064 | EV-017 | Pace Buddy | Event | 1 | 6 | null | Gain Pack +1 | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-065 | EV-018 | High Five | Event | 1 | 3 | null | You + Nearby runner +1 Energy each | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-066 | EV-019 | Friendly Rival | Event | 1 | 7 | null | +1 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-067 | EV-020 | Helpful Runner | Event | 1 | 5 | null | Give card; +1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-068 | EV-021 | Second Wind | Event | 1 | 8 | 3 | — | Effort Mode available. Energy/Effect Mode applies +3 Energy. | READY | — |
| RD-069 | EV-022 | Second Wind | Event | 1 | 9 | 3 | — | Effort Mode available. Energy/Effect Mode applies +3 Energy. | READY | — |
| RD-070 | EV-023 | Perfect Rhythm | Event | 1 | 8 | null | +2 Pace Effort | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-071 | EV-024 | Feeling Good | Event | 1 | 6 | 2 | — | Effort Mode available. Energy/Effect Mode applies +2 Energy. | READY | — |
| RD-072 | EV-025 | Goose Chase | Event | 1 | 8 | null | Choose +1 movement or -1 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, CONFLICT, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-073 | EV-026 | Porta-Potty | Event | 1 | 4 | null | Stop; +2 Energy | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-074 | EV-027 | Dog Escort | Event | 1 | 6 | null | +1 movement | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-075 | EV-028 | Funny Sign | Event | 1 | 3 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-076 | EV-029 | Free Donut | Event | 1 | 2 | 1 | — | Effort Mode available. Energy/Effect Mode applies +1 Energy. | READY | — |
| RD-077 | EV-030 | Wrong Playlist | Event | 1 | 5 | null | Change Pace one step | Effort Mode available. Energy/Effect Mode unavailable because energy is null. Effect text is not executed. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? |
| RD-078 | CO-001, CO-002 | Cramp | Condition | 2 | null | null | Push unavailable; Treat 4 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-079 | CO-003 | Tight Calf | Condition | 1 | null | null | Push costs +1 Energy; Treat 3 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-080 | CO-004 | Dead Legs | Condition | 1 | null | null | Race/Push -1 Effort; Treat 5 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-081 | CO-005, CO-006 | Blister | Condition | 2 | null | null | Push costs +1 Energy; Treat 3 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-082 | CO-007, CO-008 | Hot Spot | Condition | 2 | null | null | Race/Push -1 Effort; Treat 2 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-083 | CO-009 | Sore Feet | Condition | 1 | null | null | Concrete/Asphalt +1 Difficulty; Treat 4 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-084 | CO-010, CO-011 | Dehydrated | Condition | 2 | null | null | Steady/Race/Push +1 Energy; Water or Treat 5 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-085 | CO-012 | Nausea | Condition | 1 | null | null | Fuel gives -1 Energy; Treat 4 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-086 | CO-013 | Stomach Trouble | Condition | 1 | null | null | Fuel unavailable; Aid or Treat 5 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-087 | CO-014 | Side Stitch | Condition | 1 | null | null | Race/Push -1 Effort; Treat 3 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-088 | CO-015 | Twisted Ankle | Condition | 1 | null | null | Maximum Pace: Steady; Aid or Treat 7 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |
| RD-089 | CO-016 | Heat Exhaustion | Condition | 1 | null | null | Maximum Pace: Easy; Aid or Treat 8 | Auto-places on draw and draws replacement; consequence/treatment not executed; simulator-only cap/overflow assumption applies. | ENERGY MISSING, TEXT ONLY, PARTIAL, RULES REVIEW | What signed Energy value is printed in the separate Energy field? What complete trigger, timing, target, duration, persistence, stacking, and removal semantics apply? How are consequence, treatment, stacking, duration, maximum-active, and overflow rules resolved? |

## Validation

- PASS — 108 physical IDs are present and unique.
- PASS — every physical ID maps to exactly one of 89 unique designs.
- PASS — family counts reconcile to 108.
- PASS — every unique design appears in the master table.
- PASS — no missing Energy value was converted to zero.
- PASS — no ambiguous Effect was converted into executable semantics.
- PASS — Effort values and canonical card data were not modified.
- PASS — engine, configuration, and tests were not modified.
- PASS — no simulation was run or regenerated.
