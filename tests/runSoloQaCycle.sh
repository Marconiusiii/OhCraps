#!/bin/zsh

set -e

quickMode="false"
releaseGateMode="false"
if [[ $# -gt 0 ]]; then
	if [[ "$1" == "--quick" ]]; then
		quickMode="true"
	elif [[ "$1" == "--release-gate" ]]; then
		releaseGateMode="true"
	else
		echo "Usage: ./tests/runSoloQaCycle.sh [--quick|--release-gate]"
		exit 1
	fi
fi

startEpoch=$(date +%s)
stageReleaseStatus="SKIPPED"
stageZeroStatus="PASS"
stageOneStatus="PASS"
stageTwoStatus="PASS"
stageThreeStatus="PASS"

if [[ "${releaseGateMode}" == "true" ]]; then
	echo "[RG] Running release gate suite..."
	python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostReleaseGateSuite
	stageReleaseStatus="PASS"
fi

echo "[0/4] Running critical host-contract fast suite..."
python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostContractCriticalFastSuite

echo "[1/4] Running fast host-contract cycle..."
python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostContractFastCycle

echo "[2/4] Running compile checks..."
python3 -m py_compile tests/testEngineBehavior.py OhCraps_Py3.command

if [[ "${quickMode}" == "true" ]]; then
	stageThreeStatus="SKIPPED (quick mode)"
else
	echo "[3/4] Running full suite..."
	python3 -m unittest discover -s tests -p 'test*.py'
fi

endEpoch=$(date +%s)
elapsedSeconds=$((endEpoch - startEpoch))

echo ""
echo "QA Run Summary:"
echo "  [RG] Release gate suite: ${stageReleaseStatus}"
echo "  [0/4] Critical host-contract fast suite: ${stageZeroStatus}"
echo "  [1/4] Fast host-contract cycle: ${stageOneStatus}"
echo "  [2/4] Compile checks: ${stageTwoStatus}"
echo "  [3/4] Full suite: ${stageThreeStatus}"
echo "  Elapsed: ${elapsedSeconds}s"
if [[ "${quickMode}" == "true" ]]; then
	echo "Solo QA quick cycle complete: all executed checks passed."
else
	echo "Solo QA cycle complete: all checks passed."
fi
