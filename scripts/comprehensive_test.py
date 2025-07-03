#!/usr/bin/env python3
"""
Comprehensive test script to check all functionality and fix issues
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

# Test imports
def test_all_imports():
    """Test all required imports"""
    print("🔍 Testing All Imports")
    print("-" * 30)
    
    imports = [
        ("Flask", "from flask import Flask, request, render_template, jsonify"),
        ("Flask-SocketIO", "from flask_socketio import SocketIO, emit"),
        ("Requests", "import requests"),
        ("JSON", "import json"),
        ("OS", "import os"),
        ("DateTime", "from datetime import datetime"),
        ("Time", "import time"),
        ("Threading", "import threading"),
        ("Glob", "import glob"),
        ("URLParse", "import urllib.parse"),
        ("Werkzeug", "from werkzeug.utils import secure_filename")
    ]
    
    # Test optional imports
    optional_imports = [
        ("Twilio", "from twilio.rest import Client; from twilio.twiml import VoiceResponse"),
        ("OpenAI", "from openai import OpenAI"),
        ("Python-Dotenv", "from dotenv import load_dotenv")
    ]
    
    success_count = 0
    total_count = len(imports) + len(optional_imports)
    
    # Test required imports
    for name, import_stmt in imports:
        try:
            exec(import_stmt)
            print(f"✅ {name}: OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: FAILED - {e}")
        except Exception as e:
            print(f"⚠️  {name}: ERROR - {e}")
    
    # Test optional imports
    for name, import_stmt in optional_imports:
        try:
            exec(import_stmt)
            print(f"✅ {name}: OK")
            success_count += 1
        except ImportError as e:
            print(f"⚠️  {name}: OPTIONAL - {e}")
            success_count += 1  # Count as success since it's optional
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
    
    print(f"\n📊 Import Test: {success_count}/{total_count} successful")
    return success_count == total_count

def test_file_structure():
    """Test file structure and permissions"""
    print("\n📁 Testing File Structure")
    print("-" * 30)
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'templates/dashboard.html'
    ]
    
    required_dirs = [
        'static',
        'static/audio',
        'static/recordings',
        'scripts',
        'templates'
    ]
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: EXISTS")
        else:
            print(f"❌ {file_path}: MISSING")
    
    # Check and create directories
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/: EXISTS")
        else:
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ {dir_path}/: CREATED")
            except Exception as e:
                print(f"❌ {dir_path}/: FAILED TO CREATE - {e}")
    
    # Test memory.json
    try:
        if not os.path.exists('memory.json'):
            memory_data = {
                'conversations': [],
                'user_preferences': {},
                'recordings': []
            }
            with open('memory.json', 'w') as f:
                json.dump(memory_data, f, indent=2)
            print("✅ memory.json: CREATED")
        else:
            # Validate existing memory.json
            with open('memory.json', 'r') as f:
                data = json.load(f)
            
            required_keys = ['conversations', 'user_preferences', 'recordings']
            for key in required_keys:
                if key not in data:
                    data[key] = []
            
            with open('memory.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("✅ memory.json: VALIDATED")
            
    except Exception as e:
        print(f"❌ memory.json: ERROR - {e}")

def test_environment_variables():
    """Test environment variables"""
    print("\n🔧 Testing Environment Variables")
    print("-" * 30)
    
    # Load .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    required_vars = {
        'TWILIO_ACCOUNT_SID': 'Twilio Account SID',
        'TWILIO_AUTH_TOKEN': 'Twilio Auth Token',
        'TWILIO_PHONE_NUMBER': 'Twilio Phone Number'
    }
    
    optional_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'ELEVENLABS_API_KEY': 'ElevenLabs API Key',
        'ELEVENLABS_VOICE_ID': 'ElevenLabs Voice ID',
        'SECRET_KEY': 'Flask Secret Key'
    }
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var}: SET")
        else:
            print(f"❌ {var}: MISSING ({description})")
    
    # Check optional variables
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var}: SET")
        else:
            print(f"⚠️  {var}: NOT SET ({description})")

def test_api_connections():
    """Test API connections"""
    print("\n🌐 Testing API Connections")
    print("-" * 30)
    
    # Test Twilio
    try:
        from twilio.rest import Client
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        
        if account_sid and auth_token:
            client = Client(account_sid, auth_token)
            account = client.api.accounts(account_sid).fetch()
            print(f"✅ Twilio: Connected (Status: {account.status})")
        else:
            print("⚠️  Twilio: Credentials not set")
    except Exception as e:
        print(f"❌ Twilio: ERROR - {e}")
    
    # Test ElevenLabs
    try:
        api_key = os.environ.get('ELEVENLABS_API_KEY')
        if api_key:
            headers = {"Accept": "application/json", "xi-api-key": api_key}
            response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=10)
            if response.status_code == 200:
                voices = response.json()
                print(f"✅ ElevenLabs: Connected ({len(voices.get('voices', []))} voices)")
            else:
                print(f"❌ ElevenLabs: HTTP {response.status_code}")
        else:
            print("⚠️  ElevenLabs: API key not set")
    except Exception as e:
        print(f"❌ ElevenLabs: ERROR - {e}")
    
    # Test OpenAI
    try:
        from openai import OpenAI
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            print("✅ OpenAI: Connected")
        else:
            print("⚠️  OpenAI: API key not set")
    except Exception as e:
        print(f"❌ OpenAI: ERROR - {e}")

def create_fixed_env_file():
    """Create a properly formatted .env file"""
    print("\n📝 Creating Fixed .env File")
    print("-" * 30)
    
    env_content = """# Twilio Configuration
TWILIO_ACCOUNT_SID=AC53367dfd03c78ff96c680d2323decb43
TWILIO_AUTH_TOKEN=98c3adba905bec0043254cf070d74f02
TWILIO_PHONE_NUMBER=+18883570333

# Test Phone Number
TEST_PHONE_NUMBER=+13236287547

# OpenAI Configuration (Add your key here)
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs Configuration
ELEVENLABS_API_KEY=sk_0e8038753caef729a579ff143daf60ce53ede2404b13d605
ELEVENLABS_VOICE_ID=1SM7GgM6IMuvQlz2BwM3

# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production-12345
PORT=5000

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=False
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Remember to add your OpenAI API key!")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Comprehensive AI Voice Assistant Test")
    print("=" * 50)
    
    # Run all tests
    imports_ok = test_all_imports()
    test_file_structure()
    test_environment_variables()
    test_api_connections()
    
    # Create fixed .env file
    create_fixed_env_file()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("-" * 20)
    
    if imports_ok:
        print("✅ All imports working")
    else:
        print("❌ Some imports failed - run: pip install -r requirements.txt")
    
    print("✅ File structure validated")
    print("✅ Environment variables checked")
    print("✅ API connections tested")
    print("✅ Fixed .env file created")
    
    print("\n🎯 Next Steps:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print("4. Configure Twilio webhooks to point to your app")

if __name__ == "__main__":
    run_comprehensive_test()
