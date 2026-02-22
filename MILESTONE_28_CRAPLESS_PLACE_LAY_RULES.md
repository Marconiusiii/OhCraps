# Milestone 28: Crapless Place/Lay Rules (Mode-Aware Engine Path)

## Goal
Milestone 27 locked line-bet restrictions for Crapless mode.

Milestone 28 extends that approach to Place and Lay behavior so Crapless sessions have:

- a legal place-number domain,
- deterministic settlement path in engine,
- explicit lay restriction handling.

## What changed
### 1) Engine wrappers for mode-aware settlement
File: `engineCore.py`

Added:

- `settlePlaceBetsForMode(placeBets, roll, gameMode)`
- `settleLayBetsForMode(layBets, roll, gameMode)`

Why wrappers:

- Keep standard Craps behavior untouched.
- Add Crapless behavior in one central place.
- Keep terminal code simpler and easier to port.

### 2) Crapless Place number domain
Crapless Place numbers now include:

- `2, 3, 4, 5, 6, 8, 9, 10, 11, 12`

Terminal place entry now uses mode-aware number list via:

- `validPlaceNumbers()`

### 3) Crapless Place settlement assumptions used
This milestone applies these explicit payout assumptions:

- Place 2 / 12:
	- under 20: `11:2`
	- 20 and above: buy-style `6:1` minus vig on base wager
- Place 3 / 11:
	- under 20: `11:4`
	- 20 and above: buy-style `3:1` minus vig on base wager
- Existing 4/5/6/8/9/10 rules remain as currently implemented in this project.

These values are now encoded in engine settlement, not terminal branching.

### 4) Crapless Lay restriction behavior
Lay in Crapless is treated as unavailable.

Terminal behavior:

- `ly`/Lay menu blocked in Crapless with clear message.

Engine behavior:

- If lay exposure exists anyway, wrapper returns the full amount to bank and clears lay state.

This guarantees deterministic cleanup and prevents illegal state persistence.

### 5) Place input and press normalization updates
In terminal place flow:

- Place 2/12 must be multiples of 2.
- Place 3/11 must be multiples of 4.

Press helpers:

- Unit-size helper added for place numbers.
- Half-press and unit-press now normalize increments for new Crapless edge numbers.

Safety guard:

- Across/Inside/Center presets and place-mover are currently disabled in Crapless mode.
- This avoids invalid auto-sizing while expanded-number math is still staged.

## Tests added
File: `tests/testEngineBehavior.py`

Added coverage for:

- Standard parity:
	- mode wrapper matches canonical Place behavior in Craps mode.
- Crapless Place:
	- Place 2 under buy threshold payout path.
	- Place 3 buy-style payout path with vig.
	- Seven-out clears expanded Place domain.
- Crapless Lay:
	- return-and-clear behavior from settlement wrapper.
- Terminal:
	- Crapless helper/domain checks (`validPlaceNumbers` etc.).

## Why this milestone is important
This is the first milestone where Crapless Place/Lay behavior is both:

- mode-legal at entry,
- engine-owned at settlement.

That combination is critical for predictable play and for later iOS porting, because UI can remain thin and engine remains rule authority.

## Known staged limitations
- Crapless presets (`a`, `i`, `c`) and place-mover are disabled for now in Crapless.
- These can be re-enabled in a future milestone once expanded-domain auto-sizing is finalized and covered by tests.

## Next milestone
Re-enable Crapless Place presets and mover with fully mode-aware sizing math, then add corresponding deterministic regression tests.
