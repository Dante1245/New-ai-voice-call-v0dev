#!/bin/bash
echo "🚀 Starting Steve Perry AI with Thread Worker..."
export PORT=5000
gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app
