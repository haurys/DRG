# DRG Phase 2A — Race Card Rules Review

## BLOCKING

### RR-RACE-001 — Missing printed Energy values

**Affected:** 61 unique designs / 80 physical cards.

**Question:** What signed Energy value is printed in the separate Energy field for every unresolved card? Blank, null, absent, and zero must remain distinct.

**Evidence:** `CARDS.docx` has Effort and Effect columns but no separate Energy column. Later explicit decisions require Energy below Effort as an independent field.

### RR-RACE-002 — Training and Gear activation lifecycle

**Affected:** all Training and Gear Effects.

**Question:** Are these Effects immediate or persistent? If persistent, when do they enter play, how long do they last, how are they removed, may duplicates stack, and are the proposed three Preparation slots canonical?

**Evidence:** `CARDS.docx` says Training “should generally” persist and Gear “generally” occupies a Preparation slot. The conditional wording does not completely specify the rule, and the simulator does not implement it.

### RR-RACE-003 — Effect-mode timing and discard lifecycle

**Affected:** all 63 effect-bearing unique designs.

**Question:** When may Energy/Effect Mode be declared, when does the Effect resolve relative to movement/Pace/Conditions, and when is the card discarded or retained?

### RR-RACE-004 — Condition consequence lifecycle

**Affected:** all 12 Condition designs.

**Question:** When does each consequence begin, when is it checked, how long does it persist, and exactly when is it removed?

### RR-RACE-005 — Condition treatment semantics

**Affected:** every Condition plus Running Socks, Compression Sleeves, Electrolytes, and Salt Tabs.

**Question:** What does `Treat N` require, what resource/card value pays it, when may treatment occur, does treatment consume the treating card, and when is the Condition removed?

### RR-RACE-006 — Condition stacking, maximum, and overflow

**Affected:** all Conditions.

**Question:** May duplicate or different Conditions stack? Is there a maximum active count? If a maximum exists, what happens to an additional draw?

**Evidence:** the simulator uses “maximum three; discard excess” only as a documented playtest assumption. No canonical source establishes it.

### RR-RACE-007 — Pace Effort terminology and application

**Affected:** Base Miles, Negative Split, Tempo Run, Intervals, Pacing Practice, Running Shorts, GPS Watch, Headwind, Sun Break, Tight Turn, Friendly Rival, Perfect Rhythm, Dead Legs, Hot Spot, Side Stitch.

**Question:** Does `Pace Effort` modify Total Effort, the Pace modifier, a Pace-specific threshold, or another value? At what point in Movement Model A does it apply?

## IMPORTANT

### RR-RACE-008 — Event Play versus React timing

**Affected:** all Event Effects.

**Question:** Which Events are ordinary voluntary hand plays, which may React, what opens a reaction window, and can reactions cancel or modify another play?

### RR-RACE-009 — Target and opponent interaction

**Affected:** Headwind, Congestion, Potholes, High Five, Helpful Runner, and any card using `Target`, `Nearby runner`, or card transfer.

**Question:** Who is a legal target, when is the target selected, may the target refuse, and what public information may be used?

### RR-RACE-010 — Duration and Course scope

**Affected:** Sudden Rain, surface/elevation modifiers, heat/sun prevention, and Course-specific Training/Gear.

**Question:** Does an Effect apply to the current quarter, current mile, next mile, entire turn, round, or while a card remains active? How does it interact with a boundary crossing?

### RR-RACE-011 — Energy modifier versus printed Energy

**Affected:** Running Cap, Tech Shirt, Hydration Belt, Hot Spell, Potholes, High Five, Helpful Runner, Porta-Potty, Tight Calf, Blister, Dehydrated, and Nausea.

**Question:** For conditional or targeted lightning text, what value is modified, who gains/spends it, and is it separate from the card’s own printed Energy field?

### RR-RACE-012 — Pack definitions and benefits

**Affected:** Pace Buddy and any `Nearby runner` interaction.

**Question:** What does `Gain Pack +1` mean, how is adjacency determined, and when does the benefit begin/end?

### RR-RACE-013 — Choice and optionality

**Affected:** Potholes, Goose Chase, Wrong Playlist, Helpful Runner, Porta-Potty, and any effect containing `choose`, `stop`, `give`, or forced Pace change.

**Question:** Which effects are optional or mandatory, who chooses, and what happens if no legal option exists?

### RR-RACE-014 — Prevention and limited uses

**Affected:** Sunglasses, Anti-Chafe, GPS Watch, Running Cap, Tech Shirt.

**Question:** What constitutes the prevented event, how are `first` and `once/Round` tracked, and is the card consumed or retained after use?

## BALANCE

None. Numeric tuning is outside this audit.

## COSMETIC

### RR-RACE-015 — Final title alignment

Resolve whether prototype artwork labels such as `Wild Goose Chase` and `High Performance Shoes` supersede or merely predate the canonical inventory titles `Goose Chase` and `Running Shoes`.
