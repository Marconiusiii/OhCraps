# Milestone 22: Terminal Flow Testing and Accounting Safety

## Goal
This milestone closes a specific testing gap:

- We already had solid deterministic tests for engine settlement logic in `engineCore.py`.
- We did not have direct automated coverage for input-driven terminal flow logic in `OhCraps_Py3.command`.
- The recent hard ways save bug occurred in that untested terminal layer.

The goal here is to add deterministic tests for terminal functions and lock bankroll/chips accounting behavior on retry-heavy user input paths.

## Why this matters for the iOS path
An iOS port needs stable game rules and stable state transitions.

- Engine functions give deterministic rule outcomes.
- UI-layer flows still control when bets are replaced, removed, retried, or rejected.
- If UI-layer accounting drifts, iOS can still be wrong even if core rules are correct.

This milestone treats terminal flow as a first-class test surface so later UI adapters can reuse this behavior with confidence.

## Deterministic testing approach used
We need to test interactive functions without launching the full game loop.

### Problem
`OhCraps_Py3.command` starts the live game loop at module runtime. If tests import it directly, tests block waiting for user input forever.

### Solution
The tests now load only the function-definition region of the terminal script:

1. Read `OhCraps_Py3.command` as text.
2. Find the marker `# Game Start`.
3. Execute only source before that marker via `exec(...)` in a dedicated namespace.
4. Patch `builtins.input` with fixed input sequences for each test.
5. Call target terminal functions directly from that namespace.

This keeps tests deterministic and fast while still exercising the real terminal flow code.

## What changed
The following items were added in `tests/testEngineBehavior.py`:

- `loadTerminalNamespace()`
- `TerminalFlowRegressionTests.testHardWaysBettingSavesWager`
- `TerminalFlowRegressionTests.testHardWaysBettingTakeDownReturnsFunds`
- `TerminalFlowRegressionTests.testOddsPassRejectOverMaxRefundsBeforeRetry`
- `TerminalFlowRegressionTests.testOddsDontPassRejectOverMaxRefundsBeforeRetry`
- `TerminalFlowRegressionTests.testPropBettingHiLowRetryPreservesAccounting`

## Bugs found and fixed during this milestone
While adding the tests, three bankroll/chips accounting defects were confirmed and patched.

### 1) Hard Ways press-change accounting drift
Location: `OhCraps_Py3.command`, function `hardCheck(...)`.

Before:
- Old hard-way wager was removed from `chipsOnTable`.
- Old wager was not credited back to `bank` before collecting replacement bet.

Impact:
- Bankroll could silently drift down when changing a winning hard-way wager.

Fix:
- Add `bank += hardWays[hitNumber]` before calling `betPrompt()`.

### 2) Pass odds over-max retry loss
Location: `OhCraps_Py3.command`, function `odds(...)`, Pass branch.

Before:
- Over-max entry in `betPrompt()` had already moved money from `bank` to `chipsOnTable`.
- Retry branch only removed chips, but did not refund bank.

Impact:
- Rejected attempts could reduce bankroll incorrectly.

Fix:
- In over-max branch, refund both sides:
	- `chipsOnTable -= pOddsChange`
	- `bank += pOddsChange`

### 3) Don't Pass lay-odds over-max retry loss
Location: `OhCraps_Py3.command`, function `odds(...)`, Don't Pass branch.

Before:
- Retry branch removed chips but did not return attempted amount to bank.

Fix:
- In over-max branch, refund attempted amount:
	- `chipsOnTable -= dpOddsChange`
	- `bank += dpOddsChange`

## Testing model used in this milestone
Each new test asserts both behavioral and accounting outcomes.

Behavioral examples:
- A hard ways entry is actually stored.
- A takedown actually clears the wager.
- Odds retry accepts valid follow-up after rejecting invalid amount.

Accounting examples:
- `bank` and `chipsOnTable` end at expected exact values after retries.
- Rejected inputs do not create or destroy value.

This is the key protection against the same class of bug returning later.

## Invariants we are now asserting more deliberately
For every interactive flow test, treat these as core checks:

- A rejected wager must be net-zero on bankroll and chips.
- A replacement wager must follow remove-old-then-add-new accounting.
- A takedown must move chips back to bank exactly once.

## How to run this milestone test coverage
From project root:

```bash
python3 -m unittest discover -s tests -p "test*.py"
```

Optional compile check:

```bash
python3 -m py_compile OhCraps_Py3.command engineCore.py tests/testEngineBehavior.py
```

## What this does not do yet
- It does not remove terminal globals.
- It does not convert all terminal flows into pure engine calls.
- It does not replace random live play with full integration simulation.

It does lock the highest-risk interactive accounting paths with deterministic tests and should materially reduce regression risk for the next UI migration steps.

## Next logical follow-up
Build a small adapter layer that converts each user betting action into pure function calls with explicit state in/state out, then reuse these same test patterns on the adapter. That is the cleanest bridge from terminal loop to iOS UI events.

## Milestone 23 addendum: Place and Lay branch coverage
Milestone 23 applied the same deterministic strategy to Place/Lay interactive branches.

### Why this was the right next step
The prior terminal-flow tests locked hard ways and odds retry accounting, but Place/Lay flows still had:

- Large branch count (`a`, `i`, `c`, mover, press variants, takedown).
- Multiple remove-old/add-new transitions.
- Point inclusion/exclusion branches that can silently alter outlay.

These are exactly the kinds of paths that pass casual play testing but fail in edge sequences.

### Additional tests added
In `tests/testEngineBehavior.py`, `TerminalFlowRegressionTests` now also includes:

- `testPlacePresetAcrossExcludePoint`
- `testPlacePresetInsideExcludePoint`
- `testPlacePresetCenterSetsOnlySixAndEight`
- `testPlaceMoverConvertsSixToFiveUnitNumber`
- `testPlaceMoverConvertsFiveUnitNumberToSix`
- `testPlaceCheckFullPressMaintainsAccounting`
- `testPlaceCheckHalfPressUsesNormalizedSixIncrement`
- `testLayAllAcrossSetsEachNumber`
- `testLayBettingTakeDownReturnsFunds`

### Why the assertions are structured this way
Each test checks two things at once:

1. Behavioral correctness:
	- Correct numbers are set/cleared.
	- Correct branch executes based on input sequence.

2. Accounting correctness:
	- `bank` and `chipsOnTable` end at exact expected values.
	- No duplicate debits/credits during replacement flows.

### Important test-fixture lesson
One new test initially failed due to invalid setup:

- It had existing place bets but did not preload `chipsOnTable` to match those live bets.

That was a fixture bug, not game logic. The setup was corrected to realistic state:

- live bets are represented in `chipsOnTable`
- available rack value remains in `bank`

This is a useful rule for future test writing:

- Any test that starts with active bets must initialize `bank` and `chipsOnTable` consistently with those bets before asserting flow behavior.

### Milestone 23 outcome
- No additional game-rule patch was needed in terminal code.
- Coverage increased from 71 to 80 passing tests.
- Place/Lay branch risk is now materially lower, and adapter extraction can proceed with stronger regression protection.
