# Pre-Port Readiness Checklist

## Goal
Use this checklist before any iOS or web port work to confirm the Python engine is stable and integration contracts are safe.

## Required Runs
1. Quick loop check
- `./tests/runSoloQaCycle.sh --quick`

2. Release gate check
- `./tests/runSoloQaCycle.sh --release-gate`

3. Full gate check
- `./tests/runSoloQaCycle.sh`

## Pass Criteria
- Every run finishes without stopping early.
- QA summary shows all executed stages as `PASS`.
- Full run includes full suite pass.

## If Any Stage Fails
1. Fix the first failing stage only.
2. Re-run the same command.
3. Do not move to the next gate until current gate is green.

## Final Sign-Off
Porting should start only when all three required runs pass in the same working session.
