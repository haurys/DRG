# DRG Baseline Simulation Summary

Config: `simulation/config.json with pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-2},"Push":{"modifier":6,"energy_cost":-3}}, easy_max_energy=3, quarters_per_space=2, free_movement_effort_max=5`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 12 (p10 11, p90 14) | 12 (p10 11, p90 13) | 12 (p10 11, p90 13) |
| Round of last finish, median | 16 (p10 14, p90 20) | 16 (p10 14, p90 20) | 17 (p10 15, p90 20) |
| Total rounds (all finished or DNF), median | 16 (p10 14, p90 20) | 16 (p10 14, p90 20) | 17 (p10 15, p90 21) |
| Gap first→last finisher, mean rounds | 4.3 | 5.0 | 5.8 |
| Finish rate | 99% | 100% | 100% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 2 | failed_gut_check 1 | failed_gut_check 2 |
| Average miles per turn | 1.82 | 1.88 | 1.88 |
| Turns with zero movement | 14% | 13% | 13% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.1 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.26 | 0.33 | 0.41 |
| Will uses per runner | 0.98 | 0.96 | 0.95 |
| Pace choices | Easy 46%, Steady 29%, Push 17%, Race 8% | Easy 42%, Steady 31%, Push 18%, Race 8% | Easy 41%, Steady 31%, Push 19%, Race 10% |
| Cards never played | 16 | 16 | 16 |
