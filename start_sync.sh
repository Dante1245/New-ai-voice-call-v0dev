#!/bin/bash
echo "🚀 Starting Steve Perry AI with Sync Worker..."
export PORT=5000
gunicorn -w 1 --bind 0.0.0.0:$PORT app:app
