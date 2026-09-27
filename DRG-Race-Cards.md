# DRG Race cards — canonical playtest index

This is the **current designer-rule inventory**, not a claim that the older engine JSON has been updated. Each family file holds the per-design/current effect and all known physical copy IDs. The legacy per-copy inventory [`data/Race-Cards.md`](data/Race-Cards.md) and [`data/race_cards.json`](data/race_cards.json) are **historical baseline only** where superseded. See [Superseded Rules](DRG-Superseded-Rules.md) and [Rules Review](DRG-Rules-Review.md).

| Family | Copies | Current design count | Detailed current inventory |
|---|---:|---:|---|
| Training | 20 | 12 | [DRG-Training.md](DRG-Training.md), TR-001–020. |
| Gear | 20 | 18 | [DRG-Gear.md](DRG-Gear.md): 15 surviving old IDs and 5 currently unassigned new designs. |
| Fuel | 22 | 10 named families / 22 Effort variants | [DRG-Fuel.md](DRG-Fuel.md), FU-001–022. |
| Event | 30 | 24 titles / 30 printed Effort variants | [DRG-Events.md](DRG-Events.md), EV-001–030. |
| Condition | 16 | 12 | [DRG-Conditions.md](DRG-Conditions.md), CO-001–016. |
| **Total** | **108** | — | Counts include every physical slot. |

Normal cards have family, title, printed Effort, a **separate** signed printed Energy field **where independently established**, and optional effect. An Energy gain/cost in effect text is not proof of a separate printed Energy symbol. Unknown Energy remains `null`/unknown, never zero. Training/Gear/Fuel in Movement use **only Effort**; in Treat/Prepare use only their installation/equip/consumption effect. Event in Movement uses **Effort and mandatory Effect**; Event does not enter Treat/Prepare and is limited to one per turn. Conditions have Base/Current/Effective **Severity**, no Effort; they activate when drawn, enter the active area, and prompt replacement draw. Source `CARDS.docx` did not provide a dedicated signed-Energy column; current Fuel/Event gain amounts are effect semantics unless separate printed fields are confirmed.

Frozen replacements: GE-004 Cushioned Shoes E6; GE-007 Tempo Shoes E7; GE-011 Carbon Racers E8; GE-015 Lightweight Singlet E5; GE-017 Recovery Sleeves E5. Event replacements/clarifications: EV-014 Good Line E4; EV-017 Tough Decision E6 cycles up to two; EV-005 Sudden Rain lasts four rounds; EV-018 High Five uses Pack-or-self scope; EV-020 transfers itself with a next-round replay lock.

Visual design decisions: Training Blue `#2878B5`; Gear Orange `#E87524`; Fuel Green `#3D9140`; Event Purple `#7553A6`; Condition Red `#C83C3C`; DRG logo black only; card titles preferably at most three words. Simple solid rounded monochrome-compatible family icons: approved Training shape rotated clockwise 90°, running-equipment-inspired Gear (not mechanical cog), single-droplet Fuel, rounded four-point-star Event, thick-plus Condition. No standard suit symbols. Race cards 2.5 × 3.5 inches portrait; Effort prominent and Energy visually separate; Condition large number means Severity, **not Effort**.

Current physical Gear distribution of Running Shoes ×2, Hydration Belt ×2, and sixteen other designs ×1 **does** reconcile to 20. The five new Gear designs' Effort values and physical-copy IDs are not supplied. Do not repurpose superseded duplicate IDs without a mapping decision. Their absence blocks a fully executable 108-copy deck.
