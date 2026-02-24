#!/bin/zsh

set -e

echo "[0/4] Running critical host-contract fast suite..."
python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostContractCriticalFastSuite

echo "[1/4] Running fast host-contract cycle..."
python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostContractFastCycle

echo "[2/4] Running compile checks..."
python3 -m py_compile tests/testEngineBehavior.py OhCraps_Py3.command

echo "[3/4] Running full suite..."
python3 -m unittest discover -s tests -p 'test*.py'

echo "Solo QA cycle complete: all checks passed."
