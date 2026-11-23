# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2, effort_add=1, free_movement_effort_max=4, one_energy_effort_max=7`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 11 (p10 10, p90 12) | 11 (p10 10, p90 11) | 10 (p10 10, p90 11) |
| Round of last finish, median | 14 (p10 13, p90 15) | 13 (p10 12, p90 15) | 14 (p10 13, p90 15) |
| Total rounds (all finished or DNF), median | 14 (p10 13, p90 15) | 14 (p10 13, p90 15) | 14 (p10 13, p90 15) |
| Gap first→last finisher, mean rounds | 2.9 | 3.2 | 3.9 |
| Finish rate | 99% | 99% | 99% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 2 | failed_gut_check 4 | failed_gut_check 5 |
| Average miles per turn | 2.08 | 2.17 | 2.19 |
| Turns with zero movement | 8% | 6% | 6% |
| Deck reshuffles per race | 1.0 | 1.8 | 2.9 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.11 | 0.10 | 0.10 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 66%, Push 15%, Steady 15%, Race 4% | Easy 66%, Push 16%, Steady 13%, Race 4% | Easy 65%, Push 16%, Steady 14%, Race 4% |
| Cards never played | 16 | 16 | 16 |
