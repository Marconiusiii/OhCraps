# Milestone 24: Game Mode Scaffold (Craps vs Crapless Craps)

## What this milestone does
This milestone adds game mode selection and mode state storage, but does not change gameplay rules yet.

At startup, before bankroll input, the player now sees:

1. Craps
2. Crapless Craps

The player types `1` or `2`, then the game continues to the bankroll question.

## Why we did it this way
Adding Crapless rules touches many systems:

- Come-out behavior
- Point handling
- Place/Lay number sets
- Payout tables
- Help text and prompts

If we change all of those in one step, the risk of hidden regressions is high.

So this milestone separates concerns:

1. Build mode plumbing first.
2. Verify state and startup flow are stable.
3. Add actual Crapless rule behavior in later milestones behind that scaffold.

This gives safer, predictable iteration.

## Code changes made
### 1) Engine scaffold (`engineCore.py`)
Added:

- `GameMode` enum
	- `craps`
	- `craplessCraps`
- `GameRulesProfile` dataclass
- `parseGameModeChoice(choice)` to map:
	- `1` -> `GameMode.craps`
	- `2` -> `GameMode.craplessCraps`
- `getRulesProfile(gameMode)` to return profile metadata.

### 2) Game state now stores selected mode
`GameState` now includes:

- `gameMode: GameMode = GameMode.craps`

State helpers updated:

- `createGameState(..., gameMode=GameMode.craps)`
- `syncGameState(..., gameMode=None)`

`syncGameState` only updates mode when a mode is explicitly supplied.

### 3) Terminal startup flow (`OhCraps_Py3.command`)
Added `selectGameMode()` and called it before `cashIn()`.

Behavior:

- Shows numeric menu.
- Accepts only `1` or `2`.
- Re-prompts on invalid input.
- Stores chosen mode and syncs it into `gameState`.

## What this milestone intentionally does not change
- No payout changes.
- No Crapless point/come-out behavior changes.
- No Place/Lay domain expansion.
- No rule differences between selected modes yet.

This is deliberate. It keeps this step low risk and easy to validate.

## Deterministic tests added
In `tests/testEngineBehavior.py`:

- Mode parser tests
- Rules profile lookup tests
- `GameState` mode create/sync tests
- Terminal startup selection tests:
	- valid `1`
	- valid `2`
	- invalid then valid retry

These tests make startup mode behavior predictable and regression-resistant.

## Why this is useful for iOS later
An iOS app should not hardcode game rules in UI screens.

By adding mode to engine state now:

- the UI can pick mode once,
- engine state carries that mode through the session,
- later milestones can switch rule behavior from one central state property.

This keeps UI thin and logic centralized, which is the right direction for portability.

## Next milestone focus
Implement the first behavior-level difference between Craps and Crapless using this scaffold:

- mode-aware roll evaluation profile and point behavior
- then mode-aware bet domain/payout updates in later steps.
