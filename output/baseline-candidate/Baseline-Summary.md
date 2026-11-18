# DRG Baseline Simulation Summary

Config: `simulation/config.json` with in-memory player_count and seed only. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 33 (p10 30, p90 42) | 32 (p10 27, p90 36) | 31 (p10 28, p90 35) |
| Round of last finish, median | 40 (p10 30, p90 50) | 41 (p10 33, p90 49) | 42 (p10 38, p90 50) |
| Total rounds (all finished or DNF), median | 40 (p10 29, p90 49) | 42 (p10 36, p90 52) | 44 (p10 39, p90 51) |
| Gap first→last finisher, mean rounds | 5.1 | 9.3 | 12.2 |
| Finish rate | 43% | 50% | 57% |
| Races with no finisher | 5 | 0 | 0 |
| DNF reasons | energy_exhaustion 102, failed_gut_check 12 | energy_exhaustion 138, failed_gut_check 13 | failed_gut_check 26, energy_exhaustion 147 |
| Average miles per turn | 0.66 | 0.67 | 0.68 |
| Turns with zero movement | 22% | 20% | 18% |
| Deck reshuffles per race | 2.2 | 4.8 | 8.7 |
| Energy stops per runner | 1.03 | 1.06 | 0.87 |
| Gut Check stops per runner | 0.12 | 0.21 | 0.31 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Cards never played | 16 | 16 | 16 |
