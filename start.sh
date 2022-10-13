#! /usr/bin/env bash
set -x

cd /wallet
# Let the DB start
python app/pre_start.py

# Run migrations
alembic upgrade head

# Init data
python app/initial_data.py

# start backend
uvicorn app.main:app --host 0.0.0.0 --port 80
