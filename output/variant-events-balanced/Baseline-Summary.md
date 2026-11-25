# DRG Baseline Simulation Summary

Config: `simulation/config-working-candidate.json with always_event_effect=true, race_cards_path="simulation/variants/race_cards-events-balanced.json"`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 11 (p10 10, p90 13) | 11 (p10 10, p90 11) | 11 (p10 10, p90 11) |
| Round of last finish, median | 15 (p10 13, p90 17) | 14 (p10 13, p90 17) | 14 (p10 13, p90 16) |
| Total rounds (all finished or DNF), median | 15 (p10 13, p90 18) | 15 (p10 13, p90 17) | 14 (p10 13, p90 16) |
| Gap first→last finisher, mean rounds | 3.5 | 4.1 | 4.2 |
| Finish rate | 92% | 95% | 94% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 15 | failed_gut_check 16 | failed_gut_check 23 |
| Average miles per turn | 1.98 | 2.05 | 2.10 |
| Turns with zero movement | 7% | 6% | 5% |
| Deck reshuffles per race | 1.0 | 2.0 | 3.0 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.92 | 0.79 | 0.85 |
| Will uses per runner | 0.95 | 0.95 | 0.92 |
| Pace choices | Easy 40%, Steady 29%, Push 20%, Race 11% | Easy 40%, Steady 27%, Push 22%, Race 11% | Easy 37%, Steady 29%, Push 22%, Race 12% |
| Cards never played | 11 | 11 | 11 |
