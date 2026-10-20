# Gear — frozen Race Card redesign

20 physical cards. A non-Condition card uses printed Effort and pays its Movement Energy cost **or** resolves its Effect without printed Effort or Movement Energy cost.

Two normal Gear slots allow at most **one equipped footwear card**. Road Trainers (two copies), Cushion Trainers, Trail Shoes, Tempo Trainers, and Carbon Racers count as footwear; Running Socks do not. The `is_footwear` flag in card data is the equipment restriction. Broad Gear `category` labels are descriptive only and impose no apparel, accessory, technology, or support limits. Equipping a new hand card spends the one Treat/Prepare opportunity **and one of two Race-card plays**; a compatible new Condition attachment has the same cost. A legal relocation of already-equipped Gear uses Treat/Prepare but no new card play.

| ID | Title | Effort / Severity | Movement Energy cost | Effect |
|---|---|---:|---:|---|
| GE-001 | Road Trainers | 7 | ⚡⚡ (2) | Asphalt: +⚡ |
| GE-002 | Road Trainers | 7 | ⚡⚡ (2) | Asphalt: +⚡ |
| GE-003 | Running Socks | 4 | ⚡ (1) | Blister: -2 |
| GE-004 | Cushion Trainers | 6 | ⚡ (1) | ▶: +⚡ |
| GE-005 | Trail Shoes | 7 | ⚡⚡ (2) | Trail: +⚡⚡ |
| GE-006 | All-Weather Cap | 5 | ⚡ (1) | No -⚡ for Heat/Rain |
| GE-007 | Tempo Trainers | 7 | ⚡⚡ (2) | ▶/▶▶: +⚡ (5 Rounds) |
| GE-008 | Tech Shirt | 4 | ⚡ (1) | No -⚡ for Cold/Heat |
| GE-009 | Split Shorts | 5 | ⚡ (1) | ▶: +⚡ |
| GE-010 | Glare Shades | 4 | ⚡ (1) | No -⚡ |
| GE-011 | Carbon Racers | 8 | ⚡⚡ (2) | ▶▶/▶▶▶: +⚡⚡ (3 Rounds) |
| GE-012 | Hydration Belt | 6 | ⚡ (1) | +⚡ |
| GE-013 | Weather Shell | 6 | ⚡ (1) | No -⚡ for Cold/Rain/Wind |
| GE-014 | Anti-Chafe | 5 | ⚡ (1) | Prevent Hot Spot |
| GE-015 | Singlet | 5 | ⚡ (1) | No -⚡ Heat |
| GE-016 | Pace Watch | 8 | ⚡⚡ (2) | +⚡ (2 Rounds) |
| GE-017 | Recovery Sleeves | 5 | ⚡ (1) | Tight Calf: -1 |
| GE-018 | Pace Band | 6 | ⚡ (1) | Gut Check: +2 |
| GE-019 | Compression Sleeves | 5 | ⚡ (1) | Cramp: -2 |
| GE-020 | Support Insoles | 6 | ⚡ (1) | Concrete: +⚡ |

Hydration Belt gains 1 Energy at an applicable Water opportunity, at most once per opportunity. Temporary Gear counts its installation turn as the first runner-round. Energy gains trigger once per runner-turn where stated; Pace Watch grants +1 on each of its two active runner-rounds. Weather protection caps at the actual matching Energy loss and never creates Energy.
