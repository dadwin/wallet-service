#! /usr/bin/env bash

cd /wallet
# Let the DB start
python app/pre_start.py

# Run migrations
alembic upgrade head

# start backend
uvicorn app.main:app --host 0.0.0.0 --port 80
