# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with forecast="random", race_cards_path="simulation/variants/race_cards-weather-gear-copies.json"`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 11 (p10 10, p90 12) | 11 (p10 10, p90 12) | 10 (p10 10, p90 11) |
| Round of last finish, median | 13 (p10 13, p90 16) | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) |
| Total rounds (all finished or DNF), median | 13 (p10 13, p90 16) | 14 (p10 13, p90 16) | 14 (p10 13, p90 16) |
| Gap first→last finisher, mean rounds | 2.8 | 3.3 | 3.6 |
| Finish rate | 100% | 99% | 98% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 1 | failed_gut_check 3 | failed_gut_check 7 |
| Average miles per turn | 2.10 | 2.11 | 2.17 |
| Turns with zero movement | 6% | 6% | 5% |
| Deck reshuffles per race | 1.0 | 1.9 | 3.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.20 | 0.17 | 0.16 |
| Will uses per runner | 0.98 | 0.99 | 0.98 |
| Pace choices | Easy 45%, Steady 26%, Push 17%, Race 11% | Easy 46%, Steady 26%, Push 17%, Race 11% | Easy 42%, Steady 28%, Push 18%, Race 12% |
| Cards never played | 0 | 0 | 0 |
