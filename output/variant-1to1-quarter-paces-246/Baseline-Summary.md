# DRG Baseline Simulation Summary

Config: `simulation/config.json with movement_result_per_space=1, easy_max_energy=3, free_movement_effort_max=6, pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-2},"Push":{"modifier":6,"energy_cost":-3}}`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 13 (p10 12, p90 14) | 12 (p10 11, p90 13) | 12 (p10 11, p90 13) |
| Round of last finish, median | 17 (p10 15, p90 19) | 16 (p10 15, p90 21) | 17 (p10 15, p90 20) |
| Total rounds (all finished or DNF), median | 17 (p10 15, p90 19) | 16 (p10 15, p90 21) | 17 (p10 15, p90 20) |
| Gap first→last finisher, mean rounds | 4.4 | 5.4 | 5.5 |
| Finish rate | 99% | 100% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 2 | failed_gut_check 1 | failed_gut_check 7 |
| Average miles per turn | 1.75 | 1.85 | 1.87 |
| Turns with zero movement | 16% | 12% | 12% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.1 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.34 | 0.35 | 0.47 |
| Will uses per runner | 0.96 | 0.96 | 0.93 |
| Pace choices | Easy 39%, Steady 34%, Push 18%, Race 9% | Easy 39%, Steady 31%, Push 20%, Race 10% | Easy 35%, Steady 32%, Push 21%, Race 11% |
| Cards never played | 16 | 16 | 16 |
