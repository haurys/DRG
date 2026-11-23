# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2, gear_difficulty_reduction=1`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 13 (p10 12, p90 14) | 12 (p10 11, p90 13) | 12 (p10 11, p90 13) |
| Round of last finish, median | 16 (p10 15, p90 18) | 16 (p10 14, p90 18) | 16 (p10 15, p90 19) |
| Total rounds (all finished or DNF), median | 16 (p10 15, p90 18) | 16 (p10 14, p90 18) | 16 (p10 15, p90 19) |
| Gap first→last finisher, mean rounds | 3.4 | 4.1 | 4.7 |
| Finish rate | 98% | 98% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 3 | failed_gut_check 6 | failed_gut_check 8 |
| Average miles per turn | 1.78 | 1.88 | 1.88 |
| Turns with zero movement | 11% | 9% | 9% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.2 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.20 | 0.23 | 0.31 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 65%, Steady 16%, Push 15%, Race 4% | Easy 65%, Steady 16%, Push 15%, Race 5% | Easy 63%, Steady 18%, Push 15%, Race 5% |
| Cards never played | 16 | 16 | 16 |
