#! /usr/bin/env bash
set -x

pytest -s  --cov=app --cov-branch --cov-report=term-missing tests/
