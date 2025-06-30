#!/bin/bash

echo "Applying migrations..."
uv run --no-sync alembic upgrade head

echo "Starting app..."
uv run --no-sync uvicorn owl_core.main:app --host 0.0.0.0 --port 8000 --reload