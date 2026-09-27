# Rules Review

## BLOCKING

None for execution under the stated assumptions. The following prevent an assumption-free, canonically legitimate simulation.

- **RR-002 Card Energy completeness:** the source inventory does not show a separate Energy field for most cards. Values cannot be inferred from title or art.
- **RR-003 Effect execution:** target selection, timing, duration, reactions, Preparation slots, and persistence are incomplete.
- **RR-004 Condition lifecycle:** activation timing, stacking, treatment spending/timing, maximum handling, and duration are incomplete.
- **RR-005 Finish:** exact 0.1/0.2-mile movement/payment procedure is unspecified.

## IMPORTANT

- Water and Aid/Fuel recovery amounts and timing.
- Gut Check test procedure, failure consequence, and modifiers.
- Will trigger, benefit, and exact timing.
- Pack entry/exit timing and mechanical benefit.
- Deck exhaustion and discard recycling timing.
- Energy minimum/maximum and whether a Pace cost can make Energy negative.
- Maximum Conditions per turn and overflow behavior.
- Pre-race negotiation valuation and simultaneous/open timing.

## BALANCE

- Pace costs, starting Energy, movement conversion, starting hand, two-card limit, and Condition cap.

## COSMETIC / NON-SIMULATION

- Final card titles and whether Country is replaced everywhere by Rural.
- Final printed terminology for energy icons and treatment notation.

## Configurable playtest assumptions

All unresolved executable choices are in `simulation/config.json`; none are declared canonical. Movement is now canonical for simulation: `Total Effort + Pace modifier - current Difficulty`, with positive excess carried across boundaries and adjusted only by the Difficulty difference. Remaining assumptions cover Condition overflow, discard recycling, milestones, Will, Pack benefit, incomplete Effects, Energy floor, and Finish completion.
