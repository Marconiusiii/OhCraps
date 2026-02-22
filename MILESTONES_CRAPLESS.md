# Crapless Milestones (Consolidated)

This file is the single running milestone journal for Crapless mode work.
New milestone updates should be appended here rather than creating new milestone files.

## Milestone 24: Game Mode Scaffold

### What changed
- Added mode scaffold in engine (`GameMode`, `GameRulesProfile`, mode parsing/profile helpers).
- Added startup mode selection before bankroll with numeric choices:
	- `1. Craps`
	- `2. Crapless Craps`
- Stored selected mode in game state.

### Why
- Build plumbing first before behavior changes so multi-system updates can be staged safely.

### Scope limits
- No payout/domain behavior changes in this step.

## Milestone 25: Mode-Aware Roll/Point Behavior

### What changed
- `evaluateRoll(...)` became mode-aware:
	- Craps: standard come-out behavior.
	- Crapless: only 7 is a natural on come-out; all other come-out totals establish point.
- Terminal phase transitions switched to `RollOutcome`-driven branching.

### Why
- Makes mode selection behaviorally meaningful with minimal blast radius.

### Scope limits
- No Place/Lay payout matrix changes yet.

## Milestone 26: Resolving Path Stabilization

### What changed
- Fixed first-roll control-flow regression (`outcome` NameError path).
- Added mode-aware line settlement entry wrapper and terminal routing.

### Why
- Ensure Crapless sessions can always progress beyond first roll.

### Scope limits
- Wrapper initially delegated to canonical logic.

## Milestone 27: Crapless Line Rule Enforcement

### What changed
- Enforced no `Don't Pass` / `Don't Pass Odds` in Crapless:
	- Prompt-level rejection in terminal line betting.
	- Engine settlement wrapper returns/clears any existing Don't exposure.

### Why
- First explicit Stratosphere-aligned line constraint in live logic.

### Scope limits
- Non-line families unchanged in this milestone.

## Milestone 28: Crapless Place/Lay Domain + Settlement Path

### What changed
- Added mode-aware Place/Lay settlement wrappers.
- Crapless place domain expanded to `2,3,4,5,6,8,9,10,11,12`.
- Added Crapless place validation for edge-number multiples.
- Disabled Lay in Crapless; any lay exposure is returned/cleared by wrapper.
- Routed terminal place/lay checks through mode-aware wrappers.

### Why
- Move Place/Lay mode behavior into deterministic engine paths.

### Scope limits
- Presets/mover initially constrained in Crapless to avoid invalid auto-sizing.

## Milestone 29: Extreme Across Helper (`ea`)

### What changed
- Kept existing helper meanings unchanged:
	- `a` remains standard across behavior.
	- `i` remains standard inside behavior.
	- `c` remains standard center behavior.
- Added `ea` helper for Crapless Extreme Across on `2,3,4,5,6,8,9,10,11,12`.
- Implemented unit-size based multiplier behavior for `ea`.

### Why
- Add expanded-domain automation without overloading established helper semantics.

### Scope limits
- `a/i/c` intentionally not repurposed for expanded domain.

## Regression Note: Point 11 Win

- Engine line settlement confirms point 11 hit wins in Crapless point phase.
- This behavior is now explicitly locked by tests in the suite.

## Milestone 30: Edge Helper (`e`)

### What changed
- Added new Place helper `e` for edge-only setup in Crapless sessions.
- `e` places wagers only on:
	- `2, 3, 11, 12`
- Unit sizing for `e` uses existing edge unit rules:
	- 2/12: 2-unit base
	- 3/11: 4-unit base

### Preserved behavior
- Existing helpers were not repurposed:
	- `a` unchanged
	- `i` unchanged
	- `c` unchanged
	- `ea` unchanged

### Accounting model
- `e` follows preset-style replacement behavior:
	- clears non-edge place numbers,
	- applies edge wagers from selected unit size,
	- updates bank/chips with deterministic outlay math.

### Test coverage
- Added deterministic tests for:
	- edge-only placement map from `e`,
	- bank/chips invariants,
	- no regression of existing helper behaviors.

## Milestone 31: Restore `a`, `i`, `c` Helpers In Crapless

### What changed
- Removed the Crapless helper gate in `placePreset(pre)` that blocked standard presets.
- Removed the related warning message stating presets were unavailable in Crapless.
- Restored active behavior for original helpers in Crapless mode:
	- `a` runs normal Across sizing on `4,5,6,8,9,10`.
	- `i` runs normal Inside sizing on `5,6,8,9`.
	- `c` runs normal Center sizing on `6,8`.
- Kept Crapless-only helpers intact:
	- `ea` for Extreme Across `2,3,4,5,6,8,9,10,11,12`.
	- `e` for edges `2,3,11,12`.

### Why
- You requested parity with original helper workflows in Crapless and removal of the blocking gate text.

### Test coverage
- Replaced the prior Crapless "disabled" tests for `a/i/c` with active behavior tests.
- New assertions verify resulting place map plus `bank` and `chipsOnTable` totals for each helper.

## Milestone 32: Crapless Helper Integration Coverage

### What changed
- Added integration-style terminal regression tests for Crapless helper flows.
- New coverage verifies original helpers in Crapless through real preset calls:
	- `a` with point exclusion path (`pointIsOn` + "Include the Point?" = no).
	- `i` with point exclusion path.
- Added sequential helper replacement coverage in one session:
	- `a` then `e` then `ea` with final map/accounting assertions.
- Added guard coverage for current place mover behavior in Crapless:
	- confirms mover remains disabled and does not mutate bankroll/table/place state.
- Added press-path integration check after helper setup:
	- `c` helper setup followed by `hp` on a winning 8, with normalized increment and accounting assertions.

### Why
- Unit checks were already present, but helper/menu interactions still carried risk in point-phase and sequential replacement flows.
- This milestone locks the high-risk user paths most likely to regress while expanding Crapless behavior.

### Test impact
- Test suite now includes these additional deterministic cases under `tests/testEngineBehavior.py`.
- Full suite remains green after additions.

## Milestone 33: Crapless Edge Place Payout Matrix Lock

### What changed
- Added deterministic payout matrix tests for Crapless edge Place numbers (`2, 3, 11, 12`).
- Added explicit coverage for three payout bands:
	- under buy-threshold behavior,
	- threshold behavior where buy/vig starts,
	- above-threshold behavior with vig rounding.
- Added assertions that on winning Place hits:
	- only winnings are added to bank,
	- chips-on-table delta stays unchanged,
	- original Place wager remains up.

### Why
- Edge-number Place bets are the highest-risk payout area in Crapless and needed exact regression locks.
- Matrix tests reduce risk of silent payout drift while refactoring toward iOS-ready architecture.

### Rule mapping notes
- Current implementation profile (as coded) is now explicitly locked by tests:
	- Place 2/12 under threshold uses 11-for-2 style payout.
	- Place 3/11 under threshold uses 11-for-4 style payout.
	- Buy-style payout activates at `>= 20` for edge numbers.
	- Vig uses existing commission rounding in engine (`calculateVig`).

### Test coverage summary
- Added three new test methods in `tests/testEngineBehavior.py`:
	- `testSettlePlaceBetsForModeCraplessEdgeNumbersUnderBuyThresholdMatrix`
	- `testSettlePlaceBetsForModeCraplessEdgeNumbersBuyThresholdMatrix`
	- `testSettlePlaceBetsForModeCraplessEdgeNumbersBuyVigRoundingMatrix`
- Full suite remains green.

## Milestone 34: Mode-Aware Place Helper Commands And Help Text

### What changed
- Added centralized mode-aware Place helper command list:
	- `validPlacePresetCodesForMode()`
- Added centralized Place help text generator:
	- `placeHelpText(pointPhase=False)`
- Updated both Place betting loops (come-out and point phase) to use mode-aware helper dispatch.
- Added explicit invalid-option feedback in the come-out Place loop for safer command handling.
- Added mode-safe validation at the start of `placePreset(pre)`:
	- rejects presets not valid for the current game mode,
	- prevents bet/accounting mutation on invalid helper commands.

### Why
- Place helper discoverability and command handling needed to be deterministic and mode-correct.
- This removes ambiguity about which helper codes are valid in each game type.

### Behavior now
- Craps mode valid helper presets: `a`, `i`, `c`
- Crapless mode valid helper presets: `a`, `i`, `c`, `e`, `ea`
- Entering helper presets not valid for the current mode is ignored safely with a message.

### Test coverage
- Added deterministic tests in `tests/testEngineBehavior.py`:
	- `testValidPlacePresetCodesForModeCraps`
	- `testValidPlacePresetCodesForModeCrapless`
	- `testPlacePresetEdgeRejectedInCrapsNoMutation`
	- `testPlacePresetExtremeAcrossRejectedInCrapsNoMutation`
	- `testPlaceHelpTextIsModeAware`
- Full suite remains green.

## Milestone 35: Extract Place Command Dispatcher

### What changed
- Added a dedicated Place command dispatcher:
	- `handlePlaceMenuCommand(command, pointPhase=False)`
- Moved Place command branching logic out of both terminal loops into that shared handler.
- Updated both Place menus (come-out and point phase) to call dispatcher and act on returned command result.

### Dispatcher contract
- Returns a dict with:
	- `handled`: whether command was recognized/executed.
	- `shouldExitMenu`: whether caller should break Place menu loop.
- Keeps existing behavior for all commands:
	- Common: `y`, `d`, helper presets, `h`, `x`
	- Point-only: `o`, `m`, `p`
- Invalid commands still fail safely without mutating table state.

### Why
- This reduces duplicate control flow and makes Place command handling deterministic and testable.
- It is a direct step toward iOS portability by isolating command intent from loop/UI structure.

### Test coverage
- Added deterministic dispatcher tests in `tests/testEngineBehavior.py`:
	- `testHandlePlaceMenuCommandExit`
	- `testHandlePlaceMenuCommandPointTogglePlaceOff`
	- `testHandlePlaceMenuCommandPointOnlyIgnoredOnComeOut`
	- `testHandlePlaceMenuCommandInvalidNoMutation`
- Full suite remains green.

## Milestone 36: Extract Lay And Hard Ways Command Dispatchers

### What changed
- Added shared Lay command dispatcher:
	- `handleLayMenuCommand(command, pointPhase=False)`
- Added shared Hard Ways command dispatcher:
	- `handleHardWaysMenuCommand(command, pointPhase=False)`
- Added centralized help text builders:
	- `layHelpText(pointPhase=False)`
	- `hardWaysHelpText(pointPhase=False)`
- Replaced duplicated Lay/Hard command branches in both:
	- initial betting phase menus,
	- point-phase betting menus.

### Behavior preserved
- Lay command coverage: `y`, `a`, `d`, `h`, `x`, plus point-only `o`.
- Hard Ways command coverage: `y`, `a`, `d`, `h4/h6/h8/h10`, `h`, `x`, plus point-only `o`.
- Crapless Lay restriction is enforced in one dispatcher path.
- Invalid command paths remain no-op on bankroll/table state.

### Why
- Removes duplicated command parsing logic and centralizes menu behavior.
- Improves determinism and testability, which is needed for iOS view/controller extraction.

### Test coverage
- Added deterministic dispatcher tests in `tests/testEngineBehavior.py`:
	- `testHandleLayMenuCommandExit`
	- `testHandleLayMenuCommandPointToggle`
	- `testHandleLayMenuCommandCraplessGuardExits`
	- `testHandleLayMenuCommandInvalidNoMutation`
	- `testHandleHardWaysMenuCommandExit`
	- `testHandleHardWaysMenuCommandPointToggle`
	- `testHandleHardWaysMenuCommandInvalidNoMutation`
- Full suite remains green.

## Milestone 37: Crapless Come Odds Structure Fix

### What changed
- Added mode-aware Come odds limit function in engine:
	- `maxComeOddsForMode(number, baseBet, gameMode)`
- Kept `maxComeOdds(...)` as standard wrapper for backward compatibility.
- Extended Come table settlement to be mode-aware:
	- `settleComeTableBets(..., gameMode=GameMode.craps)`
- Added mode-aware Come number domain helper:
	- `comeNumbersForMode(gameMode)`
- Updated Come settlement loops to include Crapless edge points (`2, 3, 11, 12`) when in Crapless mode.
- Added Come odds payout handling for Crapless edge numbers:
	- Come 2/12 odds pay `6:1`
	- Come 3/11 odds pay `3:1`
- Added mode-aware Come bar handling:
	- `settleComeBarBet(..., gameMode=GameMode.craps)`
	- In Crapless: Come wins only on 7; all other totals move to numbers.

### Terminal integration
- Updated terminal to call mode-aware Come odds limit function in both odds entry paths.
- Updated terminal Come bar settlement call to pass `gameMode`.
- Updated terminal Come table settlement call to pass `gameMode`.
- Expanded terminal Come/Don't Come dictionaries to include edge keys (`2, 3, 11, 12`) so Crapless odds and settlements are tracked safely.

### Why
- Come odds behavior in Crapless was still using standard Craps constraints and number sets.
- This caused incorrect max-odds and settlement behavior for edge points.

### Test coverage
- Added deterministic tests for:
	- Crapless Come bar movement on 11 and 2.
	- Mode-aware max Come odds for edge numbers.
	- Crapless Come odds payouts for 11 and 2 hits.
- Full suite remains green.

## Milestone 38: Centralize Come Odds Policy Helpers

### What changed
- Added mode-aware odds helpers in engine:
	- `comeOddsWinForMode(number, oddsBet, gameMode)`
	- `dComeOddsWinForMode(number, oddsBet, gameMode)`
- Refactored Come odds settlement in `settleComeTableBets(...)` to use helper functions instead of inline branch payout logic.
- Refactored Come bet normalization to be mode-aware by number domain:
	- `normalizeComeBets(comeBets, numbers=None)`
- Kept number-domain policy centralized via `comeNumbersForMode(gameMode)`.

### Why
- Odds policy was spread across inline branches, which increases risk for regression and future rule extension.
- Centralizing payout and domain policy improves predictability and makes iOS service-layer extraction easier.

### Behavior
- No functional gameplay change intended; this milestone is structural normalization.
- Existing Craps and Crapless payout behavior remains locked by tests.

### Test coverage
- Added direct helper tests in `tests/testEngineBehavior.py`:
	- `testComeOddsWinForModeStandardAndCrapless`
	- `testDComeOddsWinForModeStandardAndCrapless`
- Existing Come odds settlement tests remain passing.
- Full suite remains green.

## Milestone 39: Odds Unit Validation Normalization

### What changed
- Added engine policy helpers for odds entry units:
	- `comeOddsUnitForMode(number, gameMode)`
	- `dComeOddsUnitForMode(number, gameMode)`
	- `isOddsBetUnitValid(number, oddsBet, gameMode, isDont=False)`
- Integrated unit validation into terminal odds entry paths:
	- `cdcOddsChange(...)`
	- immediate Come odds prompt after Come bet moves
	- immediate Don't Come lay-odds prompt after Don't Come bet moves

### Rule effect
- Odds values that do not match allowed increments are now rejected at input time.
- Existing payout math is unchanged; this milestone prevents invalid wager shapes before settlement.

### Why
- This removes truncation-style artifacts caused by off-unit odds amounts.
- It improves consistency between what users can enter and what settlement logic expects.

### Test coverage
- Added engine-level unit tests:
	- `testComeOddsUnitsByMode`
	- `testDComeOddsUnitsByMode`
	- `testIsOddsBetUnitValidByMode`
- Added terminal validation tests:
	- `testCdcOddsChangeRejectsInvalidComeOddsUnitInCraps`
	- `testCdcOddsChangeRejectsInvalidDontComeOddsUnitInCrapless`
- Full suite remains green.

## Milestone 40: Terminal Bet-State Snapshot Adapter

### What changed
- Added terminal state snapshot helpers:
	- `captureBetSnapshot()`
	- `applyBetSnapshot(snapshot)`
- Snapshot includes high-mutation bet/accounting state:
	- `bank`, `chipsOnTable`
	- `comeBet`, `dComeBet`
	- `comeBets`, `dComeBets`, `comeOdds`, `dComeOdds`
	- `place`, `layBets`, `hardWays`, `fieldBet`
- Refactored settlement application paths to use snapshot read/write:
	- `comePay(...)`
	- `placeCheck(...)`
	- `layCheck(...)`
	- `hardCheck(...)`
	- `fieldCheck(...)`

### Why
- This reduces direct global mutation spread and creates explicit synchronization points.
- It is a practical intermediate step toward extracting a portable state/controller layer for iOS.

### Behavior
- No intended gameplay rule changes.
- Settlement deltas and prompt flows remain functionally equivalent.

### Test coverage
- Added deterministic snapshot tests in `tests/testEngineBehavior.py`:
	- `testBetSnapshotCaptureApplyRoundTrip`
	- `testSnapshotApplyWithPlaceSettlementPreservesOtherBets`
- Full suite remains green.

## Milestone 41: Come Subsystem Action-Result Pattern

### What changed
- Added lightweight action-result helpers in terminal code:
	- `createActionResult(success=True, messages=None, stateChanged=False)`
	- `mergeActionResult(baseResult, newResult)`
	- `emitActionResult(actionResult)`
- Extracted Come post-roll command processing into:
	- `processComePostRollAction(roll)`
- Refactored `comeCheck(roll)` to:
	- execute `comePay(roll)`,
	- process post-roll Come/Don't Come bar actions via structured result,
	- emit aggregated messages,
	- return action-result object.

### Why
- Moves Come command handling toward structured, testable command outcomes instead of implicit print/mutate flow.
- Improves portability for future non-terminal UI layers (including iOS) where action results can be rendered by view logic.

### Behavior
- Gameplay/accounting behavior remains unchanged.
- Existing prompts and user decisions are preserved.

### Test coverage
- Added deterministic tests:
	- `testCreateActionResultShape`
	- `testComeCheckReturnsActionResultForMovedComeBet`
	- `testComeCheckReturnsNoChangeActionResultWhenNoBarBets`
- Full suite remains green.

## Milestone 42: Normalize Menu Handlers To Action-Result Contract

### What changed
- Upgraded command handlers to return structured action-result payloads:
	- `handlePlaceMenuCommand(...)`
	- `handleLayMenuCommand(...)`
	- `handleHardWaysMenuCommand(...)`
- Each handler now returns:
	- `success`
	- `messages`
	- `stateChanged`
	- `shouldExitMenu`
- Updated menu loop call sites to emit handler messages centrally via:
	- `emitActionResult(commandResult)`

### Why
- Aligns subsystem command handlers under one result contract.
- Reduces direct print side-effects inside handlers and improves portability to non-terminal UIs.

### Behavior
- Gameplay and menu semantics remain unchanged.
- Exit and invalid-command behavior is preserved.

### Test coverage
- Updated handler tests to assert new action-result fields instead of legacy `handled` key.
- Existing no-mutation and exit-path tests remain passing under the new contract.
- Full suite remains green.

## Regression Fix: Come Odds Prompt Order And Number Context

### Issue
- Come odds prompt appeared before movement messaging in Come flow.
- Come odds prompt text no longer identified rolled number context.

### Fix
- In `processComePostRollAction(roll)`:
	- movement + max-odds reminder now prints immediately before odds decision prompt,
	- odds prompt now includes rolled number (`Odds on your Come N? >`).
- Prevented duplicate delayed movement messaging in aggregated action-result output.
- Left Don't Come flow unchanged.

### Locked behavior order
1. roll outcome reaches Come bar handling,
2. movement message with max-odds reminder is shown,
3. odds prompt on rolled number is shown.

### Test coverage
- Added regression test:
	- `testComeCheckPrintsMoveReminderBeforeOddsPromptWithNumber`
- Updated prior action-result test to align with immediate movement message emission path.
- Full suite remains green.

## Milestone 43: Unify Odds Limits And Prompt Semantics

### What changed
- Added engine helper:
	- `oddsBetLimits(number, baseBet, gameMode, isDont=False)`
	- Returns: `rawMax`, `effectiveMax`, `unit`.
- Switched terminal odds entry paths to consume this helper:
	- `odds()` (Pass and Don't Pass)
	- `cdcOddsChange(...)` (Come/Don't Come odds edits)
	- `processComePostRollAction(...)` (post-move Come/Don't Come odds)
- Standardized odds prompts to always show:
	- target number,
	- effective max (enterable under unit rules),
	- required multiple increment.

### Why
- Removes split logic where one path computed max and another enforced unit multiples.
- Prevents user-facing contradictions such as displaying a max that cannot be entered.
- Consolidates odds constraints into deterministic engine logic, improving iOS portability.

### Behavior changes
- Pass and Don't Pass odds now enforce increment units in `odds()` the same way Come/Don't Come already did.
- Displayed max values now align to the highest valid amount for the required unit.
- Come and Don't Come prompts now follow the same effective-max + multiples format.

### Test coverage
- Added engine-level tests for `oddsBetLimits(...)`.
- Added terminal regression tests for:
	- Pass odds unit rejection/retry,
	- Don't Pass effective-max rejection/retry,
	- updated Come/Don't Come prompt text expectations.
- Full suite remains green.

## Milestone 44: Crapless Place Edge Matrix Hardening

### What changed
- Expanded deterministic engine tests for Crapless Place edge numbers (`2, 3, 11, 12`) to cover additional vig-rounding boundaries.
- Added mixed seven-out matrix coverage for Crapless place books with both edge and core numbers at varied wager sizes.
- Added terminal-flow checks that confirm Buy confirmation messaging appears for high-edge wagers on `11` and `12`.

### Why
- Edge-number place rules have been a repeated regression hotspot.
- This closes remaining gaps where previous tests covered only part of the edge buy/rounding space.
- Strengthens confidence before iOS-port-focused refactors.

### Behavior
- No gameplay rule changes in this milestone.
- This milestone is test and verification hardening only.

### Test coverage
- Added/expanded tests in `tests/testEngineBehavior.py` for:
	- `2/12` and `3/11` vig rounding symmetry on buy payouts.
	- mixed large Crapless seven-out clearing and accounting.
	- terminal Buy messaging on `11` and `12` at `$20+`.
- Full suite remains green.

## Milestone 45: Crapless Edge Press/Half-Press Determinism

### What changed
- Added deterministic terminal tests for Crapless Place edge-number press behavior on `2` and `3`.
- Covered both:
	- half-press normalization (unit-aware increment behavior),
	- full-press accounting after a buy-threshold hit.

### Why
- Press/half-press is a high-regression path due to combined payout, normalization, and bankroll/chips updates in one flow.
- Edge numbers in Crapless have different unit behavior from standard center numbers, so explicit coverage is required.

### Test coverage
- Added tests in `tests/testEngineBehavior.py` for:
	- `Place 2` half-press normalization and accounting,
	- `Place 3` half-press normalization and accounting,
	- `Place 2` full-press accounting after buy-style settlement.
- Full suite remains green.

## Milestone 46: Post-Hit Manual Place Edit Threshold Enforcement

### What changed
- Added a shared validator in terminal flow for place amounts:
	- `isPlaceAmountAllowed(number, bet)`
- Applied this validator to both:
	- initial `placeBets()` entry,
	- post-hit manual change path in `placeCheck(...)` when `press == 'y'`.

### Why
- Threshold rules for Crapless edge numbers (`2,3,11,12`) were previously enforced in initial entry, but not in post-hit manual change edits.
- This could allow under-`$20` invalid non-multiple edits after a hit, creating inconsistent behavior.

### Behavior
- Under `$20`, edge-number manual changes now require valid multiples.
- At `$20+`, edge-number manual changes accept non-multiple amounts (auto-buy threshold path).
- Invalid manual edits are rejected with immediate retry and refunded wager before reprompt.

### Test coverage
- Added deterministic tests in `tests/testEngineBehavior.py` for:
	- under-`$20` invalid-then-valid manual change flow,
	- `$20+` non-multiple manual change acceptance.
- Full suite remains green.

## Milestone 47: Buy Messaging Consistency Coverage

### What changed
- Added deterministic terminal tests for place buy messaging at threshold boundaries.
- Covered standard Craps auto-buy messaging for `4` and `10` at `$10+`.
- Covered non-buy messaging for standard `4` below threshold.
- Preserved existing Crapless edge buy messaging coverage at `$20+`.

### Why
- Messaging consistency is a frequent regression vector even when payout math is correct.
- Deterministic text checks improve confidence for future UI-layer ports where messages may be mapped directly to UX surfaces.

### Test coverage
- Added tests in `tests/testEngineBehavior.py` for:
	- standard `4/10` buy text at threshold,
	- standard `4` non-buy text below threshold.
- Full suite remains green.

## Milestone 48: Player-Facing Rules Text Alignment

### What changed
- Updated README game-instructions wording for Place and Odds so it matches live table behavior in both Craps and Crapless.
- Clarified Crapless edge-number Place flow from a player perspective:
	- under `$20` table-step sizing on `2/3/11/12`,
	- auto-buy handling at `$20+` with vig.
- Clarified Pass Odds limits in Crapless for edge points (`2/12` and `3/11`).
- Kept all wording player-facing and table-oriented.

### Why
- Gameplay behavior had moved ahead of user instructions in a few key spots.
- Aligning instructions to table behavior reduces confusion during live play and testing.

### Test coverage
- No rules or payout logic changed in this milestone.
- Existing automated suite remains green after documentation updates.
