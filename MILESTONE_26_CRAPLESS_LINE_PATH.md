# Milestone 26: Crapless Resolving Path and First-Roll Stability

## What was wrong
After Milestone 25, there was a runtime traceback when starting Crapless and making the first roll:

- `NameError: name 'outcome' is not defined`

This was not expected behavior.

## Why it happened
The `comeOut = roll()` and `outcome = evaluateRoll(...)` lines were in the wrong control-flow position.

They were effectively outside the live path that follows betting-loop exit, while downstream code still expected `outcome` to exist.

So when the game reached the first roll branch, it referenced `outcome` before assignment.

## What this milestone changed
### 1) First-roll control flow fixed
File: `OhCraps_Py3.command`

- Restored roll/evaluate lines to the correct post-betting location:
	- roll dice
	- evaluate roll outcome
	- then process come-out branch

Result:

- First roll now resolves without traceback.
- Both mode selections can progress past come-out.

### 2) Mode-aware line settlement entry point added
File: `engineCore.py`

Added:

- `settleLineBetsForMode(...)`

Current behavior:

- Craps: delegates to `settleLineBets(...)`
- Crapless: currently also delegates to `settleLineBets(...)`

This may look redundant now, but it is intentional.

It creates one central function where Stratosphere-specific Crapless line rules can be implemented next without touching every terminal branch.

### 3) Terminal now calls the mode-aware line wrapper
File: `OhCraps_Py3.command`

`lineCheck(...)` now calls `settleLineBetsForMode(...)` instead of directly calling `settleLineBets(...)`.

That means the runtime path is now prepared for upcoming mode-specific line behavior.

## What this milestone does not yet do
- It does not yet apply full Stratosphere Crapless line payout/push/win/loss policy differences.
- It does not yet modify place/lay domains for Crapless.

Those come next, now that the path is stable.

## Tests added
File: `tests/testEngineBehavior.py`

Added:

- `testSettleLineBetsForModeCrapsMatchesCanonical`
- `testSettleLineBetsForModeCraplessUsesResolvablePath`
- `testCraplessFirstRollPathDoesNotRaiseNameError`

These tests confirm:

- wrapper behavior is callable in both modes,
- and first-roll Crapless flow has a stable resolving path.

## Why this is important for your question
You asked whether there is at least a resolving path for Crapless gameplay.

After this milestone, yes:

- the immediate first-roll crash path is fixed,
- and line settlement is mode-routable through a dedicated function.

That is the minimum stable base needed before applying stricter Stratosphere table behavior in the next milestone.
