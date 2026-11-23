# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2, effort_add=1`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 12 (p10 11, p90 13) | 12 (p10 11, p90 12) | 11 (p10 11, p90 12) |
| Round of last finish, median | 15 (p10 14, p90 17) | 15 (p10 14, p90 16) | 15 (p10 14, p90 18) |
| Total rounds (all finished or DNF), median | 15 (p10 14, p90 17) | 15 (p10 14, p90 16) | 15 (p10 14, p90 18) |
| Gap first→last finisher, mean rounds | 3.1 | 3.3 | 4.2 |
| Finish rate | 98% | 98% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 5 | failed_gut_check 5 | failed_gut_check 9 |
| Average miles per turn | 1.93 | 1.98 | 1.98 |
| Turns with zero movement | 8% | 6% | 7% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.08 | 0.10 | 0.18 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 68%, Steady 15%, Push 14%, Race 3% | Easy 68%, Steady 14%, Push 14%, Race 3% | Easy 68%, Steady 14%, Push 14%, Race 4% |
| Cards never played | 16 | 16 | 16 |
