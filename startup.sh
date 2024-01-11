#!/bin/bash
echo "Starting alembic"
python -m alembic upgrade head
echo "Alembic finished. Starting service."
uvicorn app.main:app