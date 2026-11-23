# DRG Baseline Simulation Summary

Config: `simulation/config.json with quarters_per_space=2`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 17 (p10 14, p90 20) | 16 (p10 14, p90 18) | 15 (p10 14, p90 16) |
| Round of last finish, median | 20 (p10 16, p90 26) | 21 (p10 18, p90 26) | 23 (p10 20, p90 29) |
| Total rounds (all finished or DNF), median | 22 (p10 17, p90 29) | 23 (p10 20, p90 30) | 25 (p10 21, p90 31) |
| Gap first→last finisher, mean rounds | 4.1 | 5.8 | 9.2 |
| Finish rate | 50% | 66% | 76% |
| Races with no finisher | 4 | 0 | 0 |
| DNF reasons | energy_exhaustion 82, failed_gut_check 17 | energy_exhaustion 82, failed_gut_check 20 | energy_exhaustion 74, failed_gut_check 24 |
| Average miles per turn | 1.24 | 1.29 | 1.31 |
| Turns with zero movement | 28% | 24% | 21% |
| Deck reshuffles per race | 1.1 | 2.6 | 4.5 |
| Energy stops per runner | 0.73 | 0.62 | 0.47 |
| Gut Check stops per runner | 0.26 | 0.34 | 0.42 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Cards never played | 16 | 16 | 16 |
