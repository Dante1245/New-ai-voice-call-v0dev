#!/bin/bash
echo "Starting with Sync worker (fallback)..."
gunicorn -w 1 --bind 0.0.0.0:$PORT app:app
