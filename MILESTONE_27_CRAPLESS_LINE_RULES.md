# Milestone 27: Stratosphere Crapless Line Rule Enforcement

## Goal
This milestone applies the first strict table-rule behavior for Crapless mode:

- Don't Pass and Don't Pass Odds are not allowed in Crapless.

This is the first step from "mode scaffold" into concrete Stratosphere-style gameplay constraints.

## What changed
### 1) Engine line settlement now has a mode-specific entry path
File: `engineCore.py`

Added:

- `settleLineBetsForMode(lineBets, pointIsOn, roll, p2roll, gameMode)`

Behavior now:

- `GameMode.craps`:
	- uses existing canonical `settleLineBets(...)` behavior unchanged.
- `GameMode.craplessCraps`:
	- refunds any active Don't Pass and Don't Pass Odds amounts,
	- clears those bets from table state,
	- settles Pass Line outcomes only.

This keeps mode differences in engine logic, where they are testable and deterministic.

### 2) Terminal line prompt now enforces the Crapless constraint
File: `OhCraps_Py3.command`

In `lineBetting()`:

- If mode is Crapless and player tries a Don't Pass command, the game prints a rejection message and does not place the bet.

In `lineCheck()`:

- Settlement now routes through `settleLineBetsForMode(...)`.

## Why this is safe
This change is intentionally narrow:

- It does not alter place/lay domains yet.
- It does not change non-line payout families yet.
- It enforces one rule with deterministic tests and centralized engine ownership.

This reduces risk while still making Crapless behavior meaningfully different in live play.

## Tests added
File: `tests/testEngineBehavior.py`

Added coverage for:

- Standard mode parity:
	- wrapper output matches canonical line settlement for Craps.
- Crapless line enforcement:
	- existing Don't Pass / Don't Pass Odds are returned and cleared.
	- come-out 11 leaves Pass working (point-established path remains).
- Terminal prompt rule:
	- line-bet flow rejects Don't Pass entry in Crapless mode.

## Practical result
After this milestone:

- Crapless has a stable first-roll path (from Milestone 26),
- and now has explicit line-rule enforcement consistent with Stratosphere-style "no Don't line action" constraints.

## Next milestone
Apply the next Stratosphere-specific Crapless table updates to bet domains and payouts (Place/Lay and related constraints), while preserving deterministic invariants and tab-indented terminal behavior.
