#!/bin/bash

pip install -r /app/requirements.txt

cd /app
echo $(ls)
python3 -m alembic upgrade head

uvicorn app.main:app --host "0.0.0.0" --port 10000