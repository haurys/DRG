# DRG Baseline Simulation Summary

Config: `simulation/config.json with pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-2},"Push":{"modifier":6,"energy_cost":-3}}, easy_max_energy=3, quarters_per_space=2`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 14 (p10 12, p90 16) | 14 (p10 12, p90 15) | 13 (p10 12, p90 14) |
| Round of last finish, median | 20 (p10 17, p90 23) | 19 (p10 17, p90 23) | 19 (p10 17, p90 23) |
| Total rounds (all finished or DNF), median | 20 (p10 17, p90 23) | 19 (p10 17, p90 23) | 19 (p10 17, p90 23) |
| Gap first→last finisher, mean rounds | 5.3 | 5.9 | 7.3 |
| Finish rate | 98% | 99% | 97% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 5 | failed_gut_check 3 | failed_gut_check 11 |
| Average miles per turn | 1.55 | 1.63 | 1.66 |
| Turns with zero movement | 17% | 14% | 15% |
| Deck reshuffles per race | 1.0 | 2.1 | 3.8 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.25 | 0.34 | 0.45 |
| Will uses per runner | 0.99 | 1.00 | 0.99 |
| Pace choices | Easy 58%, Steady 23%, Push 13%, Race 6% | Easy 55%, Steady 24%, Push 14%, Race 7% | Easy 53%, Steady 26%, Push 14%, Race 7% |
| Cards never played | 16 | 16 | 16 |
