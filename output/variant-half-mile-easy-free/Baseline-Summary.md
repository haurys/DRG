# DRG Baseline Simulation Summary

Config: `simulation/config.json with quarters_per_space=2, pace={"Easy":{"modifier":0,"energy_cost":0},"Steady":{"modifier":1,"energy_cost":-1},"Race":{"modifier":2,"energy_cost":-2},"Push":{"modifier":3,"energy_cost":-3}}`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 19 (p10 16, p90 22) | 18 (p10 16, p90 19) | 17 (p10 15, p90 19) |
| Round of last finish, median | 24 (p10 21, p90 29) | 26 (p10 23, p90 33) | 26 (p10 22, p90 32) |
| Total rounds (all finished or DNF), median | 26 (p10 22, p90 29) | 27 (p10 24, p90 33) | 28 (p10 23, p90 33) |
| Gap first→last finisher, mean rounds | 5.8 | 9.5 | 10.1 |
| Finish rate | 84% | 89% | 90% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 18, energy_exhaustion 14 | energy_exhaustion 15, failed_gut_check 17 | failed_gut_check 24, energy_exhaustion 17 |
| Average miles per turn | 1.16 | 1.18 | 1.22 |
| Turns with zero movement | 27% | 25% | 23% |
| Deck reshuffles per race | 1.5 | 3.1 | 5.1 |
| Energy stops per runner | 0.28 | 0.30 | 0.24 |
| Gut Check stops per runner | 0.40 | 0.47 | 0.49 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Cards never played | 16 | 16 | 16 |
