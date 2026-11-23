# DRG Baseline Simulation Summary

Config: `simulation/config.json with movement_result_per_space=1, easy_max_energy=3, free_movement_effort_max=6, pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":1,"energy_cost":-1},"Race":{"modifier":2,"energy_cost":-2},"Push":{"modifier":3,"energy_cost":-3}}`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 15 (p10 13, p90 16) | 14 (p10 13, p90 15) | 14 (p10 12, p90 14) |
| Round of last finish, median | 19 (p10 16, p90 22) | 20 (p10 18, p90 24) | 20 (p10 17, p90 23) |
| Total rounds (all finished or DNF), median | 19 (p10 16, p90 22) | 20 (p10 18, p90 24) | 20 (p10 17, p90 23) |
| Gap first→last finisher, mean rounds | 5.3 | 6.1 | 6.5 |
| Finish rate | 98% | 99% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 4 | failed_gut_check 2 | failed_gut_check 9 |
| Average miles per turn | 1.53 | 1.58 | 1.62 |
| Turns with zero movement | 18% | 14% | 13% |
| Deck reshuffles per race | 1.0 | 2.2 | 3.8 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.30 | 0.48 | 0.51 |
| Will uses per runner | 0.95 | 0.95 | 0.97 |
| Pace choices | Easy 44%, Steady 34%, Push 15%, Race 6% | Easy 43%, Steady 33%, Push 16%, Race 8% | Easy 43%, Steady 32%, Push 17%, Race 8% |
| Cards never played | 16 | 16 | 16 |
