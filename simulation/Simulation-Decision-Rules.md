# Simulation Decision Rules

Each legal Pace and card option receives a deterministic score. Trace entries preserve considered options, selected option, and reason. Ties use stable IDs, never hidden opponent data. Events always contribute printed Effort and their mandatory effect; Training, Gear, and Fuel use either Movement Effort or Treat/Prepare, never both.

The live turn order is Replenish, deterministic Treat/Prepare, Pace payment, Movement, milestones/Events, and End Turn. Pack state and Pace are frozen from the Round Start snapshot. Same-round finishers are placed only at Round End.

- Balanced: moderate Pace; protects Energy below 6.
- Aggressive: highest sustainable Pace; favors maximum Effort.
- Energy Conservative: prioritizes recovery below 10 and Easy/Steady.
- Course Planner: raises Effort weight on Difficulty 5+ and looks one public mile ahead.
- Pack Runner: adds value to matching the nearest public runner’s Pace.
- Opportunist: values immediate recovery when low and otherwise best current combination.
- Front Runner: emphasizes high Pace until Energy threshold.
- Adaptive: shifts weights using public rank, Energy, Difficulty, and distance remaining.

Pre-race negotiation is a **PLAYTEST ASSUMPTION**: remaining exchanges replace the lowest-valued eligible original card from the deck. Acquired replacements lock.

RR-13 Pack procedure uses a **PLAYTEST ASSUMPTION**: every virtual runner consents to the nearest legal same-Pace group within 0.5 mile of its leader at Round Start; stable player ID breaks policy ties. Potholes chooses Energy loss when possible and Movement loss at zero Energy. Treat/Prepare prioritizes named remedies, compatible suppression, open Training/Gear slots, then Fuel recovery. These are AI policies, not new physical-game rules.
