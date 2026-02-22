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
