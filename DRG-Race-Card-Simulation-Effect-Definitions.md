# DRG Race Card Simulation Effect Definitions

**Status:** Frozen specification for the next simulation
**Source:** Latest `RaceCards.docx` plus the frozen clarifications established after import.
**Purpose:** Provide explicit simulation semantics behind the compact printed card Effects.

---

## 1. Canonical Symbols

| Meaning | Symbol |
|---|---|
| Movement | `→` |
| Easy Pace | `▷` |
| Steady Pace | `▶` |
| Race Pace | `▶▶` |
| Push Pace | `▶▶▶` |
| Energy | `⚡` |

`Runner` means another player. The current player is implicit.

---

## 2. Card Use Model

Every non-Condition Race Card has two mutually exclusive uses.

### Movement Use

Use the printed **Effort** and ignore the printed Effect.

Movement Energy cost is determined by printed Effort:

| Effort | Energy cost |
|---:|---:|
| 1–3 | 0 |
| 4–6 | 1 Energy |
| 7+ | 2 Energy |

If two cards are used for Movement in the same turn, pay each card's Movement Energy cost independently.

### Effect Use

Resolve the printed Effect and ignore the printed Effort.

Playing a card for its Effect does **not** pay that card's Movement Energy cost.

### Conditions

Conditions:
- show **Severity**, not Effort;
- cannot be used for Movement;
- have no Movement Energy cost;
- enter play under the existing Condition draw/replacement rules.

---

## 3. General Simulation Conventions

- `+⚡` = gain 1 Energy.
- `+⚡⚡` = gain 2 Energy.
- `+⚡⚡⚡` = gain 3 Energy.
- `-⚡` = lose 1 Energy.
- `+→` = +1 Movement to the applicable Movement resolution.
- `-→` = -1 Movement to the applicable Movement resolution.
- `++→` = +2 Movement.
- A named Condition followed by `-N` means reduce that Condition's **Current Severity** by N unless the card is specifically defined as temporary suppression.
- A terrain/elevation followed by `-N` means reduce applicable Course Difficulty by N.
- A surface followed by `+N` on a Condition means increase applicable Course Difficulty by N.
- Installed Training/Gear recurring Energy Effects trigger at most once per runner-turn unless a card explicitly states another timing.
- `No -⚡` means prevent the specified 1-Energy loss/cost from the named source.
- `Remedy [Condition]` means fully resolve/remove that eligible nonpersistent Condition according to the canonical remedy rule.
- If a persistent Condition reaches Current Severity 0, preserve the existing persistent-at-zero handling unless a card explicitly removes it.
- Where an Event gives another Runner a future Movement modifier, stage it for that Runner's next applicable Movement resolution.
- Historical audit files may retain obsolete names/effects; this document describes the current simulation specification.

---

# 4. Training — 20 Physical Cards

Training cards are installed through the existing Training setup action. Their persistent Effect remains active while installed unless a duration is specified.

| Qty | Effort | Move Cost | Title | Printed Effect | Simulation Definition |
|---:|---:|---:|---|---|---|
| 2 | 7 | 2 | Long Run | `▶▶: No -⚡; Dead Legs: -2` | While installed, at Race Pace prevent 1 Pace-related Energy cost once per runner-turn. On installation/acquisition, if Dead Legs is active, reduce its Current Severity by 2. |
| 1 | 6 | 1 | Base Miles | `▷: +⚡; Dead Legs/Tight Calf: -1` | While installed, at Easy Pace gain 1 Energy once per runner-turn. On installation/acquisition, reduce Current Severity of one applicable active Dead Legs or Tight Calf by 1. |
| 1 | 8 | 2 | Negative Split | `▶▶: +⚡` | While installed, at Race Pace gain 1 Energy once per runner-turn. |
| 2 | 6 | 1 | Tempo Run | `▶: +⚡` | While installed, at Steady Pace gain 1 Energy once per runner-turn. |
| 2 | 8 | 2 | Intervals | `▶▶▶: +⚡` | While installed, at Push Pace gain 1 Energy once per runner-turn. |
| 2 | 7 | 2 | Hill Repeats | `Incline: -2; Steep Incline: -1` | While installed, reduce Course Difficulty by 2 on Incline segments and by 1 on Steep Incline segments. Apply before Movement conversion. |
| 2 | 5 | 1 | Strength Training | `Gut Check: +1; Cramp/Tight Calf: -1` | While installed, add +1 to every Gut Check total. On installation/acquisition, reduce Current Severity of one applicable active Cramp or Tight Calf by 1. |
| 2 | 6 | 1 | Pacing Practice | `▶: No -⚡; Side Stitch: -2` | While installed, at Steady Pace prevent the 1-Energy Pace cost once per runner-turn. On installation/acquisition, if Side Stitch is active, reduce its Current Severity by 2. |
| 2 | 5 | 1 | Trail Training | `Trail: +⚡` | While installed and running on Trail, gain 1 Energy once per runner-turn. |
| 1 | 4 | 1 | Form Drills | `Flat: +⚡; Hot Spot/Sore Feet: -1` | While installed on Flat elevation, gain 1 Energy once per runner-turn. On installation/acquisition, reduce Current Severity of one applicable active Hot Spot or Sore Feet by 1. |
| 1 | 5 | 1 | Downhill Practice | `Descent: -2; Steep Descent: -1` | While installed, reduce Course Difficulty by 2 on Descent segments and by 1 on Steep Descent segments. Apply before Movement conversion. |
| 2 | 9 | 2 | Mental Toughness | `Gut Check: +3` | While installed, add +3 to every Gut Check total. |

### Training Notes

- Training Condition reductions occur when the Training card is installed/acquired, not every round.
- Gut Check modifiers stack when multiple legally installed cards apply.
- Training Effects do not add printed Effort to normal Movement.

---

# 5. Gear — 20 Physical Cards

Gear is equipped/attached through the existing Gear setup rules. Effects remain active while equipped unless temporary duration is specified.

| Qty | Effort | Move Cost | Title | Printed Effect | Simulation Definition |
|---:|---:|---:|---|---|---|
| 2 | 7 | 2 | Running Shoes | `Asphalt: +⚡` | While equipped and running on Asphalt, gain 1 Energy once per runner-turn. |
| 1 | 4 | 1 | Running Socks | `Blister: -2` | While attached/equipped for an active Blister, reduce its Effective Severity by 2 without changing underlying Current Severity unless the canonical Gear suppression rule says otherwise. |
| 1 | 6 | 1 | Cushioned Shoes | `▶: +⚡` | While equipped at Steady Pace, gain 1 Energy once per runner-turn. |
| 1 | 7 | 2 | Trail Shoes | `Trail: +⚡⚡` | While equipped and running on Trail, gain 2 Energy once per runner-turn. |
| 1 | 5 | 1 | Running Cap | `No -⚡ for Heat/Rain` | While equipped, prevent one 1-Energy loss attributable to a Heat or Rain effect each time such an applicable effect resolves. |
| 1 | 7 | 2 | Tempo Shoes | `▶/▶▶: +⚡ (5 Rounds)` | When equipped, remain active for 5 runner-rounds. At Steady or Race Pace, gain 1 Energy once per runner-turn while active. Expire after the fifth applicable round. |
| 1 | 4 | 1 | Tech Shirt | `No -⚡ for Cold/Heat` | While equipped, prevent one 1-Energy loss attributable to a Cold or Heat effect each time such an applicable effect resolves. |
| 1 | 5 | 1 | Running Shorts | `▶: +⚡` | While equipped at Steady Pace, gain 1 Energy once per runner-turn. |
| 1 | 4 | 1 | Sunglasses | `No -⚡` | While equipped, prevent the applicable 1-Energy loss caused by Sun effects. |
| 1 | 8 | 2 | Carbon Racers | `▶▶/▶▶▶: +⚡⚡ (3 Rounds)` | When equipped, remain active for 3 runner-rounds. At Race or Push Pace, gain 2 Energy once per runner-turn while active. Expire after the third applicable round. |
| 1 | 6 | 1 | Hydration Belt | `+⚡` | While equipped, gain 1 Energy when the runner resolves an applicable Water opportunity/milestone. Resolve at most once per Water opportunity. |
| 1 | 6 | 1 | Running Jacket | `No -⚡ for Cold/Rain/Wind` | While equipped, prevent one 1-Energy loss attributable to a Cold, Rain, or Wind effect each time such an applicable effect resolves. |
| 1 | 5 | 1 | Anti-Chafe | `Prevent Hot Spot` | While equipped/active, prevent a new Hot Spot Condition from being applied. It does not remove an already-active Hot Spot unless another rule says so. |
| 1 | 5 | 1 | Singlet | `No -⚡ Heat` | While equipped, prevent one 1-Energy loss attributable to Heat each time such an applicable effect resolves. |
| 1 | 8 | 2 | GPS Watch | `+⚡ (2 Rounds)` | When equipped/activated, gain 1 Energy in each of the next 2 runner-rounds, then expire. Maximum total gain is 2 Energy. |
| 1 | 5 | 1 | Recovery Sleeves | `Tight Calf: -1` | While attached/equipped for an active Tight Calf, reduce its Effective Severity by 1 without changing underlying Current Severity unless the canonical Gear suppression rule says otherwise. |
| 1 | 6 | 1 | Pace Band | `Gut Check: +2` | While equipped, add +2 to every Gut Check total. |
| 1 | 5 | 1 | Compression Sleeves | `Cramp: -2` | While attached/equipped for an active Cramp, reduce its Effective Severity by 2 without changing underlying Current Severity unless the canonical Gear suppression rule says otherwise. |
| 1 | 6 | 1 | Insoles | `Concrete: +⚡` | While equipped and running on Concrete, gain 1 Energy once per runner-turn. |

### Gear Notes

- Running Jacket replaces the former second Hydration Belt slot.
- Only one Hydration Belt remains.
- Weather protection prevents the named Energy loss; it does not generate Energy.
- Temporary Gear duration is deterministic and must be logged on activation, tick, and expiry.

---

# 6. Fuel — 22 Physical Cards

Fuel cards are normally one-shot Effect cards and then discard/recycle under the existing deck rules.

For any Fuel card with `or`, choose exactly one branch.

| Effort | Move Cost | Title | Printed Effect | Simulation Definition |
|---:|---:|---|---|---|
| 3 | 0 | Energy Gel | `+⚡⚡` | Gain 2 Energy immediately. |
| 5 | 1 | Energy Gel | `+⚡⚡` | Gain 2 Energy immediately. |
| 7 | 2 | Energy Gel | `+⚡⚡` | Gain 2 Energy immediately. |
| 4 | 1 | Energy Chews | `+⚡⚡` | Gain 2 Energy immediately. |
| 6 | 1 | Energy Chews | `+⚡⚡` | Gain 2 Energy immediately. |
| 3 | 0 | Banana | `+⚡⚡ or Tight Calf: -2` | Choose one: gain 2 Energy immediately, OR reduce active Tight Calf Current Severity by 2. Never resolve both. |
| 5 | 1 | Banana | `+⚡⚡ or Tight Calf: -2` | Choose one: gain 2 Energy immediately, OR reduce active Tight Calf Current Severity by 2. Never resolve both. |
| 4 | 1 | Snack Bar | `+⚡⚡` | Gain 2 Energy immediately. |
| 7 | 2 | Snack Bar | `+⚡⚡` | Gain 2 Energy immediately. |
| 2 | 0 | Water Bottle | `+⚡⚡ or Heat Exhaustion: -2` | Choose one: gain 2 Energy immediately, OR reduce active Heat Exhaustion Current Severity by 2. |
| 4 | 1 | Water Bottle | `+⚡⚡ or Heat Exhaustion: -2` | Choose one: gain 2 Energy immediately, OR reduce active Heat Exhaustion Current Severity by 2. |
| 6 | 1 | Water Bottle | `+⚡⚡ or Heat Exhaustion: -2` | Choose one: gain 2 Energy immediately, OR reduce active Heat Exhaustion Current Severity by 2. |
| 3 | 0 | Sports Drink | `+⚡⚡` | Gain 2 Energy immediately. |
| 5 | 1 | Sports Drink | `+⚡⚡` | Gain 2 Energy immediately. |
| 7 | 2 | Sports Drink | `+⚡⚡` | Gain 2 Energy immediately. |
| 4 | 1 | Electrolytes | `+⚡⚡ or Remedy Dehydrated` | Choose one: gain 2 Energy immediately, OR fully Remedy one active Dehydrated Condition. |
| 6 | 1 | Electrolytes | `+⚡⚡ or Remedy Dehydrated` | Choose one: gain 2 Energy immediately, OR fully Remedy one active Dehydrated Condition. |
| 8 | 2 | Electrolytes | `+⚡⚡ or Remedy Dehydrated` | Choose one: gain 2 Energy immediately, OR fully Remedy one active Dehydrated Condition. |
| 5 | 1 | Salt Tabs | `+⚡⚡ or Remedy Cramp` | Choose one: gain 2 Energy immediately, OR fully Remedy one active Cramp Condition. |
| 7 | 2 | Salt Tabs | `+⚡⚡ or Remedy Cramp` | Choose one: gain 2 Energy immediately, OR fully Remedy one active Cramp Condition. |
| 3 | 0 | Orange Slice | `+⚡⚡` | Gain 2 Energy immediately. |
| 8 | 2 | Gummy Bears | `+⚡⚡` | Gain 2 Energy immediately. |

### Fuel Notes

- Effect use never pays the printed Movement Energy cost.
- Nausea's `No Fuel Allowed` restriction prevents Fuel **Effect use** while Nausea is active. Fuel cards remain legal Movement cards because Movement use ignores family Effect text.

---

# 7. Event — 30 Physical Cards

Events are one-shot race circumstances. Unless a duration is printed, resolve the Effect immediately or stage it for the target's next applicable resolution as described below.

| ID | Effort | Move Cost | Title | Printed Effect | Simulation Definition |
|---|---:|---:|---|---|---|
| EV-001 | 5 | 1 | Headwind | `Runner -→` | Choose one legal other Runner. Stage -1 Movement for that Runner's next applicable Movement resolution, then clear it. |
| EV-002 | 7 | 2 | Headwind | `Runner -→` | Same as EV-001. |
| EV-003 | 4 | 1 | Tailwind | `+→` | Add +1 Movement to the current player's applicable Movement resolution this turn. |
| EV-004 | 6 | 1 | Tailwind | `+→` | Same as EV-003. |
| EV-005 | 5 | 1 | Sudden Rain | `Difficulty +1 (4 Rounds)` | Increase Course Difficulty by 1 for the affected rain scope for 4 rounds using the existing course/global Event duration model. Log each active round and expiry. |
| EV-006 | 6 | 1 | Hot Spell | `-⚡ (1 Round)` | Current player loses 1 Energy for the applicable Hot Spell resolution window lasting 1 round. Applicable Heat protection can prevent this loss. |
| EV-007 | 4 | 1 | Cool Breeze | `+⚡` | Gain 1 Energy immediately. |
| EV-008 | 3 | 0 | Sun Break | `+→` | Add +1 Movement to the current player's applicable Movement resolution this turn. |
| EV-009 | 4 | 1 | Congestion | `-→` | Apply -1 Movement to the current player's applicable Movement resolution this turn. |
| EV-010 | 6 | 1 | Cold Snap | `-⚡ (1 Round)` | Current player loses 1 Energy for the applicable Cold Snap resolution window lasting 1 round. Applicable Cold protection can prevent this loss. |
| EV-011 | 5 | 1 | Potholes | `Runner -→ or -⚡` | Choose one legal other Runner. That Runner chooses: lose 1 Energy immediately, OR receive -1 Movement on the next applicable Movement resolution. |
| EV-012 | 7 | 2 | Potholes | `Runner -→ or -⚡` | Same as EV-011. |
| EV-013 | 7 | 2 | Clear Road | `+→` | Add +1 Movement to the current player's applicable Movement resolution this turn. |
| EV-014 | 4 | 1 | Good Line | `Ignore Difficulty` | For the current player's applicable Movement resolution this turn, treat Course Difficulty as 0 before Movement conversion. Do not alter the stored Course Difficulty. |
| EV-015 | 5 | 1 | Crowd Support | `+⚡; Runner +⚡` | Current player gains 1 Energy and chooses one legal other Runner to gain 1 Energy. |
| EV-016 | 7 | 2 | Crowd Support | `+⚡; Runner +⚡` | Same as EV-015. |
| EV-017 | 6 | 1 | Tough Decision | `Cycle 2 Cards` | After the applicable Movement resolution, choose up to 2 other cards from hand, discard/cycle them under the existing cycle rule, and draw the same number of replacements if legal. |
| EV-018 | 3 | 0 | High Five | `+⚡; Runner +⚡` | Current player gains 1 Energy and chooses one legal other Runner to gain 1 Energy. Preserve any existing legal-nearby/pack targeting restriction if the canonical engine already defines one. |
| EV-019 | 7 | 2 | Friendly Rival | `+→; Runner +→` | Add +1 Movement to the current player's applicable Movement resolution this turn. Choose one legal other Runner; stage +1 Movement for that Runner's next applicable Movement resolution, then clear it. |
| EV-020 | 5 | 1 | Helpful Runner | `Runner +⚡` | Choose one legal other Runner; that Runner gains 1 Energy immediately. Preserve the existing card-transfer behavior only if it remains canonical outside the printed Effect specification; otherwise do not invent a transfer. |
| EV-021 | 8 | 2 | Second Wind | `+⚡⚡⚡` | Gain 3 Energy immediately. |
| EV-022 | 9 | 2 | Second Wind | `+⚡⚡⚡` | Gain 3 Energy immediately. |
| EV-023 | 10 | 2 | Perfect Rhythm | `++→` | Add +2 Movement to the current player's applicable Movement resolution this turn. Structured value: `movement_delta = +2`. |
| EV-024 | 6 | 1 | Feeling Good | `+⚡⚡` | Gain 2 Energy immediately. |
| EV-025 | 8 | 2 | Wild Goose Chase | `Runner -→ or -⚡` | Choose one legal other Runner. That Runner chooses: lose 1 Energy immediately, OR receive -1 Movement on the next applicable Movement resolution. |
| EV-026 | 4 | 1 | Porta-Potty | `-→; +⚡⚡` | Gain 2 Energy immediately and apply -1 Movement to the current player's applicable Movement resolution this turn. |
| EV-027 | 6 | 1 | Dog Escort | `+→` | Add +1 Movement to the current player's applicable Movement resolution this turn. |
| EV-028 | 3 | 0 | Funny Sign | `+⚡` | Gain 1 Energy immediately. |
| EV-029 | 2 | 0 | Free Donut | `+⚡` | Gain 1 Energy immediately. |
| EV-030 | 5 | 1 | Untied Lace | `Runner -→; No Pack (1 Round)` | Choose one legal other Runner. Stage -1 Movement for that Runner's next applicable Movement resolution and make that Runner ineligible for Pack formation/Pack Energy preservation for 1 round. Expire both effects after the stated round. |

### Event Notes

- `Wrong Playlist` no longer exists.
- EV-010 is `Cold Snap`, not a second `Congestion`.
- Movement modifiers do not change printed Effort; they modify the resulting Movement value for the applicable resolution.
- Where another Runner receives a Movement modifier, the modifier must be staged because that Runner is not resolving Movement during the source player's turn.
- If an existing engine rule defines a stricter legal target set, preserve it and log the selected target.

---

# 8. Conditions — 16 Physical Cards

Conditions remain active under the existing persistence/removal rules.

| Qty | Severity | Title | Printed Effect | Simulation Definition |
|---:|---:|---|---|---|
| 2 | 4 | Cramp | `No ▶▶▶` | While active with Effective Severity above 0, Push Pace is unavailable. |
| 1 | 3 | Tight Calf | `▶▶▶: -⚡` | While active with Effective Severity above 0 and runner is at Push Pace, lose 1 additional Energy once per runner-turn. |
| 1 | 5 | Dead Legs | `▶▶/▶▶▶: -→` | While active with Effective Severity above 0 and runner is at Race or Push Pace, apply -1 Movement to the runner's Movement resolution once per runner-turn. |
| 2 | 3 | Blister | `▶▶▶: -⚡` | While active with Effective Severity above 0 and runner is at Push Pace, lose 1 additional Energy once per runner-turn. |
| 2 | 2 | Hot Spot | `▶▶/▶▶▶: -→` | While active with Effective Severity above 0 and runner is at Race or Push Pace, apply -1 Movement to the runner's Movement resolution once per runner-turn. |
| 1 | 4 | Sore Feet | `Concrete/Asphalt: +2` | While active with Effective Severity above 0 and runner is on Concrete or Asphalt, increase applicable Course Difficulty by 2 before Movement conversion. |
| 1 | 5 | Dehydrated | `▶/▶▶/▶▶▶: -⚡` | While active with Effective Severity above 0 and runner is at Steady, Race, or Push Pace, lose 1 additional Energy once per runner-turn. |
| 1 | 4 | Nausea | `No Fuel Allowed` | While active with Effective Severity above 0, the runner cannot play a Fuel card for its Effect. Fuel cards remain legal for Movement use. |
| 1 | 5 | Gashed Knee | `-→` | While active with Effective Severity above 0, apply -1 Movement to every applicable Movement resolution. |
| 1 | 3 | Side Stitch | `▶▶/▶▶▶: -→` | While active with Effective Severity above 0 and runner is at Race or Push Pace, apply -1 Movement to the runner's Movement resolution once per runner-turn. |
| 1 | 7 | Twisted Ankle | `Max ▶` | While active with Effective Severity above 0, maximum legal Pace is Steady. |
| 1 | 8 | Heat Exhaustion | `Max ▷` | While active with Effective Severity above 0, maximum legal Pace is Easy. |
| 1 | 5 | Cold Chills | `▶▶/▶▶▶: -⚡` | While active with Effective Severity above 0 and runner is at Race or Push Pace, lose 1 additional Energy once per runner-turn. |

### Condition Quantity Check

- Cramp ×2
- Tight Calf ×1
- Dead Legs ×1
- Blister ×2
- Hot Spot ×2
- Sore Feet ×1
- Dehydrated ×1
- Nausea ×1
- Gashed Knee ×1
- Side Stitch ×1
- Twisted Ankle ×1
- Heat Exhaustion ×1
- Cold Chills ×1

**Total Conditions: 16**

### Condition Notes

- `Stomach Trouble` no longer exists.
- `Cold Chills` replaces the former second Dehydrated copy.
- Gashed Knee is nonpersistent under the previously frozen replacement ruling unless the canonical repository has since established otherwise.
- Nausea blocks Fuel Effect use, not Fuel Movement use.
- A Condition's printed Severity is not automatically the numeric magnitude of its penalty. The printed Effect defines the penalty; Severity tracks treatment/state.

---

# 9. Gut Check Simulation Rule

Gut Check Total:

`sum of printed Effort on eligible cards remaining in hand + all applicable installed Gut Check modifiers`

Frozen modifiers:

| Card | Modifier |
|---|---:|
| Strength Training | +1 |
| Pace Band | +2 |
| Mental Toughness | +3 |

Cards are not consumed merely by performing a Gut Check.

Current Marathon thresholds remain:

| Mile | Requirement |
|---:|---:|
| 10 | 25 |
| 18 | 30 |
| 23 | 35 |

---

# 10. Aid / Remedy Interactions

Frozen Aid interactions:

| Condition | Aid Result |
|---|---|
| Nausea | Remedy |
| Gashed Knee | Remedy |
| Twisted Ankle | Current Severity -3 |
| Heat Exhaustion | Current Severity -4 |

Other frozen remedies:

| Source | Result |
|---|---|
| Electrolytes | Remedy Dehydrated OR +2 Energy |
| Salt Tabs | Remedy Cramp OR +2 Energy |
| Water Bottle | Heat Exhaustion Current Severity -2 OR +2 Energy |
| Banana | Tight Calf Current Severity -2 OR +2 Energy |
| Water milestone/opportunity | Preserve existing canonical Dehydrated remedy behavior |

---

# 11. Weather Mapping

| Weather | Hindrances | Protection / Counterplay |
|---|---|---|
| Heat | Hot Spell, Heat Exhaustion | Running Cap, Tech Shirt, Singlet, Water Bottle, Aid |
| Cold | Cold Snap, Cold Chills | Tech Shirt, Running Jacket |
| Rain | Sudden Rain | Running Cap, Running Jacket |
| Wind | Headwind / Tailwind | Running Jacket |

Weather protection only prevents the applicable Energy loss unless another card explicitly says otherwise.

---

# 12. Structured Effect Fields

The simulator should store explicit semantics rather than parsing printed text at runtime.

Recommended fields:

```text
effect_type
effect_target
effect_value
effect_duration
effect_timing
pace_trigger
surface_trigger
elevation_trigger
weather_trigger
movement_delta
energy_delta
difficulty_delta
severity_delta
gut_check_modifier
pace_max
prevent_condition
remedy_condition
energy_prevention
temporary_rounds
once_per_turn
choice_group
```

Examples:

### Headwind

```yaml
effect_type: movement_modifier
effect_target: other_runner
movement_delta: -1
effect_timing: target_next_movement
once_per_turn: true
```

### Banana

```yaml
effect_type: choice
choice_group:
  - energy_delta: +2
  - condition_name: Tight Calf
    severity_delta: -2
effect_target: self
effect_timing: immediate
```

### GPS Watch

```yaml
effect_type: recurring_energy
effect_target: self
energy_delta: +1
temporary_rounds: 2
effect_timing: round_tick
```

### Cold Chills

```yaml
effect_type: conditional_energy_loss
effect_target: self
pace_trigger: [Race, Push]
energy_delta: -1
once_per_turn: true
condition_required_active: Cold Chills
```

---

# 13. Deck Validation Targets

| Family | Physical Cards |
|---|---:|
| Training | 20 |
| Gear | 20 |
| Fuel | 22 |
| Event | 30 |
| Condition | 16 |
| **Total** | **108** |

Required current swaps:

- second Hydration Belt → Running Jacket
- EV-010 Congestion → Cold Snap
- second Dehydrated → Cold Chills

Required obsolete removals from canonical current card data:

- Wrong Playlist
- Stomach Trouble
- second EV-010 Congestion
- second Hydration Belt
- second Dehydrated
- old `Pace Effort` Effect language

---

# 14. Rules Review / Implementation Cautions

The following are implementation cautions rather than invitations to redesign frozen cards:

1. **Helpful Runner historical transfer behavior**
   The printed frozen Effect is only `Runner +⚡`. If the repository still contains a separate canonical card-transfer mechanic for Helpful Runner, Work must report it before retaining or removing it. Do not infer a transfer from the printed Effect alone.

2. **High Five target eligibility**
   Earlier implementations used Pack/nearby eligibility. Preserve an already-canonical targeting restriction if present; otherwise do not invent one.

3. **Sudden Rain scope**
   The printed card fixes `Difficulty +1 (4 Rounds)`, but the exact course/global scope should use the existing canonical Event-duration model. If the repository contains conflicting scopes, report the conflict rather than choosing silently.

4. **Weather protection stacking**
   Multiple equipped protections must not create Energy. They only prevent applicable loss. If more than one protection applies to the same single 1-Energy loss, total prevention is capped at that loss.

5. **Condition Severity vs penalty magnitude**
   Severity tracks treatment/state. Unless a card explicitly says otherwise, the magnitude of the active penalty is the fixed printed Effect and does not scale numerically with Current Severity.

---

# 15. Simulation Logging Requirements

For every Effect resolution, log enough information to reconstruct the result:

- card ID/title
- card use mode: MOVEMENT or EFFECT
- printed Effort
- Movement Energy cost
- Pace Energy cost
- Energy before/after
- Movement before/after modifier
- Difficulty before/after modifier
- target Runner if applicable
- Condition before/after Severity
- prevention/remedy source
- duration activation/tick/expiry
- Gut Check base hand total
- each Gut Check modifier
- final Gut Check total

The purpose of this document is to eliminate reliance on interpretation of compact printed Effect text during simulation.
