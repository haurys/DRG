# DRG Baseline Simulation Summary

Config: `simulation/config.json with pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-2},"Push":{"modifier":6,"energy_cost":-3}}, easy_max_energy=3, free_movement_effort_max=6`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 24 (p10 22, p90 26) | 23 (p10 22, p90 25) | 22 (p10 21, p90 24) |
| Round of last finish, median | 29 (p10 28, p90 34) | 30 (p10 28, p90 33) | 30 (p10 28, p90 34) |
| Total rounds (all finished or DNF), median | 29 (p10 28, p90 34) | 30 (p10 28, p90 33) | 30 (p10 28, p90 34) |
| Gap first→last finisher, mean rounds | 6.3 | 6.9 | 8.3 |
| Finish rate | 100% | 98% | 99% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 1 | failed_gut_check 6 | failed_gut_check 5 |
| Average miles per turn | 0.97 | 1.00 | 1.02 |
| Turns with zero movement | 13% | 12% | 11% |
| Deck reshuffles per race | 2.0 | 4.0 | 6.2 |
| Energy stops per runner | 0.00 | 0.00 | 0.01 |
| Gut Check stops per runner | 0.28 | 0.44 | 0.53 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 53%, Steady 29%, Push 12%, Race 6% | Easy 53%, Steady 27%, Push 14%, Race 6% | Easy 52%, Steady 27%, Push 14%, Race 7% |
| Cards never played | 16 | 16 | 16 |
