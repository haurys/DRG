# DRG Baseline Simulation Summary

Config: `simulation/config.json with pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-2},"Push":{"modifier":6,"energy_cost":-3}}, easy_max_energy=3`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 31 (p10 29, p90 34) | 30 (p10 27, p90 32) | 28 (p10 27, p90 29) |
| Round of last finish, median | 38 (p10 35, p90 43) | 38 (p10 34, p90 44) | 38 (p10 35, p90 45) |
| Total rounds (all finished or DNF), median | 39 (p10 36, p90 43) | 38 (p10 34, p90 44) | 38 (p10 35, p90 45) |
| Gap first→last finisher, mean rounds | 7.8 | 9.7 | 11.4 |
| Finish rate | 94% | 94% | 95% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 12, energy_exhaustion 1 | failed_gut_check 18 | failed_gut_check 21 |
| Average miles per turn | 0.75 | 0.78 | 0.80 |
| Turns with zero movement | 16% | 14% | 13% |
| Deck reshuffles per race | 2.9 | 5.1 | 8.2 |
| Energy stops per runner | 0.01 | 0.01 | 0.00 |
| Gut Check stops per runner | 0.35 | 0.49 | 0.52 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 71%, Steady 17%, Push 8%, Race 3% | Easy 70%, Steady 17%, Push 9%, Race 4% | Easy 69%, Steady 18%, Push 9%, Race 5% |
| Cards never played | 16 | 16 | 16 |
