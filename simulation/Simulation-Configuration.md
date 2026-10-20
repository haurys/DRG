# Simulation Configuration

`config.json` is the executable parameter set. Fields ending `_assumption` are non-canonical and appears in output metadata. `difficulty_transition_rule` records the approved canonical boundary behavior. Change seed, player count, or race format without modifying engine code.

The now-canonical `pack_resolution` descriptor records nearest-leader Round Start grouping and fixed round membership. The `will_resolution` descriptor specifies single-use exact shortfall coverage for otherwise legal Pace and Movement-card costs after preservation. It is a rule descriptor, not a balance parameter.

## v1.3 fixed policy

The existing 400-turn maximum remains a safety guard. Assistance uses one requester Treat/Prepare action and zero Race-card plays; the helper has no action debt. A DNF runner is removed from active round decisions. Neither the deck values nor the Pace/Energy configuration changes.

## v1.4 candidate configuration

`starting_hand` is 6 and also the hand ceiling for the single normal Replenish draw; `exchange_limit` remains 3. Deck recycling uses only eligible discard cards, and empty draw plus empty eligible discard skips the draw. Four Pace costs and Movement Energy bands are unchanged.

The marathon's existing Course builder selects 13 of 30 physical two-mile cards and maps their outbound and return one-mile sides to 26 data records (104 quarter-mile spaces). The physical Start/Finish card anchors the end containing mile 1 outbound and mile 26 return. Course Difficulty and station configuration remain unchanged. Gear `is_footwear` is the one-shoe legality field; broad `category` does not constrain installation. A newly played Treat/Prepare card uses one of two card plays; an already-equipped relocation or assistance uses no new card play.
