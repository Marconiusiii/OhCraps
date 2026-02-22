# Milestone 29: Extreme Across (`ea`) Helper

## Goal
Add a new Crapless helper that places across the expanded number set without changing the meaning of existing helper codes.

Your requested behavior is preserved exactly:

- `a` stays standard across helper (4 through 10 behavior)
- `i` stays standard inside helper (5 through 9 behavior)
- `c` stays standard center helper (6 and 8 only)
- new `ea` handles expanded Crapless across from 2 through 12 (excluding 7)

## What changed
File: `OhCraps_Py3.command`

### 1) New helper command
`placePreset(...)` now supports:

- `ea`

In Crapless mode, `ea` places wagers on:

- 2, 3, 4, 5, 6, 8, 9, 10, 11, 12

### 2) Unit sizing for `ea`
Per-number base units used:

- 2 and 12: 2
- 3 and 11: 4
- 4, 5, 9, 10: 5
- 6 and 8: 6

Total across cost is derived from those units times user unit count.

### 3) Existing helpers preserved
In Crapless mode:

- `a`, `i`, and `c` are not remapped to the expanded domain.
- They remain treated as standard-only behaviors.

This keeps existing command meaning stable while adding new expanded functionality with `ea`.

## Why this is safe
Changing the meaning of existing helper codes often causes accidental regressions and user confusion.

By adding `ea` instead:

- no existing helper semantics are overloaded,
- expanded Crapless automation is explicit and testable,
- migration to iOS command/action mapping stays clearer.

## Tests added
File: `tests/testEngineBehavior.py`

Added deterministic coverage for:

- `a` remains non-expanded in Crapless context.
- `i` remains non-expanded in Crapless context.
- `c` remains non-expanded in Crapless context.
- `ea` creates correct wager map and accounting for 2 through 12.

## Runtime verification
Live terminal smoke confirmed:

- In Crapless mode, entering Place -> `ea` -> unit `1` creates:
	- 2:2, 3:4, 4:5, 5:5, 6:6, 8:6, 9:5, 10:5, 11:4, 12:2
- bankroll/table deltas match expected total outlay.

## Next milestone
Re-enable and harden additional Crapless helper automation (if desired) with explicit commands per expanded-domain behavior, while keeping legacy helper meanings unchanged.
