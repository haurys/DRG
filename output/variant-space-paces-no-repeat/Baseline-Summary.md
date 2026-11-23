# DRG Baseline Simulation Summary

Config: `simulation/config.json with quarters_per_space=2, easy_no_repeat=true, pace={"Easy":{"modifier":0,"energy_cost":0,"energy_gain":1},"Steady":{"modifier":2,"energy_cost":-1},"Race":{"modifier":4,"energy_cost":-3},"Push":{"modifier":6,"energy_cost":-5}}`; player_count and seed set in memory. Seeds 1001–1050 at every player count.

| Metric | 4 players | 6 players | 8 players |
|---|---|---|---|
| Races completed / errors | 50 / 0 | 50 / 0 | 50 / 0 |
| Round of first finish, median | 15 (p10 14, p90 17) | 14 (p10 13, p90 17) | 14 (p10 12, p90 15) |
| Round of last finish, median | 20 (p10 18, p90 23) | 20 (p10 18, p90 22) | 20 (p10 18, p90 22) |
| Total rounds (all finished or DNF), median | 20 (p10 18, p90 23) | 20 (p10 18, p90 22) | 20 (p10 18, p90 25) |
| Gap first→last finisher, mean rounds | 4.5 | 5.5 | 7.0 |
| Finish rate | 92% | 93% | 94% |
| Races with no finisher | 0 | 0 | 0 |
| DNF reasons | failed_gut_check 16 | failed_gut_check 20 | failed_gut_check 22 |
| Average miles per turn | 1.48 | 1.53 | 1.54 |
| Turns with zero movement | 21% | 18% | 19% |
| Deck reshuffles per race | 1.0 | 2.3 | 3.9 |
| Energy stops per runner | 0.00 | 0.00 | 0.00 |
| Gut Check stops per runner | 0.46 | 0.58 | 0.54 |
| Will uses per runner | 1.00 | 0.99 | 1.00 |
| Pace choices | Easy 49%, Steady 36%, Push 11%, Race 4% | Easy 47%, Steady 38%, Push 11%, Race 4% | Easy 45%, Steady 39%, Push 10%, Race 5% |
| Cards never played | 16 | 16 | 16 |
