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

## Milestone 49: Shared Betting Command Router

### What changed
- Added shared betting router helpers in terminal flow:
	- `runPlaceMenu(pointPhase=...)`
	- `runLayMenu(pointPhase=...)`
	- `runHardWaysMenu(pointPhase=...)`
	- `handleBettingCommand(command, pointPhase=...)`
- Replaced duplicated Come Out and Point phase command branches with the shared router.
- Preserved existing command vocabulary and player-facing prompt text.

### Why
- Come Out and Point phase menus had duplicated command-routing code.
- Duplication increases regression risk when one branch is updated and the other is not.
- A shared router is a direct portability step for future iOS controller extraction.

### Behavior
- No payout-rule changes.
- No bet math changes.
- No command removals.
- Roll triggers remain:
	- Come Out: `x` or `r`
	- Point phase: `x` or `r`

### Test coverage
- Added terminal routing regression tests in `tests/testEngineBehavior.py` for:
	- Place menu routing in Come Out.
	- Place menu routing in Point phase.
	- Point-phase roll command returns roll intent.
	- Point-phase odds command with no line bet keeps proper guard message.

## Milestone 50: Come Out And Point Roll Orchestrators

### What changed
- Extracted Come Out roll resolution into `resolveComeOutRoll()`.
- Extracted Point-phase roll resolution into `resolvePointRoll()`.
- Rewired the main game loop to call these orchestrators instead of inline roll-resolution blocks.
- Preserved existing command prompts and payout paths while reducing nested loop complexity.

### Why
- Roll-resolution logic was embedded directly in the main loop with large duplicated state-sync/settlement sequences.
- Extracting deterministic orchestrators reduces control-flow risk and makes a future iOS controller layer easier to map.

### Behavior
- No payout-rule changes.
- No table-rule changes.
- Point transitions and round resets still follow existing logic:
	- Come Out naturals/craps continue to next Come Out.
	- Point established enters point phase.
	- Seven out and point hit both end point phase.

### Test coverage
- Added terminal orchestration tests in `tests/testEngineBehavior.py` for:
	- `resolveComeOutRoll()` natural path (including throw reset on 7).
	- `resolveComeOutRoll()` point-established path.
	- `resolvePointRoll()` seven-out point-end path.
	- `resolvePointRoll()` neutral roll continuation path, including one-roll Off flag reset behavior.
- Full suite and compile checks remain green.

## Milestone 51: Point-Phase Menu Extraction

### What changed
- Extracted point-phase betting prompt loop into `runPointPhaseBettingMenu()`.
- Replaced inline point-phase betting prompt loop in main game flow with a call to the new function.
- Kept point-phase command routing through `handleBettingCommand(..., pointPhase=True)`.

### Why
- The point-phase prompt loop still lived inline in the top-level game coordinator.
- Extracting this loop reduces top-level nesting and isolates one more UI-loop responsibility for eventual iOS controller mapping.

### Behavior
- No payout-rule changes.
- No command changes.
- Point-phase betting menu still loops until a roll command is entered.

### Test coverage
- Added terminal tests in `tests/testEngineBehavior.py` for:
	- loop-until-roll behavior in `runPointPhaseBettingMenu()`.
	- explicit `pointPhase=True` routing to `handleBettingCommand(...)`.
- Compile and full suite remain green.

## Milestone 52: Come Out Menu Extraction

### What changed
- Extracted Come Out betting prompt loop into `runComeOutBettingMenu()`.
- Replaced inline Come Out betting prompt loop in main game flow with a call to the new function.
- Kept Come Out command routing through `handleBettingCommand(..., pointPhase=False)`.

### Why
- Come Out betting prompt logic remained inline while point-phase prompt logic had already been extracted.
- This keeps phase menu structure symmetric and further simplifies the top-level coordinator for iOS-port readiness.

### Behavior
- No payout-rule changes.
- No command changes.
- Come Out betting menu still loops until a roll command is entered.

### Test coverage
- Added terminal tests in `tests/testEngineBehavior.py` for:
	- loop-until-roll behavior in `runComeOutBettingMenu()`.
	- explicit `pointPhase=False` routing to `handleBettingCommand(...)`.
- Compile and full suite remain green.

## Milestone 53: Point-Phase Status Presenter Extraction

### What changed
- Extracted point-phase status rendering into `showPointPhaseStatus()`.
- Replaced inline point-phase status block in main game flow with the new helper call.
- Preserved existing output order:
	- bankroll/chips line,
	- out-of-money guard,
	- point banner,
	- throws line.

### Why
- The top-level point-phase loop still contained repeated status-display and guard logic.
- Pulling that into one function reduces coordinator complexity and isolates terminal-presenter behavior for future UI mapping.

### Behavior
- No payout-rule changes.
- No command changes.
- No text wording changes intended for point-phase status output.

### Test coverage
- Added terminal tests in `tests/testEngineBehavior.py` for:
	- status output with chips on table.
	- zero-bank/zero-table path calling `outOfMoney()` and still rendering point/throws lines.
- Compile and full suite remain green.

## Milestone 54: Point-Phase Round Coordinator Extraction

### What changed
- Extracted full point-phase round loop into `runPointPhaseRound()`.
- Replaced inline point-phase round loop in main flow with a call to the coordinator.
- Kept coordinator internals delegated to existing helpers:
	- `showPointPhaseStatus()`
	- `runPointPhaseBettingMenu()`
	- `resolvePointRoll()`

### Why
- Even after menu/status extraction, the top-level loop still directly owned point-phase round control flow.
- This extraction further isolates gameplay orchestration from top-level script flow and improves portability to an iOS controller structure.

### Behavior
- No payout-rule changes.
- No command changes.
- Point-phase round still repeats until a point-ending roll result occurs.

### Test coverage
- Added terminal tests in `tests/testEngineBehavior.py` for:
	- immediate round end path in `runPointPhaseRound()`.
	- multi-iteration neutral-then-end path in `runPointPhaseRound()`.
- Compile and full suite remain green.

## Milestone 55: Come Out Round Coordinator Extraction

### What changed
- Extracted full Come Out round flow into `runComeOutRound()`.
- Replaced inline main-loop Come Out round sequence with a single coordinator call.
- Kept coordinator internals delegated to existing helpers:
	- `runComeOutBettingMenu()`
	- `resolveComeOutRoll()`

### Why
- Come Out round control still lived inline while point-phase round had already been extracted.
- This makes phase orchestration symmetric and keeps the top-level loop focused on phase transitions only.

### Behavior
- No payout-rule changes.
- No command changes.
- Come Out round still follows the same branch outcomes:
	- continue Come Out if no point is entered,
	- transition into point phase when point is established.

### Test coverage
- Added terminal tests in `tests/testEngineBehavior.py` for:
	- continue-path result from `runComeOutRound()`.
	- enter-point result from `runComeOutRound()`.
- Compile and full suite remain green.

## Milestone 56: Typed Round Transition Results

### What changed
- Added typed transition classes in terminal flow:
	- `comeOutRollResult`
	- `pointRollResult`
	- `comeOutRoundResult`
	- `pointPhaseRoundResult`
- Replaced dict-based transition returns with typed objects for:
	- `resolveComeOutRoll()`
	- `resolvePointRoll()`
	- `runComeOutRound()`
	- `runPointPhaseRound()`
- Updated top-level callers and tests to use attribute access instead of string-key indexing.

### Why
- String-key dict transitions are fragile and make orchestration logic harder to reason about.
- Typed transition objects improve clarity, reduce typo risk, and better match iOS controller/state modeling patterns.

### Behavior
- No payout-rule changes.
- No command changes.
- No prompt text changes.
- Round/phase transition behavior is unchanged.

### Test coverage
- Updated existing round/roll orchestration tests in `tests/testEngineBehavior.py` to assert against typed result attributes.
- Compile and full suite remain green.

## Milestone 57: Orchestrator IO Adapter Boundary

### What changed
- Added terminal I/O wrapper helpers:
	- `writeOutput(message)`
	- `readInput(promptText)`
- Migrated orchestrator-level prompt/display functions to use wrappers:
	- `runComeOutBettingMenu()`
	- `runPointPhaseBettingMenu()`
	- `showPointPhaseStatus()`
- Kept all player-facing prompt text unchanged.

### Why
- Direct `print/input` calls are a key portability blocker for non-terminal UIs.
- A thin adapter boundary makes orchestration easier to retarget for iOS without touching rule logic.

### Behavior
- No payout-rule changes.
- No command changes.
- No prompt wording changes.

### Test coverage
- Updated menu tests to patch `readInput`/`writeOutput` adapter functions directly.
- Added explicit adapter usage test for `showPointPhaseStatus()` output flow.
- Compile and full suite remain green.

## Milestone 58: Typed Betting Command Result

### What changed
- Added typed command result class:
	- `bettingCommandResult(shouldRoll, handled)`
- Updated `handleBettingCommand(...)` to return `bettingCommandResult` instead of dicts.
- Updated orchestrator menu callers to read `commandResult.shouldRoll`.
- Updated deterministic tests to assert typed command result attributes and use typed fake command results.

### Why
- Dict-key command control results were fragile and less explicit in orchestration paths.
- Typed command results improve readability, reduce key-typo risk, and align with iOS controller modeling patterns.

### Behavior
- No payout-rule changes.
- No command routing changes.
- No prompt wording changes.

### Test coverage
- Updated command-handler and menu-loop tests in `tests/testEngineBehavior.py` to use typed command results.
- Compile and full suite remain green.

## Milestone 59: Line Odds Prompt Language Normalization

### What changed
- Updated Pass Line Odds prompt wording in `odds()` to:
	- initial: `Odds on the $point?`
	- existing odds: `You have $amount in Odds for the $point. How much for your Odds?`
- Updated Don't Pass/Lay Odds prompt wording in `odds()` to:
	- initial: `Lay Odds against the $point?`
	- existing odds: `You have $amount laid against the $point. How much do you want to Lay?`
- Added max reminder as a separate line:
	- `Max odds is $maxOdds.`
- Multiples reminder now appears only when unit is not 1:
	- `Multiples of $unit.`
- Updated Lay take-down confirmation message to:
	- `Taking down your Lay Odds.`

### Why
- Prompt language needed to match requested table wording and reduce clutter.
- Always printing `multiples of 1` is noisy and not useful to players.

### Behavior
- No payout-rule changes.
- No odds-limit logic changes.
- No bankroll/chips accounting changes.

### Test coverage
- Updated existing odds prompt assertions for Pass and Don't Pass text.
- Added tests for:
	- existing Pass Odds wording plus no `Multiples of 1` output.
	- existing Lay Odds wording plus Lay take-down confirmation string.
- Compile and full suite remain green.

## Milestone 60: Line Odds IO Adapter Routing

### What changed
- Routed line-odds output messaging in `odds()` through `writeOutput(...)`.
- Kept existing input path via `betPrompt()` unchanged for odds amount entry.
- Preserved all line-odds prompt wording and validation behavior from the prior milestone.

### Why
- Line-odds flow remained a direct terminal I/O hotspot after orchestrator adapter extraction.
- Moving this flow to the adapter boundary is a direct step toward UI portability for iOS.

### Behavior
- No payout-rule changes.
- No odds-limit logic changes.
- No bankroll/chips accounting changes.

### Test coverage
- Updated odds prompt tests to capture adapter output via `writeOutput` instead of patching `builtins.print`.
- Existing line-odds wording and validation assertions remain covered.
- Compile and full suite remain green.

## Milestone 61: Line Betting IO Adapter Routing

### What changed
- Routed `lineBetting()` menu output through `writeOutput(...)`.
- Routed `lineBetting()` command input through `readInput(...)`.
- Kept bet amount entry path via `betPrompt()` unchanged.
- Preserved existing line-bet command behavior and prompt wording.

### Why
- Line betting remained a direct terminal I/O hotspot after earlier adapter work.
- Moving this menu flow onto the adapter boundary improves portability toward iOS UI integration.

### Behavior
- No payout-rule changes.
- No command changes.
- No bankroll/chips accounting changes.

### Test coverage
- Updated Crapless Don't Pass rejection test to use adapter stubs.
- Added adapter-focused line-betting test for Pass entry path and prompt messaging.
- Compile and full suite remain green.

## Milestone 62: Point-Phase Line Control IO Adapter Routing

### What changed
- Routed `dpPhase2()` prompt/output through adapter helpers:
	- `readInput(...)`
	- `writeOutput(...)`
- Routed `oddsCheck()` settlement message output through `writeOutput(...)`.
- Preserved existing wording and bet/accounting behavior.

### Why
- Point-phase line control still had direct terminal I/O after previous adapter milestones.
- Moving this flow to adapter wrappers keeps controller-layer migration consistent for iOS.

### Behavior
- No payout-rule changes.
- No command changes.
- No bankroll/chips accounting changes.

### Test coverage
- Added adapter-focused tests in `tests/testEngineBehavior.py` for:
	- `dpPhase2()` take-down path with adapter stubs.
	- `oddsCheck()` message emission through `writeOutput`.
- Compile and full suite remain green.

## Milestone 63: Bankroll Shortcut Command (`bb`)

### What changed
- Added new shared betting command `bb` in `handleBettingCommand(...)`.
- `bb` now opens bankroll refill flow via `outOfMoney()` in both:
	- Come Out betting
	- Point-phase betting
- Updated in-game help text strings to include:
	- `bb: Add bankroll from the ATM`

### README updates
- Added `bb` to both command tables:
	- Come Out Roll Bet Codes
	- Point Phase Bet Codes
- Added bankroll note near startup bankroll section explaining that `bb` can be used at betting prompts.

### Why
- Players need a manual way to add bankroll on demand in all game modes without waiting for an out-of-money trigger.

### Behavior
- `bb` does not roll dice.
- `bb` does not change bet states directly.
- `bb` only invokes bankroll top-up flow.

### Test coverage
- Added deterministic command-handler tests in `tests/testEngineBehavior.py` to confirm:
	- `bb` calls `outOfMoney()` in come-out context.
	- `bb` calls `outOfMoney()` in point-phase context.
	- `bb` returns non-roll command result.
- Compile and full suite remain green.

## Milestone 64: Bankroll Management IO Adapter Routing

### What changed
- Routed `cashIn()` prompts and messages through adapter helpers:
	- `readInput(...)`
	- `writeOutput(...)`
- Routed `outOfMoney()` prompts and messages through adapter helpers:
	- `readInput(...)`
	- `writeOutput(...)`
- Kept bankroll accounting behavior unchanged.

### Why
- Bankroll management remained a core direct-I/O area after `bb` command was added.
- Adapter routing here is required for clean UI portability to iOS flows.

### Behavior
- No payout-rule changes.
- No betting command changes.
- No bankroll math changes.

### Test coverage
- Added deterministic adapter-focused tests in `tests/testEngineBehavior.py` for:
	- `cashIn()` invalid/zero retry path then successful bankroll set.
	- `outOfMoney()` invalid/negative retry path then successful bankroll top-up.
- Compile and full suite remain green.

## Milestone 65: Bet Prompt IO Adapter Routing

### What changed
- Routed `betPrompt()` input/output through adapter helpers:
	- `readInput(...)` for wager and follow-up bankroll prompt
	- `writeOutput(...)` for invalid-number message
- Preserved wager accounting and existing `outOfMoney()` branch behavior.

### Why
- `betPrompt()` is a high-fanout input path used across many betting systems.
- Moving it to adapter I/O significantly improves portability toward non-terminal UIs.

### Behavior
- No payout-rule changes.
- No command changes.
- No wager/accounting logic changes.

### Test coverage
- Added deterministic adapter-focused tests in `tests/testEngineBehavior.py` for:
	- invalid-number retry then accepted wager path.
	- insufficient-bank path invoking `outOfMoney()` then accepted wager path.
- Updated existing line-betting adapter test to provide `readInput` values for shared `betPrompt()` path.
- Full suite remains green.

## Milestone 66: Come Movement IO Adapter Routing

### What changed
- Routed Come/Don’t Come post-roll movement prompts in `processComePostRollAction(...)` through adapter helpers:
	- `readInput(...)`
	- `writeOutput(...)`
- Kept movement message order aligned with current game flow:
	- move message first
	- odds yes/no prompt second
	- odds amount prompt/retry loop third
- Fixed malformed indentation/control flow in the moved-bet odds loops for both Come and Don’t Come branches.

### Why
- Come movement and odds attachment remained a high-impact direct terminal I/O path.
- Adapter routing here is required for predictable UI migration to iOS while preserving existing table behavior.

### Behavior
- No payout-rule changes.
- No odds limit rule changes.
- No command surface changes.

### Test coverage
- Updated Come/Don’t Come movement regression tests to feed `readInput(...)` for both yes/no and odds amount paths.
- Preserved assertions for prompt ordering, max-odds retry behavior, and accepted odds persistence.
- Compile and full suite remain green (`201` tests passing).

## Milestone 67: Suppress Unit-1 Multiples Text Across Prompts

### What changed
- Removed unit-1 multiples wording from all prompt paths by making multiples text conditional (`unit != 1`) in:
	- `cdcOddsChange(...)` Come and Lay odds-change prompts
	- `processComePostRollAction(...)` Come moved-bet odds prompt
	- `processComePostRollAction(...)` Don't Come moved-bet lay-odds prompt
- Existing odds prompts that already conditionally hide unit-1 multiples remain unchanged.

### Why
- `Multiples of 1` is redundant and confusing in player prompts.
- Standardized prompt behavior so unit-1 contexts never display multiples text in any flow.

### Behavior
- No payout-rule changes.
- No max-odds math changes.
- No bet validation changes.

### Test coverage
- Added regression test for Crapless Come moved-bet odds prompt to confirm unit-1 prompt omits multiples text.
- Added regression test for `cdcOddsChange(...)` Come unit-1 prompt to confirm multiples text omission.
- Compile and full suite remain green (`203` tests passing).

## Milestone 68: `cdcOddsChange` IO Adapter Migration

### What changed
- Routed `cdcOddsChange(...)` prompts and messages through adapter helpers:
	- `readInput(...)`
	- `writeOutput(...)`
- Removed direct `input(...)`/`print(...)` use from this odds-edit flow.
- Preserved unit-aware prompt text behavior so unit-1 contexts do not show multiples text.

### Why
- `cdcOddsChange(...)` was still a direct terminal I/O path and blocked consistent UI boundary handling for iOS porting.
- Adapter routing here completes another high-traffic odds control surface.

### Behavior
- No payout-rule changes.
- No odds limit or unit validation rule changes.
- No bankroll/chips accounting changes.

### Test coverage
- Updated deterministic `cdcOddsChange(...)` tests to stub `readInput(...)`/`writeOutput(...)` directly.
- Kept validations for:
	- invalid unit retry
	- accepted odds persistence
	- unit-1 prompt omission of multiples text
- Compile and full suite remain green (`203` tests passing).

## Milestone 69: Hard Ways IO Adapter Migration

### What changed
- Routed Hard Ways subsystem prompts/messages to adapter helpers in:
	- `hardWaysBetting()`
	- `hardTakeDown()`
	- `hardAuto()`
	- `hardHigh()`
	- `hardCheck()`
	- `hardShow()`
- Replaced direct `input(...)`/`print(...)` in those flows with:
	- `readInput(...)`
	- `writeOutput(...)`

### Why
- Hard Ways remained a high-use direct terminal I/O hotspot.
- Adapter routing here improves portability and keeps command/controller boundaries consistent for iOS UI migration.

### Behavior
- No payout-rule changes.
- No Hard Ways press/re-up logic changes.
- No bankroll/chips accounting rule changes.

### Test coverage
- Updated Hard Ways betting tests to use adapter stubs for input/output.
- Added adapter-focused post-roll tests for:
	- press flow after a hard-way hit
	- re-up flow after an easy-way loss
- Compile and full suite remain green (`205` tests passing).

## Milestone 70: Fix Come/Don't Come Bar-Bet Settlement Emission in Craps Mode

### What changed
- Fixed `processComePostRollAction(...)` so Come and Don't Come settlement action results are merged for all bar-bet outcomes, not only moved-number outcomes.
- Kept moved-number de-duplication behavior in place so move messages are not duplicated when adapter prompts run.

### Why
- A regression caused non-move bar-bet outcomes (for example, Come losing on 2/3/12 in Craps, Come winning on 7/11, and Don't Come bar resolutions) to settle money but return empty action messages and `stateChanged=False`.
- This broke visible evaluation feedback and downstream flow state checks.

### Behavior
- Restores proper bar-bet evaluation reporting in Craps mode:
	- Come wins on 7/11
	- Come loses on 2/3/12
- Preserves existing Crapless Come behavior where 2/3/11/12 move to numbers.
- Preserves Don't Come bar rules:
	- wins on 2/3
	- loses on 7/11
	- pushes on 12

### Test coverage
- Added targeted regression tests in `tests/testEngineBehavior.py` to verify Craps-mode Come bar:
	- loss on 2 includes message and state change
	- win on 7 includes message and state change
- Compile and full suite remain green (`207` tests passing).

## Milestone 71: Enforce No Don't Pass / Don't Come in Crapless Mode

### What changed
- Enforced Come-only entry in Crapless mode:
	- `come()` now bypasses the Come/Don't Come chooser and only accepts a Come wager when mode is Crapless.
- Added strict command gates in Crapless mode:
	- `dp` is blocked with a mode message.
	- `dcd` is blocked with a mode message.
	- point-phase and come-out help menus no longer list `dcd` in Crapless mode.
	- point-phase help no longer lists `dp` in Crapless mode.
- Added cleanup safety for legacy Don't Come state:
	- `clearDontComeForCrapless()` refunds and clears `dComeBet`, `dComeBets`, and `dComeOdds` if found while in Crapless mode.
	- invoked from `comeCheck()` and from blocked `dcd` flow in Crapless mode.
- Restricted Don't Come display/management prompts in Crapless:
	- `comeShow()` no longer shows Don't Come rows in Crapless.
	- `comeOddsChange()` no longer opens Don't Come odds change path in Crapless.

### Why
- Crapless rules do not permit Don't Pass or Don't Come betting.
- Prior behavior still allowed Don't Come command flows and stale-state processing in Crapless sessions.

### Behavior
- Crapless mode now behaves as Come-only (no Don't Come controls).
- Legacy Don't Come amounts (if present from previous state) are returned to bankroll and cleared.
- Craps mode behavior remains unchanged.

### Test coverage
- Added regression test: Crapless `come()` path does not present Don't Come choice.
- Added regression test: `dcd` command is blocked in Crapless and refunds/clears legacy Don't Come state.
- Full compile and test suite remain green (`209` tests passing).

## Milestone 72: Field Subsystem IO Adapter Migration

### What changed
- Routed Field subsystem prompts/messages to adapter helpers in:
	- `fieldShow()`
	- `field()`
	- `fieldTakeDown()`
	- `fieldCheck()`
- Replaced direct `print(...)`/`input(...)` in those paths with:
	- `writeOutput(...)`
	- `readInput(...)`

### Why
- Field betting remained a frequent direct terminal I/O hotspot.
- Adapter routing keeps controller I/O boundaries consistent for iOS portability.

### Behavior
- No Field payout-rule changes.
- No bankroll/chips accounting rule changes.
- Existing win/loss change and re-up behavior preserved.

### Test coverage
- Added deterministic adapter-focused tests for:
	- Field entry wager flow.
	- Post-win field change flow.
	- Post-loss field re-up flow.
- Compile and full suite remain green (`212` tests passing).

## Milestone 73: Prop Bets IO Adapter Migration

### What changed
- Routed Prop betting menu I/O to adapter helpers:
	- `propHelp()` now uses `writeOutput(...)`
	- `propBetting()` now uses `readInput(...)` for command entry and `writeOutput(...)` for all menu messages/prompts/retry text
- Routed Prop settlement message emission to adapter output:
	- `propPay()` now emits alias, subset settlement, Buffalo settlement, Hop settlement, and manual-management notices via `writeOutput(...)`

### Why
- Prop betting remained one of the largest interactive direct terminal I/O surfaces.
- Moving this flow to adapter boundaries significantly improves UI-portability consistency for iOS migration.

### Behavior
- No prop payout-rule changes.
- No prop key/alias behavior changes.
- No prop bankroll/chips accounting rule changes.

### Test coverage
- Added deterministic adapter-focused tests for:
	- Hi-Low retry flow through `readInput(...)`/`writeOutput(...)`
	- Prop settlement output path through `writeOutput(...)`
- Existing Hi-Low accounting regression remains green.
- Compile and full suite remain green (`214` tests passing).

## Milestone 74: Crapless Lay Expansion, Payout Alignment, and Lay IO Migration

### What changed
- Expanded Lay support in Crapless mode to include edge numbers:
	- 2, 3, 11, 12 (alongside 4, 5, 6, 8, 9, 10)
- Added Crapless Lay helpers:
	- `e`: lays only 2, 3, 11, and 12
	- `ea`: Extreme Across lays all numbers from 2 through 12
- Kept standard `a` helper behavior as the original Lay Across on box numbers.
- Migrated Lay subsystem I/O to adapter helpers:
	- `layAll()` / `layBetting()` / `layShow()` / `layCheck()` / `runLayMenu()` now use `readInput(...)` and `writeOutput(...)`.
- Updated Lay payouts in engine settlement logic for Crapless edge numbers using Stratosphere-aligned true-odds lay structure:
	- Lay 2/12: 1:6
	- Lay 3/11: 1:3
	- Existing Lay 4/10, 5/9, 6/8 payouts unchanged.

### Why
- Lay betting in Crapless needed feature parity with edge numbers and helper workflows.
- Existing code still hard-blocked Lay in Crapless and used direct terminal I/O in Lay flows.
- Payout logic needed to include edge-number Lay math for consistent Crapless rules.

### Behavior
- Crapless mode now supports direct Lay entry/edit for 2, 3, 11, and 12.
- Lay settle/win/loss behavior now evaluates edge lays in Crapless mode.
- Lay menu help in Crapless now includes `e` and `ea` helper guidance.

### Documentation updates
- Updated README Lay section to reflect Crapless Lay availability and new helper commands (`e`, `ea`).
- Updated README payout table with Lay/DC Odds rows for:
	- 3, 11 (1:3)
	- 2, 12 (1:6)

### Test coverage
- Replaced old Crapless Lay-block test with edge-payout settlement coverage.
- Added/updated regression tests for:
	- Crapless Lay menu entry
	- Crapless Lay helper commands (`e`, `ea`)
	- Lay Across behavior with adapter input/output
	- Lay take-down behavior with adapter input/output
- Compile and full suite remain green (`217` tests passing).

## Milestone 75: Place Menu and Prompt IO Adapter Completion

### What changed
- Completed Place subsystem/menu input routing to adapter helpers in:
	- `runPlaceMenu()`
	- `placePreset(...)`
	- `placeBets()`
	- `placeShow()`
	- `placeMover()`
	- `placeCheck(...)`
	- `vig(...)`
- Replaced direct `input(...)`/`print(...)` calls in those Place flows with:
	- `readInput(...)`
	- `writeOutput(...)`

### Why
- Place betting remains one of the most-used interaction surfaces and was still partially direct terminal I/O.
- Finishing adapter routing here improves UI-boundary consistency for iOS port readiness.

### Behavior
- No Place payout-rule changes.
- No Place unit/multiple validation changes.
- No bankroll/chips accounting changes.

### Test coverage
- Added adapter-focused regression tests for:
	- `runPlaceMenu()` consuming commands via `readInput(...)`
	- `placeCheck(...)` press prompt consuming input via `readInput(...)`
- Existing Place and Crapless preset/buy-threshold test matrix remains green.
- Compile and full suite remain green (`219` tests passing).

## Milestone 76: ATS/Fire and Field Prompt IO Adapter Completion

### What changed
- Migrated ATS terminal I/O to adapter helpers:
	- `atsBetting()` now uses `readInput(...)`/`writeOutput(...)`
	- `ats()` settlement messaging now uses `writeOutput(...)`
- Migrated Fire terminal I/O to adapter helpers:
	- `fireBetting()` now uses `writeOutput(...)`
	- `fireCheck()` settlement messaging now uses `writeOutput(...)`
- Migrated remaining Field command prompts in betting flow to adapter input:
	- Point-phase `Field Bet? >` prompt in `handleBettingCommand(...)` now uses `readInput(...)`
	- Come-out `Field Bet? >` prompt in `handleBettingCommand(...)` now uses `readInput(...)`

### Why
- ATS and Fire still contained direct terminal I/O and were part of the remaining portability gaps.
- `handleBettingCommand(...)` still had two direct field-entry prompts; these were the last high-frequency direct inputs in that path.
- Completing adapter routing improves terminal/UI separation for future iOS integration.

### Behavior
- No ATS payout-rule changes.
- No Fire payout-rule changes.
- No Field bet-rule or bankroll accounting changes.
- Prompt text and settlement outcomes remain functionally equivalent.

### Test coverage
- Added deterministic adapter-focused tests for:
	- ATS betting prompt path using `readInput(...)` and output via `writeOutput(...)`
	- ATS seven-out loss messaging through adapter output
	- Fire betting prompt path using adapter output
	- `handleBettingCommand(...)` field prompts using `readInput(...)`
- Compile check passed.
- Full suite remains green (`223` tests passing).

## Milestone 77: Hard Ways and Game Mode Selection IO Adapter Normalization

### What changed
- Migrated remaining direct Hard Ways menu command input to adapter input:
	- `runHardWaysMenu()` now reads command via `readInput("Hard Ways Bets? > ")`
- Migrated game mode selection flow to adapter I/O:
	- `selectGameMode()` now emits all mode-selection lines via `writeOutput(...)`
	- `selectGameMode()` now reads mode choice via `readInput("> ")`
	- Invalid-choice and selected-mode feedback now emit via `writeOutput(...)`

### Why
- Hard Ways menu entry and game mode selection were still using direct terminal I/O.
- These are high-frequency controller interaction paths and needed the same adapter boundary used elsewhere.
- This further reduces coupling to terminal-only execution and improves iOS-portability readiness.

### Behavior
- No game rules changed.
- No payout logic changed.
- No bankroll/chips accounting changed.
- Prompts and outcomes remain functionally the same while routed through adapters.

### Test coverage
- Updated mode selection tests to assert adapter-driven flows:
	- `testSelectGameModeAcceptsCraps`
	- `testSelectGameModeAcceptsCrapless`
	- `testSelectGameModeRejectsInvalidThenAccepts`
- Added Hard Ways menu adapter regression:
	- `testRunHardWaysMenuUsesReadInput`
- Compile check passed.
- Full suite remains green (`224` tests passing).

## Milestone 78: Betting Status and Command Output Adapter Normalization

### What changed
- Migrated summary/status output in `showAllBets()` to `writeOutput(...)`:
	- Line bet rows
	- Come / Don't Come summary rows
	- Prop rows
	- ATS summary row
	- Fire bet summary row
- Migrated controller feedback output in `handleBettingCommand(...)` to `writeOutput(...)` for both point-phase and come-out command handling:
	- Bank display lines
	- Missing/blocked bet messages
	- Come bet header line
	- Help menu output
	- Working/Off toggle messages
	- ATS and Fire menu/status lines
	- Roll-ready messages and invalid-command messages
	- Line betting menu header line

### Why
- These betting/status controller paths were still using direct `print(...)` calls.
- Moving them to adapter output improves UI-boundary consistency and keeps terminal I/O behavior portable for iOS migration.
- Scope remained output-only; no bet math/rules were changed.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Existing text and flow behavior preserved while output routing is standardized.

### Test coverage
- Added deterministic adapter-focused regressions in `tests/testEngineBehavior.py`:
	- `testShowAllBetsUsesWriteOutputForSummaryRows`
	- `testHandleBettingCommandBankUsesWriteOutput`
	- `testHandleBettingCommandHelpUsesWriteOutput`
- Existing `Field Bet?` adapter routing regression retained and passing.
- Compile check passed.
- Full suite remains green (`227` tests passing).

## Milestone 79: Roll, Quit, and Round Status Output Adapter Normalization

### What changed
- Migrated roll narration output in `roll()` from direct `print(...)` to `writeOutput(...)`:
	- Hard-way callout lines
	- Come-out 7 and (Craps mode) 11 winner lines
	- General dealer-call / dice-face narration lines
- Migrated end-session output in `quitGame()` from `print(...)` to `writeOutput(...)` for all result branches.
- Migrated point-hit announcement in `resolvePointRoll()` to `writeOutput(...)`.
- Migrated game-start and top-level round status lines to `writeOutput(...)`:
	- Startup banner
	- Bank/bets-on-table status line
	- Throws line

### Why
- These high-visibility gameplay/session outputs were still bypassing adapter output.
- Routing them through `writeOutput(...)` improves consistency with the iOS-portability boundary while preserving current text and game flow.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Existing wording and control flow preserved; only output path changed.

### Test coverage
- Added deterministic adapter-focused regressions in `tests/testEngineBehavior.py`:
	- `testResolvePointRollPointHitUsesWriteOutput`
	- `testRollUsesWriteOutputForHardWayCall`
	- `testQuitGameUsesWriteOutput`
- Compile check passed.
- Full suite remains green (`230` tests passing).

## Milestone 80: Shared Settlement and Come Display Output Adapter Normalization

### What changed
- Migrated settlement message emission to adapter output in:
	- `lineCheck(...)`
	- `comePay(...)`
- Migrated action-result message emission to adapter output in:
	- `emitActionResult(...)`
- Migrated Come/Don't Come summary display lines to adapter output in:
	- `comeShow(...)`

### Why
- These shared pathways are called frequently across rounds and bet-resolution flows.
- They still used direct terminal output, which created inconsistent UI boundaries versus the rest of the adapter-based controller.
- Standardizing these paths improves portability for iOS-facing UI layers while preserving behavior.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Existing settlement/status text preserved; only output routing changed.

### Test coverage
- Added deterministic adapter-focused regressions in `tests/testEngineBehavior.py`:
	- `testEmitActionResultUsesWriteOutput`
	- `testLineCheckUsesWriteOutputForSettlementMessages`
	- `testComeShowUsesWriteOutput`
	- `testComePayUsesWriteOutputForSettlementMessages`
- Compile check passed.
- Full suite remains green (`234` tests passing).

## Milestone 81: Extracted Callable Game Entrypoint for Platform Handoff

### What changed
- Extracted startup and primary game loop into a callable `runGame()` function.
- Left a minimal terminal launcher behind `# Game Start`:
	- `if __name__ == "__main__":`
	- `	runGame()`
- Preserved startup behavior and loop sequencing:
	- Banner output
	- Game mode selection
	- Initial game state sync
	- Cash-in
	- Come-out loop status + round execution
	- Point-phase handoff

### Why
- A callable entrypoint is a key portability seam for iOS/app integration.
- This removes hardwired startup execution from top-level script body while keeping terminal play unchanged.
- It enables controlled invocation from future app host layers and automated harnesses.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Terminal execution remains unchanged when running the script directly.

### Test coverage
- Added deterministic entrypoint regressions in `tests/testEngineBehavior.py`:
	- `testRunGameBootstrapsAndLoopsThroughComeOutStatus`
	- `testRunGameTransitionsIntoPointPhaseRound`
- Compile check passed.
- Full suite remains green (`236` tests passing).

## Milestone 82: Runtime IO and Random Provider Injection Hooks

### What changed
- Added injectable runtime IO hooks:
	- `setIoHandlers(outputFunc=None, inputFunc=None)`
	- `resetIoHandlers()`
- Added injectable random provider hooks:
	- `setRandomProvider(provider=None)`
	- `resetRandomProvider()`
- Updated adapter wrappers to use injected hooks when provided:
	- `writeOutput(...)` routes to injected `outputHandler` when set; otherwise falls back to live `print(...)`
	- `readInput(...)` routes to injected `inputHandler` when set; otherwise falls back to live `input(...)`
- Updated random call sites to use injected random provider:
	- `roll()` dealer-call branch selection
	- `stickman()` call selection

### Why
- Host integration (iOS/app layers) needs explicit runtime injection seams for input/output and deterministic randomness.
- Keeping default behavior as live builtins preserves terminal gameplay and existing tests that patch builtins.
- Random provider injection gives deterministic control over narration/call selection without changing game rules.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Terminal behavior unchanged by default.
- Host/test harness can now inject custom IO and randomness without monkeypatching internals.

### Test coverage
- Added deterministic runtime-hook regressions in `tests/testEngineBehavior.py`:
	- `testSetIoHandlersOverridesReadAndWrite`
	- `testResetIoHandlersRestoresDefaults`
	- `testSetRandomProviderControlsStickmanChoice`
	- `testRollUsesInjectedRandomProviderForNarrationBranch`
- Compile check passed.
- Full suite remains green (`240` tests passing).

## Milestone 83: Runtime State Snapshot, Apply, and Reset API

### What changed
- Added runtime mode normalization helper:
	- `normalizedGameMode(modeValue)`
- Added host-facing runtime state APIs:
	- `getRuntimeState()`
	- `setRuntimeState(runtimeState)`
	- `resetRuntimeState()`
- `getRuntimeState()` now returns a normalized state payload including:
	- core runtime values (`bank`, `chipsOnTable`, `throws`, `pointIsOn`, `comeOut`, `p2`, toggles)
	- mode (`gameMode`)
	- line/prop/ATS/fire values
	- full bet snapshot (`betSnapshot`) via existing snapshot helpers
- `setRuntimeState(...)` now:
	- validates input type
	- rejects unsupported keys
	- applies partial updates for supported keys
	- supports game mode values as enum or normalized text
	- syncs `gameState` after updates
- `resetRuntimeState()` now restores a deterministic new-session baseline for runtime/bet structures and returns the resulting state.

### Why
- iOS/app host integration needs a safe and explicit way to inspect/apply session state without mutating globals directly.
- Deterministic reset and controlled partial updates reduce host-side coupling and state drift risk.
- Reusing existing snapshot structures minimizes behavioral risk.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Default terminal gameplay flow unchanged.

### Test coverage
- Added deterministic runtime-state regression tests in `tests/testEngineBehavior.py`:
	- `testGetRuntimeStateIncludesCoreAndSnapshot`
	- `testSetRuntimeStateAppliesCoreValuesAndMode`
	- `testSetRuntimeStateRejectsUnknownKeys`
	- `testResetRuntimeStateRestoresDefaults`
- Compile check passed.
- Full suite remains green (`244` tests passing).

## Milestone 84: Added Single-Cycle Runtime Runner for Host-Controlled Flow

### What changed
- Added new step-oriented runtime API:
	- `runOneCycle()`
- `runOneCycle()` now executes exactly one top-level game cycle:
	- runs `runComeOutRound()`
	- if no point is entered, returns immediately with cycle metadata
	- if point is entered, runs `runPointPhaseRound()` and returns point-phase metadata
- Refactored `runGame()` loop to call `runOneCycle()` for each cycle while preserving existing terminal behavior and status output.

### Why
- iOS/app hosts need predictable step-by-step execution control instead of direct dependence on nested infinite loops.
- A single-cycle runner creates a stable control seam for host-driven UI update loops and future session orchestration.
- Keeping `runGame()` as the terminal wrapper maintains existing play flow.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Terminal gameplay behavior unchanged.
- Host integrations can now call `runOneCycle()` directly for deterministic progression.

### Test coverage
- Added deterministic cycle/control regressions in `tests/testEngineBehavior.py`:
	- `testRunOneCycleReturnsComeOutOnlyPath`
	- `testRunOneCycleReturnsPointPhasePath`
- Updated runGame loop regressions to align with cycle runner integration:
	- `testRunGameBootstrapsAndLoopsThroughComeOutStatus`
	- `testRunGameTransitionsIntoPointPhaseRound`
- Compile check passed.
- Full suite remains green (`246` tests passing).

## Milestone 85: Runtime Event Hook API and Cycle Boundary Events

### What changed
- Added runtime event hook APIs:
	- `setEventHandler(handler=None)`
	- `resetEventHandler()`
	- `emitEvent(eventName, payload=None)`
- Integrated event emission into `runOneCycle()` at stable boundaries:
	- `cycleStarted`
	- `comeOutResolved`
	- `pointPhaseResolved` (only when point phase is entered)
	- `cycleCompleted`
- Event payloads now include deterministic cycle metadata and runtime snapshots where relevant:
	- cycle booleans/outcomes
	- point/throws snapshots
	- `runtimeState` via `getRuntimeState()` on resolution/completion events

### Why
- iOS/app hosts need push-style runtime notifications instead of polling full state after every step.
- Stable boundary events make UI updates, animations, and narration sync deterministic while preserving core game logic.
- Optional handler keeps terminal execution unchanged when no host subscriber is attached.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting changes.
- Terminal gameplay unchanged by default.
- Host integrations can now subscribe to cycle events for structured flow updates.

### Test coverage
- Added deterministic event regressions in `tests/testEngineBehavior.py`:
	- `testRunOneCycleEmitsEventsForComeOutOnlyPath`
	- `testRunOneCycleEmitsEventsForPointPhasePath`
	- `testResetEventHandlerClearsHandler`
- Compile check passed.
- Full suite remains green (`249` tests passing).

## Milestone 86: Introduced GameRuntime Core Container and Sync Bridge

### What changed
- Added `GameRuntime` container for core loop/runtime values:
	- `bank`
	- `chipsOnTable`
	- `throws`
	- `comeOut`
	- `pointIsOn`
	- `p2`
	- `gameMode`
- Added runtime/global bridge helpers:
	- `syncRuntimeFromGlobals(runtime=None)`
	- `syncGlobalsFromRuntime(runtime=None)`
- Added initialized shared runtime instance:
	- `gameRuntime = GameRuntime(...)`
- Integrated runtime-object reads into the selected vertical slice:
	- `showPointPhaseStatus()` now reads status values from synced runtime object
	- `runOneCycle()` now sources cycle/event point/throws metadata from synced runtime object
	- `runGame()` status banner loop now reads from synced runtime object
- Updated runtime state apply path:
	- `setRuntimeState(...)` now calls `syncRuntimeFromGlobals()` after applying/syncing globals

### Why
- This establishes the first concrete move away from direct scattered globals toward an encapsulated runtime model.
- The sync bridge keeps behavior stable while enabling incremental migration function-by-function.
- iOS host integration can now rely on a clearer runtime container without requiring full rewrite in one step.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Terminal gameplay flow unchanged.

### Test coverage
- Added deterministic runtime-bridge regressions in `tests/testEngineBehavior.py`:
	- `testSyncRuntimeFromGlobalsCapturesCoreLoopValues`
	- `testSyncGlobalsFromRuntimeAppliesCoreLoopValues`
- Existing cycle/status tests continue to pass with runtime-object integration.
- Compile check passed.
- Full suite remains green (`251` tests passing).

## Milestone 87: Roll Resolution Runtime Bridge Synchronization

### What changed
- Updated roll-resolution core functions to synchronize runtime bridge at entry/exit points:
	- `resolveComeOutRoll()`
	- `resolvePointRoll()`
- Entry behavior now synchronizes `gameRuntime` from current globals before resolution logic.
- Return paths now synchronize `gameRuntime` from globals after each outcome branch, preserving runtime/global alignment.

### Why
- These functions are central state transition points for every cycle.
- Ensuring runtime/global sync at roll boundaries improves consistency for host integrations using `GameRuntime` without changing existing game behavior.
- This is an incremental migration step that keeps compatibility with existing global-driven flows.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Legacy behavior and control flow preserved.
- `gameRuntime` now consistently reflects post-resolution roll outcomes.

### Test coverage
- Added deterministic runtime-sync roll-resolution regressions in `tests/testEngineBehavior.py`:
	- `testResolveComeOutRollSyncsGameRuntimeOnReturn`
	- `testResolvePointRollSyncsGameRuntimeOnReturn`
- Existing come-out/point resolution regressions remain passing.
- Compile check passed.
- Full suite remains green (`253` tests passing).

## Milestone 88: Command Path Runtime Synchronization in handleBettingCommand

### What changed
- Added runtime sync at command entry in `handleBettingCommand(...)`:
	- `syncRuntimeFromGlobals()` at function start
- Added a local return helper inside `handleBettingCommand(...)`:
	- `returnCommandResult(shouldRoll=False, handled=True)`
	- helper syncs runtime before returning the command result
- Routed all command return paths in `handleBettingCommand(...)` through `returnCommandResult(...)`.

### Why
- Command handling is a high-frequency state mutation path.
- Ensuring runtime sync at command boundaries keeps `gameRuntime` aligned with globals after every betting command outcome.
- This improves host-integration consistency without changing existing command behavior.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Command responses and flow unchanged.
- `gameRuntime` now reliably reflects post-command state.

### Test coverage
- Added/updated command-path runtime-sync regressions in `tests/testEngineBehavior.py`:
	- `testHandleBettingCommandSyncsRuntimeOnNoStateChangePath`
	- `testHandleBettingCommandBbCallsOutOfMoneyComeOut` (now also asserts runtime bank sync)
- Existing command behavior regression remains green (`testHandleBettingCommandPointRollReturnsTrue`).
- Compile check passed.
- Full suite remains green (`254` tests passing).

## Milestone 89: Runtime State Schema Helpers and API Normalization Refactor

### What changed
- Added explicit runtime-state schema helpers:
	- `runtimeStateKeys()`
	- `buildDefaultBetSnapshot()`
	- `buildDefaultRuntimeState()`
	- `validateRuntimeStatePayload(runtimeState)`
	- `normalizeRuntimeStatePayload(runtimeState)`
- Refactored runtime APIs to use schema helpers:
	- `getRuntimeState()` now returns a normalized payload shape
	- `setRuntimeState(...)` now validates and normalizes payload before apply
	- `resetRuntimeState()` now delegates to `buildDefaultRuntimeState()`
- Preserved partial-update behavior in `setRuntimeState(...)` while centralizing conversion/normalization.

### Why
- Runtime state logic had become spread across manual key checks and conversions.
- Centralized schema helpers reduce drift risk and make host contract evolution safer.
- Canonical default builders improve predictability for resets and test harnesses.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Supported runtime-state keys and overall API behavior remain consistent.

### Test coverage
- Added deterministic schema/runtime regressions in `tests/testEngineBehavior.py`:
	- `testNormalizeRuntimeStatePayloadCastsTypes`
	- `testBuildDefaultRuntimeStateMatchesResetDefaults`
- Existing runtime-state rejection/reset tests continue to pass.
- Compile check passed.
- Full suite remains green (`256` tests passing).

## Milestone 90: Programmatic Startup API for Host-Driven Initialization

### What changed
- Added host-facing mode setter:
	- `setGameMode(modeValue)`
	- normalizes mode input and syncs game/runtime state
- Added host-facing startup initializer:
	- `initializeGame(startBank, selectedMode)`
	- validates starting bank (> 0)
	- resets runtime to baseline
	- applies selected game mode
	- sets bankroll/initBank
	- syncs game/runtime state
	- emits `gameInitialized` event with runtime payload
- Updated terminal startup flow in `runGame()`:
	- preserved existing prompt sequence (`selectGameMode()` + `cashIn()`)
	- now calls `initializeGame(startBank=initBank, selectedMode=gameMode)` after prompts

### Why
- iOS/web hosts need a programmatic entrypoint that sets mode + bankroll without terminal prompts.
- This creates a clean startup contract while keeping terminal gameplay unchanged.
- Startup event emission supports host UI/session orchestration.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Terminal user flow remains the same.
- Host integrations can now initialize directly via API.

### Test coverage
- Added deterministic startup API regressions in `tests/testEngineBehavior.py`:
	- `testSetGameModeAcceptsTextAndSyncsRuntime`
	- `testInitializeGameSetsBankAndMode`
	- `testInitializeGameRejectsZeroBank`
- Updated runGame integration regressions for initialization seam:
	- `testRunGameBootstrapsAndLoopsThroughComeOutStatus`
	- `testRunGameTransitionsIntoPointPhaseRound`
- Compile check passed.
- Full suite remains green (`259` tests passing).

## Milestone 91: Host-Facing Command Submission API

### What changed
- Added host-facing command wrapper:
	- `submitCommand(commandText, pointPhase=False)`
- `submitCommand(...)` now:
	- normalizes input command text
	- executes command via `handleBettingCommand(...)`
	- returns normalized result payload containing:
		- `command`
		- `pointPhase`
		- `shouldRoll`
		- `handled`
		- `runtimeState`
	- emits `commandProcessed` event with the same payload

### Why
- Hosts (iOS/web) need a stable command-entry API rather than directly calling terminal-oriented command handlers.
- Returning runtime state with each command result reduces host-side polling and simplifies UI refresh logic.
- Event emission gives hosts an immediate push signal for command lifecycle handling.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Existing command handling behavior preserved.

### Test coverage
- Added deterministic command API regressions in `tests/testEngineBehavior.py`:
	- `testSubmitCommandReturnsNormalizedPayload`
	- `testSubmitCommandReturnsUnhandledPayload`
	- `testSubmitCommandEmitsCommandProcessedEvent`
- Compile check passed.
- Full suite remains green (`262` tests passing).

## Milestone 92: Unified Host Step API for Command and Cycle Execution

### What changed
- Added unified host-facing step executor:
	- `step(commandText=None, pointPhase=False)`
- `step(...)` supports two modes:
	- Command step: routes through `submitCommand(...)`
	- Cycle step: routes through `runOneCycle()`
- `step(...)` now returns a normalized payload shape:
	- `stepType` (`"command"` or `"cycle"`)
	- `commandResult` (or `None`)
	- `cycleResult` (or `None`)
	- `runtimeState`
- Added `stepCompleted` event emission with the same payload.
- Added input guard:
	- raises `ValueError` when `pointPhase=True` is provided without `commandText`.

### Why
- Host integrations need one orchestration entrypoint instead of branching manually between command and cycle APIs.
- Normalized payload/event shape simplifies iOS/web controller loops and UI update pipelines.
- Input guard prevents ambiguous/invalid host calls.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Existing APIs (`submitCommand`, `runOneCycle`, `runGame`) remain unchanged.

### Test coverage
- Added deterministic `step(...)` regressions in `tests/testEngineBehavior.py`:
	- `testStepCommandReturnsNormalizedPayload`
	- `testStepCycleReturnsNormalizedPayload`
	- `testStepEmitsStepCompletedEvent`
	- `testStepRejectsPointPhaseWithoutCommand`
- Compile check passed.
- Full suite remains green (`266` tests passing).

## Milestone 93: Route Terminal Betting Menus Through Unified step API

### What changed
- Updated terminal betting menu loops to use unified host/engine path via `step(...)`:
	- `runPointPhaseBettingMenu()` now calls `step(commandText=..., pointPhase=True)`
	- `runComeOutBettingMenu()` now calls `step(commandText=..., pointPhase=False)`
- Menu roll continuation behavior remains unchanged:
	- menu exits when `stepResult["commandResult"]["shouldRoll"]` is true

### Why
- This removes duplicate command-execution paths between terminal menu loops and host orchestration.
- Using `step(...)` everywhere strengthens parity across terminal and app-host execution behavior.
- It simplifies future platform adapters by consolidating command handling through one API.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Terminal prompts and roll-loop behavior unchanged.

### Test coverage
- Updated betting-menu loop regressions in `tests/testEngineBehavior.py` to assert `step(...)` path usage:
	- `testRunPointPhaseBettingMenuLoopsUntilRollCommand`
	- `testRunPointPhaseBettingMenuUsesPointPhaseTrue`
	- `testRunComeOutBettingMenuLoopsUntilRollCommand`
	- `testRunComeOutBettingMenuUsesPointPhaseFalse`
- Compile check passed.
- Full suite remains green (`266` tests passing).

## Milestone 94: Optional Output Capture for Host Payloads and Events

### What changed
- Added optional output capture runtime controls:
	- `beginOutputCapture()`
	- `endOutputCapture()`
	- `getCapturedOutput()`
- Added capture state variables:
	- `outputCaptureOn`
	- `outputCaptureBuffer`
- Updated `writeOutput(...)` to buffer message strings when capture is enabled while preserving normal output behavior.
- Updated host-facing payloads to include captured output:
	- `submitCommand(...)` now includes `capturedOutput`
	- `step(...)` now includes `capturedOutput` for both command and cycle step payloads
- Related events now carry payloads with captured output fields:
	- `commandProcessed`
	- `stepCompleted`

### Why
- Host apps often need per-step/per-command transcript chunks without reconstructing output from custom handlers.
- Optional capture keeps terminal behavior unchanged by default while enabling richer UI rendering and logging in iOS/web hosts.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Terminal output flow remains unchanged when capture is not enabled.

### Test coverage
- Added/updated deterministic output-capture regressions in `tests/testEngineBehavior.py`:
	- `testOutputCaptureBuffersWriteOutputWhenEnabled`
	- `testSubmitCommandIncludesCapturedOutputWhenCaptureEnabled`
	- submit/step payload shape assertions now include `capturedOutput`
- Compile check passed.
- Full suite remains green (`268` tests passing).

## Milestone 95: Prompt Capture and inputRequested Event Integration

### What changed
- Added prompt capture runtime controls:
	- `beginPromptCapture()`
	- `endPromptCapture()`
	- `getCapturedPrompts()`
- Added prompt capture state:
	- `promptCaptureOn`
	- `promptCaptureBuffer`
- Updated `readInput(promptText)` to:
	- emit `inputRequested` event for every prompt
	- append prompt text to capture buffer when prompt capture is enabled
- Extended host payloads to include prompt transcripts:
	- `submitCommand(...)` now includes `capturedPrompts`
	- `step(...)` now includes `capturedPrompts` in both command and cycle payloads

### Why
- iOS/web hosts need visibility into input prompts to render native UI prompt flows without scraping terminal text.
- Prompt capture complements output capture so each step can carry complete interaction context (prompts + outputs).
- `inputRequested` provides real-time prompt intent signaling to host controllers.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Terminal input/output behavior unchanged.

### Test coverage
- Added deterministic prompt-capture/input-event regressions in `tests/testEngineBehavior.py`:
	- `testPromptCaptureBuffersReadInputPromptWhenEnabled`
	- `testReadInputEmitsInputRequestedEvent`
	- `testSubmitCommandIncludesCapturedPromptsWhenCaptureEnabled`
- Updated command/step payload shape regressions to assert `capturedPrompts` presence.
- Compile check passed.
- Full suite remains green (`271` tests passing).

## Milestone 96: Scoped Capture Helper and autoCapture Host API Option

### What changed
- Added scoped capture helper:
	- `runWithCapture(func)`
	- begins output + prompt capture, executes function, returns:
		- `result`
		- `capturedOutput`
		- `capturedPrompts`
	- restores prior capture states/buffers in a `finally` block (exception-safe)
- Extended host APIs with optional auto capture mode:
	- `submitCommand(commandText, pointPhase=False, autoCapture=False)`
	- `step(commandText=None, pointPhase=False, autoCapture=False)`
- `autoCapture=True` now wraps execution through `runWithCapture(...)` and includes scoped transcripts in payloads.
- Default behavior remains unchanged when `autoCapture=False`.

### Why
- Hosts previously had to manually coordinate capture lifecycle around every call.
- `runWithCapture(...)` centralizes that orchestration and guarantees cleanup on failure.
- Optional `autoCapture` makes iOS/web host calls simpler and less error-prone.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Existing API behavior preserved when `autoCapture` is not used.

### Test coverage
- Added deterministic scoped-capture/autoCapture regressions in `tests/testEngineBehavior.py`:
	- `testRunWithCaptureCapturesAndRestoresState`
	- `testRunWithCaptureRestoresStateAfterException`
	- `testSubmitCommandAutoCaptureIncludesOutputAndPrompts`
	- `testStepAutoCaptureCycleIncludesCapturedOutput`
- Existing command/step payload regressions remain green.
- Compile check passed.
- Full suite remains green (`275` tests passing).

## Milestone 97: Engine API Versioning for Host Payload and Event Contracts

### What changed
- Added explicit engine API version constant:
	- `engineApiVersion = "1.0.0"`
- Added shared payload version helper:
	- `withApiVersion(payload)`
- Updated event emission to include API version in dict payloads:
	- `emitEvent(...)` now enriches dict payloads with `engineApiVersion`
- Added API version to host-facing return payloads:
	- `initializeGame(...)` return payload
	- `submitCommand(...)` payload
	- `step(...)` payload (command and cycle)
- Added API version to cycle/event payload construction:
	- `cycleStarted`
	- `comeOutResolved`
	- `pointPhaseResolved`
	- `cycleCompleted`
	- `gameInitialized`

### Why
- Host integrations need a stable, explicit contract version for payload/event parsing and forward compatibility.
- Centralized payload enrichment reduces schema drift and avoids ad hoc per-call version stamping.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Existing host payload keys preserved; `engineApiVersion` is additive.

### Test coverage
- Added/updated regression assertions in `tests/testEngineBehavior.py` for API version presence in:
	- `initializeGame(...)` return payload
	- `submitCommand(...)` payload + `commandProcessed` event payload
	- `step(...)` command/cycle payloads
	- cycle boundary events
- Compile check passed.
- Full suite remains green (`275` tests passing).

## Milestone 98: Session Bundle Export/Import API for Host Save and Restore

### What changed
- Added session export API:
	- `exportSessionBundle()`
	- returns canonical bundle payload with:
		- `engineApiVersion`
		- `bundleType` (`ohcrapsSession`)
		- `runtimeState`
		- `gameMode`
		- `captureState` (prompt/output capture flags + buffers)
		- `hostMetadata`
- Added session import API:
	- `importSessionBundle(bundle)`
	- validates bundle type/version/shape
	- restores runtime via `setRuntimeState(...)`
	- restores capture flags/buffers
	- emits `sessionImported` event
	- returns normalized exported bundle after import

### Why
- Host apps need one stable persistence/replay contract instead of stitching runtime/capture/event state manually.
- Canonical bundle export/import simplifies save/load, handoff, and debugging workflows for iOS/web hosts.
- Version/type checks protect against incompatible session payloads.

### Behavior
- No payout/rule changes.
- No bankroll/chips accounting rule changes.
- Runtime play flow unchanged; this is additive host-session functionality.

### Test coverage
- Added deterministic session-bundle regressions in `tests/testEngineBehavior.py`:
	- `testExportSessionBundleIncludesVersionAndCaptureState`
	- `testImportSessionBundleRoundTripRestoresState`
	- `testImportSessionBundleRejectsInvalidVersion`
	- `testImportSessionBundleEmitsSessionImportedEvent`
- Compile check passed.
- Full suite remains green (`279` tests passing).

## Milestone 99: Host Error Contract Normalization and Payload Stability

### What changed
- Added a shared host error builder:
	- `hostErrorPayload(errorCode, errorMessage, details=None)`
- Normalized `submitCommand(...)` contract:
	- Added always-present keys:
		- `success` (`True`/`False`)
		- `error` (`None` or structured error object)
	- Added protected execution block around command handling.
	- On failure, returns deterministic error payload instead of returning partial/undefined fields.
	- Added optional strict mode:
		- `raiseOnError=True` re-raises exceptions after payload construction path is available.
- Normalized `step(...)` contract:
	- Added always-present keys:
		- `success`
		- `error`
	- Command steps now mirror command payload success/error.
	- Cycle steps now catch execution errors and return structured `cycleExecutionFailed` payload.
	- Invalid argument path (`pointPhase=True` without command) now returns structured `invalidStepArguments` payload and emits `stepCompleted`.
	- Added optional strict mode:
		- `raiseOnError=True` preserves raising behavior for strict callers.

### Why
- Host apps (iOS/web) need predictable, non-ambiguous response envelopes for every call.
- Mixing raised exceptions with partial payloads increases integration complexity and UI error drift.
- A deterministic `success + error` pattern lets host clients implement one response parser and one error display path.

### Behavior
- No craps rules/payout changes.
- No bankroll/chips accounting changes.
- Terminal flow remains unchanged.
- Host API behavior is additive and more explicit:
	- Success paths still return existing payload data.
	- Failure paths now return structured errors by default.

### Test coverage
- Updated/added deterministic contract tests in `tests/testEngineBehavior.py`:
	- command and cycle step payloads now assert `success=True` and `error=None` on normal flow.
	- invalid step argument now returns structured error payload.
	- strict mode still raises (`raiseOnError=True`).
	- command failure returns `commandExecutionFailed` schema.
	- cycle failure returns `cycleExecutionFailed` schema.
- Full suite remains green after this milestone.

## Milestone 100: Centralized Host Payload Builders and Error Code Constants

### What changed
- Added host error code constants in one map:
	- `hostErrorCodes["invalidStepArguments"]`
	- `hostErrorCodes["commandExecutionFailed"]`
	- `hostErrorCodes["cycleExecutionFailed"]`
- Added shared host payload builders:
	- `buildHostCommandPayload(...)`
	- `buildHostStepPayload(...)`
- Updated `submitCommand(...)` to build payloads through `buildHostCommandPayload(...)`.
- Updated `step(...)` to build payloads through `buildHostStepPayload(...)` for:
	- command step path
	- invalid-argument path
	- cycle path
- Replaced inline error-code strings with `hostErrorCodes[...]` references in command/step error paths.

### Why
- Contract definitions were still duplicated inline across host entrypoints.
- Central payload builders reduce schema drift risk and make host response changes safer.
- Error-code constants eliminate typo/regression risk in host-side code that branches on codes.

### Behavior
- No craps rules/payout changes.
- No bankroll/chips accounting changes.
- Terminal game flow remains unchanged.
- Host payload shape remains compatible; this milestone centralizes construction and stabilizes constants.

### Test coverage
- Added deterministic regression tests in `tests/testEngineBehavior.py` for:
	- `hostErrorCodes` contract values.
	- `buildHostCommandPayload(...)` canonical keys.
	- `buildHostStepPayload(...)` canonical keys.
- Updated existing error-path assertions to reference `hostErrorCodes` constants.
- Full suite remains green after this milestone.

## Milestone 101: Host Schema Descriptor and Compatibility Check API

### What changed
- Added host feature descriptor helper:
	- `hostFeatureFlags()`
- Added host schema descriptor API:
	- `hostSchemaDescriptor()`
	- exposes:
		- `schemaVersion`
		- `errorCodes`
		- `features`
		- `payloadKeys` for `command`, `step`, and `sessionBundle`
- Added compatibility-check API:
	- `checkHostCompatibility(requiredApiVersion=None, requiredFeatures=None)`
	- returns:
		- `compatible`
		- `requiredApiVersion`
		- `requiredFeatures`
		- `missingFeatures`
		- `reasons`
		- `engineApiVersion`

### Why
- iOS/web hosts need a runtime-safe way to inspect what this engine contract supports.
- Descriptor-based integration avoids hardcoding payload assumptions in host apps.
- Explicit compatibility checks make startup gating deterministic and easier to debug.

### Behavior
- No craps rules/payout changes.
- No bankroll/chips accounting changes.
- Terminal gameplay flow unchanged.
- Host-side introspection capability is additive.

### Test coverage
- Added deterministic tests in `tests/testEngineBehavior.py` for:
	- descriptor shape (`hostSchemaDescriptor` includes core sections)
	- compatibility success for current version + supported features
	- compatibility failure for unsupported API version
	- compatibility failure for unsupported feature requests
- Full suite remains green after this milestone.

## Milestone 102: Host Event Contract Normalization

### What changed
- Added centralized host event name constants:
	- `hostEventNames`
		- `inputRequested`
		- `sessionImported`
		- `commandProcessed`
		- `stepCompleted`
		- `cycleStarted`
		- `comeOutResolved`
		- `pointPhaseResolved`
		- `cycleCompleted`
		- `gameInitialized`
- Added centralized host event payload builders:
	- `buildInputRequestedEventPayload(...)`
	- `buildSessionImportedEventPayload(...)`
	- `buildCycleStartedEventPayload(...)`
	- `buildComeOutResolvedEventPayload(...)`
	- `buildPointPhaseResolvedEventPayload(...)`
	- `buildCycleCompletedEventPayload(...)`
	- `buildGameInitializedEventPayload(...)`
- Routed all `emitEvent(...)` call sites through `hostEventNames` and payload builders.
- Extended `hostSchemaDescriptor()` with event contract introspection:
	- `eventNames`
	- `payloadKeys["events"]`

### Why
- Event names/payloads were still duplicated as raw strings and inline dicts.
- Centralizing event contracts reduces schema drift and host parsing regressions.
- Publishing event contracts in schema descriptor improves iOS/web runtime integration safety.

### Behavior
- No craps rules/payout changes.
- No bankroll/chips accounting changes.
- Terminal gameplay flow remains unchanged.
- Host event contract is now centralized and introspectable.

### Test coverage
- Added deterministic tests for:
	- `hostEventNames` contract values
	- event payload builder contract keys
	- schema descriptor event sections
- Updated event-emission tests to assert against `hostEventNames` constants.
- Full suite remains green after this milestone.

## Milestone 103: One-Call Startup Package for App Hosts

### What problem this solves
- Right now, an iOS/web app needs to make several separate calls to understand engine state at startup.
- That makes startup wiring harder and easier to break.

### What changed
- Added `createHostStartupBundle(...)` in `OhCraps_Py3.command`.
- This returns one package with:
	- current runtime state
	- schema descriptor
	- compatibility result
	- feature flags
	- success/error fields
- Added startup validation error code:
	- `startupValidationFailed`
- Added `startupBundle` keys to `hostSchemaDescriptor()` so host apps can inspect this contract.

### Why this helps
- App startup can now be one clean call instead of multiple setup calls.
- If startup input is bad, the app gets a clear structured error instead of guessing what failed.

### Behavior
- No craps rules changed.
- No payout math changed.
- Terminal gameplay flow is unchanged.

### Test coverage
- Added tests for:
	- success startup package without re-initializing
	- success startup package with initialization
	- missing startup args error handling
	- invalid startup values error handling
	- compatibility failure details included in startup package
- Full suite remains green after this milestone.

## Milestone 104: Host Command List API (What buttons are valid right now)

### What problem this solves
- An app UI needs to know which commands are valid in the current moment.
- Before this, the app had to hardcode that logic and could drift from engine behavior.

### What changed
- Added `hostAllowedCommands(pointPhase=False)` in `OhCraps_Py3.command`.
- This returns a simple package with:
	- current mode
	- whether we are in point phase
	- command list with:
		- `code`
		- `label`
		- `enabled`
		- optional `reason` if disabled
- Added `allowedCommands` contract keys to `hostSchemaDescriptor()`.

### Why this helps
- iOS/web can build menus/buttons directly from the engine response.
- Mode-specific rules are now provided by the engine, not guessed by the app.

### Behavior
- No craps rules changed.
- No payout math changed.
- Terminal gameplay flow is unchanged.

### Test coverage
- Added tests for:
	- Craps come-out command list includes enabled `dcd`
	- Crapless come-out command list disables `dcd` with reason
	- point-phase command list includes odds/come actions
	- schema descriptor includes `allowedCommands`
- Full suite remains green after this milestone.

## Milestone 105: One-Call UI Snapshot API

### What problem this solves
- After each action, an app still needed multiple calls to rebuild the UI.
- That made refresh logic harder and increased risk of screen drift.

### What changed
- Added `createHostUiSnapshot(pointPhase=False)` in `OhCraps_Py3.command`.
- It returns one package with:
	- current mode
	- current phase flag
	- runtime state
	- allowed commands
	- captured output
	- captured prompts
- Added `uiSnapshot` to `hostSchemaDescriptor()` payload keys.

### Why this helps
- iOS/web can refresh screen state from one response.
- Fewer host calls and less wiring logic.
- Lower chance of UI showing stale or incomplete state.

### Behavior
- No craps rules changed.
- No payout logic changed.
- Terminal gameplay flow remains unchanged.

### Test coverage
- Added tests for:
	- snapshot includes state + commands + capture buffers
	- point-phase snapshot includes point-phase commands
	- Crapless snapshot disables Don’t Come controls in point phase
	- schema descriptor includes `uiSnapshot`
- Full suite remains green after this milestone.
