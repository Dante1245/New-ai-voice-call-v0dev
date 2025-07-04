#!/bin/bash
echo "🚀 Starting Steve Perry AI with Gevent..."
export PORT=5000
gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app
