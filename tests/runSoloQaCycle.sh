#!/bin/zsh

set -e

echo "[1/3] Running fast host-contract cycle..."
python3 -m unittest discover -s tests -p 'testEngineBehavior.py' -k HostContractFastCycle

echo "[2/3] Running compile checks..."
python3 -m py_compile tests/testEngineBehavior.py OhCraps_Py3.command

echo "[3/3] Running full suite..."
python3 -m unittest discover -s tests -p 'test*.py'

echo "Solo QA cycle complete: all checks passed."
