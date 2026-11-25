# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with always_event_effect=true`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 10 (p10 9, p90 11) | 10 (p10 9, p90 10) | 9 (p10 9, p90 10) |
| Round of last finish, median | 13 (p10 12, p90 14) | 12 (p10 11, p90 14) | 12 (p10 11, p90 14) |
| Total rounds (all finished or DNF), median | 13 (p10 12, p90 15) | 12 (p10 11, p90 14) | 12 (p10 12, p90 14) |
| Gap first→last finisher, mean rounds | 2.6 | 2.9 | 3.3 |
| Finish rate | 93% | 97% | 97% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 14 | energy_exhaustion 1, failed_gut_check 8 | failed_gut_check 12 |
| Average miles per turn | 2.26 | 2.36 | 2.43 |
| Turns with zero movement | 5% | 3% | 3% |
| Deck reshuffles per race | 1.0 | 1.5 | 2.9 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.71 | 0.48 | 0.45 |
| Will uses per runner | 0.92 | 0.91 | 0.90 |
| Pace choices | Easy 38%, Steady 30%, Push 22%, Race 10% | Easy 36%, Steady 29%, Push 23%, Race 11% | Easy 34%, Steady 31%, Push 23%, Race 12% |
| Cards never played | 0 | 0 | 0 |
