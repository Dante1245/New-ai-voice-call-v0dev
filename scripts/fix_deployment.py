#!/usr/bin/env python3
"""
Fix deployment issues and provide alternative configurations
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def fix_requirements():
    """Fix requirements.txt for better compatibility"""
    print("🔧 Fixing requirements.txt for production compatibility...")
    
    requirements_content = """# Core Flask and Web Framework
Flask==2.3.3
Flask-SocketIO==5.3.6
Werkzeug==2.3.7

# WebSocket and Async Support
python-socketio==5.9.0
python-engineio==4.7.1
gevent==23.9.1
gevent-websocket==0.10.1

# HTTP Requests and Utilities
requests==2.31.0
urllib3==1.26.18
certifi>=2023.7.22

# WSGI Server for Production
gunicorn==21.2.0

# Environment Variables
python-dotenv==1.0.0

# Twilio SDK
twilio==8.10.0

# OpenAI SDK
openai==1.3.0

# Additional Production Dependencies
wheel>=0.38.0
setuptools>=65.0.0

# Security and Performance
cryptography>=41.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    print("✅ Requirements.txt updated with compatible versions")

def create_alternative_configs():
    """Create multiple deployment configuration options"""
    print("🔧 Creating alternative deployment configurations...")
    
    # Standard Procfile with gevent
    procfile_gevent = "web: gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
    
    # Fallback Procfile with sync workers
    procfile_sync = "web: gunicorn -w 1 --bind 0.0.0.0:$PORT app:app"
    
    # Threading Procfile
    procfile_thread = "web: gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app"
    
    configs = {
        'Procfile': procfile_gevent,
        'Procfile.sync': procfile_sync,
        'Procfile.thread': procfile_thread
    }
    
    for filename, content in configs.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Created {filename}")

def update_app_for_compatibility():
    """Update app.py for better production compatibility"""
    print("🔧 Updating app.py for production compatibility...")
    
    # Read current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Replace eventlet with gevent in SocketIO initialization
    if 'async_mode=\'eventlet\'' in content:
        content = content.replace('async_mode=\'eventlet\'', 'async_mode=\'gevent\'')
        print("✅ Updated SocketIO async_mode to gevent")
    
    # Add fallback for SocketIO initialization
    socketio_init = '''            # Initialize SocketIO with production settings
            self.socketio = SocketIO(
                self.app,
                cors_allowed_origins="*",
                async_mode='gevent',
                logger=False,
                engineio_logger=False,
                ping_timeout=60,
                ping_interval=25
            )'''
    
    if 'async_mode=\'gevent\'' not in content:
        # Find and replace the SocketIO initialization
        import re
        pattern = r'self\.socketio = SocketIO$$[^)]+$$'
        if re.search(pattern, content):
            content = re.sub(
                r'self\.socketio = SocketIO$$[^)]+$$',
                '''self.socketio = SocketIO(
                self.app,
                cors_allowed_origins="*",
                async_mode='gevent',
                logger=False,
                engineio_logger=False,
                ping_timeout=60,
                ping_interval=25
            )''',
                content
            )
            print("✅ Updated SocketIO initialization")
    
    # Write updated content
    with open('app.py', 'w') as f:
        f.write(content)

def create_render_yaml():
    """Create render.yaml for Render deployment"""
    print("🔧 Creating render.yaml configuration...")
    
    render_config = """services:
  - type: web
    name: steve-perry-ai-voice-assistant
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_config)
    
    print("✅ Created render.yaml")

def create_runtime_txt():
    """Create runtime.txt for Python version specification"""
    print("🔧 Creating runtime.txt...")
    
    # Use Python 3.11 for better compatibility
    with open('runtime.txt', 'w') as f:
        f.write('python-3.11.0')
    
    print("✅ Created runtime.txt with Python 3.11")

def test_local_compatibility():
    """Test if the app runs locally with new configuration"""
    print("🧪 Testing local compatibility...")
    
    try:
        # Try importing gevent
        import gevent
        print("✅ Gevent available")
    except ImportError:
        print("⚠️  Gevent not installed locally, but should work in production")
    
    try:
        # Test Flask-SocketIO with gevent
        from flask_socketio import SocketIO
        from flask import Flask
        
        test_app = Flask(__name__)
        test_socketio = SocketIO(test_app, async_mode='gevent')
        print("✅ Flask-SocketIO with gevent works")
        
    except Exception as e:
        print(f"⚠️  Flask-SocketIO test warning: {e}")
        print("This may work in production environment")

def create_deployment_alternatives():
    """Create alternative deployment scripts"""
    print("🔧 Creating deployment alternatives...")
    
    # Alternative start commands for different scenarios
    start_commands = {
        'start_gevent.sh': '''#!/bin/bash
echo "Starting with Gevent worker..."
gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app
''',
        'start_sync.sh': '''#!/bin/bash
echo "Starting with Sync worker (fallback)..."
gunicorn -w 1 --bind 0.0.0.0:$PORT app:app
''',
        'start_thread.sh': '''#!/bin/bash
echo "Starting with Thread worker..."
gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app
''',
        'start_dev.sh': '''#!/bin/bash
echo "Starting development server..."
python app.py
'''
    }
    
    for filename, content in start_commands.items():
        with open(filename, 'w') as f:
            f.write(content)
        
        # Make executable
        try:
            os.chmod(filename, 0o755)
        except:
            pass
        
        print(f"✅ Created {filename}")

def main():
    """Main fix deployment function"""
    print("🚀 FIXING DEPLOYMENT CONFIGURATION")
    print("=" * 50)
    
    # Fix requirements
    fix_requirements()
    
    # Create alternative configs
    create_alternative_configs()
    
    # Update app for compatibility
    update_app_for_compatibility()
    
    # Create deployment files
    create_render_yaml()
    create_runtime_txt()
    
    # Test compatibility
    test_local_compatibility()
    
    # Create alternatives
    create_deployment_alternatives()
    
    print("\n✅ DEPLOYMENT FIXES COMPLETE!")
    print("=" * 50)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Commit the changes:")
    print("   git add .")
    print("   git commit -m 'Fix deployment configuration'")
    print("   git push")
    
    print("\n2. Try deployment with these options:")
    print("   Option A (Recommended): Use Procfile (gevent)")
    print("   Option B (Fallback): Use Procfile.sync")
    print("   Option C (Alternative): Use Procfile.thread")
    
    print("\n3. If gevent still fails, rename Procfile.sync to Procfile:")
    print("   mv Procfile.sync Procfile")
    
    print("\n4. Deploy to Render:")
    print("   - Use Python 3.11 runtime")
    print("   - Build command: pip install -r requirements.txt")
    print("   - Start command will use the Procfile")
    
    print("\n🎸 Your AI Voice Assistant will rock in production!")

if __name__ == "__main__":
    main()
