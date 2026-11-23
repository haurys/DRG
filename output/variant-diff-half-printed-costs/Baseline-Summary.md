# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 14 (p10 13, p90 16) | 14 (p10 12, p90 15) | 13 (p10 12, p90 14) |
| Round of last finish, median | 18 (p10 16, p90 22) | 18 (p10 16, p90 21) | 18 (p10 16, p90 21) |
| Total rounds (all finished or DNF), median | 18 (p10 16, p90 22) | 18 (p10 16, p90 21) | 18 (p10 16, p90 21) |
| Gap first→last finisher, mean rounds | 4.3 | 5.4 | 5.1 |
| Finish rate | 98% | 98% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 5 | failed_gut_check 5 | failed_gut_check 9 |
| Average miles per turn | 1.60 | 1.67 | 1.71 |
| Turns with zero movement | 15% | 13% | 12% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.6 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.39 | 0.46 | 0.47 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 62%, Steady 20%, Push 14%, Race 4% | Easy 61%, Steady 20%, Push 14%, Race 5% | Easy 61%, Steady 20%, Push 14%, Race 5% |
| Cards never played | 16 | 16 | 16 |
