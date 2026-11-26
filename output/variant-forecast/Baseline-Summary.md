# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with forecast="random"`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 11 (p10 10, p90 12) | 11 (p10 10, p90 12) | 10 (p10 10, p90 11) |
| Round of last finish, median | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) |
| Total rounds (all finished or DNF), median | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) |
| Gap first→last finisher, mean rounds | 3.0 | 3.2 | 3.7 |
| Finish rate | 97% | 99% | 99% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 6 | failed_gut_check 4 | failed_gut_check 4 |
| Average miles per turn | 2.07 | 2.14 | 2.18 |
| Turns with zero movement | 7% | 5% | 5% |
| Deck reshuffles per race | 1.0 | 1.9 | 3.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.12 | 0.13 | 0.17 |
| Will uses per runner | 1.00 | 0.99 | 0.99 |
| Pace choices | Easy 46%, Steady 26%, Push 17%, Race 11% | Easy 47%, Steady 24%, Push 17%, Race 11% | Easy 41%, Steady 29%, Push 18%, Race 12% |
| Cards never played | 0 | 0 | 0 |
