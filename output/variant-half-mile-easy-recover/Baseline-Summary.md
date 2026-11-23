# DRG Baseline Simulation Summary

Config: `simulation/config.json with quarters_per_space=2, pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":1,"energy_cost":-1},"Race":{"modifier":2,"energy_cost":-2},"Push":{"modifier":3,"energy_cost":-3}}`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 16 (p10 15, p90 18) | 15 (p10 13, p90 16) | 14 (p10 13, p90 16) |
| Round of last finish, median | 21 (p10 18, p90 24) | 21 (p10 18, p90 24) | 22 (p10 19, p90 26) |
| Total rounds (all finished or DNF), median | 21 (p10 18, p90 24) | 21 (p10 18, p90 24) | 22 (p10 20, p90 26) |
| Gap first→last finisher, mean rounds | 5.2 | 6.6 | 8.7 |
| Finish rate | 96% | 97% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 8 | failed_gut_check 8 | failed_gut_check 8 |
| Average miles per turn | 1.43 | 1.48 | 1.48 |
| Turns with zero movement | 19% | 18% | 18% |
| Deck reshuffles per race | 1.0 | 2.5 | 4.2 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.33 | 0.46 | 0.51 |
| Will uses per runner | 0.96 | 0.98 | 0.99 |
| Cards never played | 16 | 16 | 16 |
