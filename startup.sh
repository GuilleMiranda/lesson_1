#!/bin/bash

python -m alembic upgrade head

uvicorn app.main:app