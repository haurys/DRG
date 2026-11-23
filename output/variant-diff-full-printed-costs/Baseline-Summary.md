# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with free_movement_effort_max=3`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 18 (p10 16, p90 19) | 17 (p10 16, p90 18) | 16 (p10 15, p90 18) |
| Round of last finish, median | 23 (p10 20, p90 28) | 24 (p10 21, p90 31) | 23 (p10 20, p90 29) |
| Total rounds (all finished or DNF), median | 23 (p10 20, p90 28) | 24 (p10 21, p90 31) | 23 (p10 20, p90 29) |
| Gap first→last finisher, mean rounds | 5.8 | 8.7 | 7.6 |
| Finish rate | 92% | 96% | 97% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 15 | failed_gut_check 11 | failed_gut_check 11 |
| Average miles per turn | 1.27 | 1.28 | 1.35 |
| Turns with zero movement | 20% | 20% | 16% |
| Deck reshuffles per race | 1.4 | 3.0 | 4.7 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.39 | 0.46 | 0.45 |
| Will uses per runner | 1.00 | 1.00 | 1.00 |
| Pace choices | Easy 63%, Steady 21%, Push 12%, Race 4% | Easy 60%, Steady 23%, Push 11%, Race 5% | Easy 61%, Steady 22%, Push 12%, Race 5% |
| Cards never played | 16 | 16 | 16 |
