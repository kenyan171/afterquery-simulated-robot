#!/bin/sh
set -eu

mkdir -p /logs/verifier

reward=0

cleanup() {
    printf '%s\n' "$reward" > /logs/verifier/reward.txt
}

trap cleanup EXIT

if python -m pytest -q \
    /tests/test_verifier.py \
    --ctrf=/logs/verifier/report.json
then
    reward=1
else
    reward=0
fi
