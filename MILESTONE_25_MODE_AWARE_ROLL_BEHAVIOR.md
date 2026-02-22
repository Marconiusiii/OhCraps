# Milestone 25: Mode-Aware Roll and Point Behavior

## Goal
Milestone 24 added mode selection and mode state.

Milestone 25 makes mode selection affect gameplay in a controlled way by changing roll outcome classification and point lifecycle behavior.

## What changed in code
### 1) Engine roll classification is now mode-aware
File: `engineCore.py`

`evaluateRoll(gameState, rollValue)` now checks `gameState.gameMode`.

Standard Craps behavior remains exactly as before:

- Come-out 7 or 11 => `natural`
- Come-out 2, 3, or 12 => `craps`
- Other come-out values => `pointEstablished`

Crapless Craps behavior in this milestone:

- Come-out 7 => `natural`
- Any other come-out value => `pointEstablished`

Point phase behavior remains shared in both modes:

- Roll 7 => `sevenOut`
- Roll equals point => `pointHit`
- Otherwise => `neutral`

### 2) Terminal phase control now uses roll outcomes
File: `OhCraps_Py3.command`

Come-out and point-phase transitions now branch on `RollOutcome` values rather than hardcoded roll lists.

This matters because hardcoded `if roll in [7,11]` style logic cannot scale safely once mode-specific rules are introduced.

By routing phase transitions through engine outcomes, mode behavior stays centralized and predictable.

## Why this milestone is safe
This milestone is intentionally narrow:

- It changes only outcome classification and phase branching.
- It does not yet change payout tables.
- It does not yet change place/lay number sets.
- It does not yet lock down bet availability differences for Crapless.

That narrow scope keeps risk low while still making mode selection actually functional.

## Deterministic tests added
File: `tests/testEngineBehavior.py`

Added tests verify:

- Crapless come-out 7 is natural.
- Crapless come-out 11 is point-established (not natural).
- Crapless come-out 2/3/12 are point-established.
- Crapless point-phase still resolves seven-out and point-hit correctly.
- Terminal namespace test confirms mode-aware outcome classification path.

## Important Stratosphere scope note
You requested Stratosphere Crapless standards as the locked target.

This milestone only implements the roll/point foundation needed for that target.

Stratosphere-specific payout mapping and table behavior constraints will be applied in upcoming milestones using this engine-first structure.

## Why this helps iOS migration
For iOS, you want UI to ask for mode once and then rely on engine results.

This milestone moves us in that direction:

- UI selects mode.
- Engine classifies outcomes by mode.
- UI follows returned outcomes to drive phase transitions.

That separation is the right architecture for cross-platform consistency.

## Next milestone
Implement mode-aware line and core bet resolution differences needed for Crapless table behavior, still behind deterministic tests and explicit rule-profile data.
