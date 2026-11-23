# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2, training_effort_bonus=1, gear_difficulty_reduction=1`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 12 (p10 11, p90 13) | 11 (p10 11, p90 12) | 11 (p10 10, p90 12) |
| Round of last finish, median | 15 (p10 14, p90 16) | 15 (p10 14, p90 16) | 15 (p10 14, p90 17) |
| Total rounds (all finished or DNF), median | 15 (p10 14, p90 16) | 15 (p10 14, p90 16) | 15 (p10 14, p90 17) |
| Gap first→last finisher, mean rounds | 2.9 | 3.7 | 4.3 |
| Finish rate | 98% | 99% | 99% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 3 | failed_gut_check 4 | failed_gut_check 5 |
| Average miles per turn | 1.93 | 1.98 | 2.00 |
| Turns with zero movement | 9% | 7% | 7% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.20 | 0.19 | 0.21 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 65%, Push 16%, Steady 15%, Race 4% | Easy 66%, Push 15%, Steady 14%, Race 5% | Easy 64%, Steady 16%, Push 16%, Race 5% |
| Cards never played | 16 | 16 | 16 |
