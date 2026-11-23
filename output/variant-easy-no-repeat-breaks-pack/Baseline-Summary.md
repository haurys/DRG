# DRG Baseline Simulation Summary

Config: `simulation/config.json with quarters_per_space=2, pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":1,"energy_cost":-1},"Race":{"modifier":2,"energy_cost":-2},"Push":{"modifier":3,"energy_cost":-3}}, easy_no_repeat=true, easy_breaks_pack=true`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 16 (p10 15, p90 18) | 15 (p10 14, p90 17) | 15 (p10 13, p90 16) |
| Round of last finish, median | 21 (p10 18, p90 25) | 22 (p10 19, p90 26) | 22 (p10 19, p90 27) |
| Total rounds (all finished or DNF), median | 21 (p10 18, p90 26) | 22 (p10 19, p90 26) | 23 (p10 19, p90 27) |
| Gap first→last finisher, mean rounds | 5.6 | 7.0 | 8.3 |
| Finish rate | 93% | 96% | 96% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 14 | failed_gut_check 12 | failed_gut_check 15 |
| Average miles per turn | 1.39 | 1.43 | 1.46 |
| Turns with zero movement | 20% | 19% | 17% |
| Deck reshuffles per race | 1.1 | 2.7 | 4.2 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.31 | 0.47 | 0.49 |
| Will uses per runner | 0.99 | 0.99 | 0.99 |
| Pace choices | Easy 54%, Steady 30%, Push 10%, Race 7% | Easy 51%, Steady 32%, Push 10%, Race 7% | Easy 49%, Steady 34%, Push 10%, Race 7% |
| Cards never played | 16 | 16 | 16 |
