# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3, difficulty_divisor=2, effort_add=2, free_movement_effort_max=5, one_energy_effort_max=8`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 9 (p10 8, p90 9) | 9 (p10 8, p90 9) | 8 (p10 8, p90 9) |
| Round of last finish, median | 11 (p10 10, p90 12) | 10 (p10 10, p90 11) | 11 (p10 10, p90 12) |
| Total rounds (all finished or DNF), median | 11 (p10 10, p90 12) | 11 (p10 10, p90 11) | 11 (p10 10, p90 12) |
| Gap first→last finisher, mean rounds | 2.1 | 1.9 | 2.6 |
| Finish rate | 99% | 100% | 100% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 2 | failed_gut_check 1 | none |
| Average miles per turn | 2.64 | 2.70 | 2.76 |
| Turns with zero movement | 5% | 4% | 3% |
| Deck reshuffles per race | 0.4 | 1.0 | 2.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.03 | 0.03 | 0.01 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 65%, Push 18%, Steady 13%, Race 5% | Easy 65%, Push 18%, Steady 13%, Race 4% | Easy 64%, Push 18%, Steady 12%, Race 5% |
| Cards never played | 16 | 16 | 16 |
