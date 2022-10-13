#! /usr/bin/env bash

pytest -s  --cov=app --cov-branch --cov-report=term-missing tests/
