#!/usr/bin/env python3
"""
Script to verify all required imports are working
"""

def test_imports():
    """Test all required imports for the AI Voice Assistant"""
    print("🔍 Verifying Python Imports")
    print("=" * 40)
    
    imports_to_test = [
        ("Flask", "from flask import Flask, request, render_template, jsonify"),
        ("Flask-SocketIO", "from flask_socketio import SocketIO, emit"),
        ("Twilio", "from twilio.rest import Client"),
        ("Twilio TwiML", "from twilio.twiml import VoiceResponse"),
        ("OpenAI", "from openai import OpenAI"),
        ("Requests", "import requests"),
        ("JSON", "import json"),
        ("OS", "import os"),
        ("DateTime", "from datetime import datetime"),
        ("Threading", "import threading"),
        ("Time", "import time"),
        ("Python-Dotenv", "from dotenv import load_dotenv")
    ]
    
    success_count = 0
    failed_imports = []
    
    for name, import_statement in imports_to_test:
        try:
            exec(import_statement)
            print(f"✅ {name}: Import successful")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
            failed_imports.append(name)
        except Exception as e:
            print(f"⚠️  {name}: Unexpected error - {e}")
            failed_imports.append(name)
    
    print(f"\n📊 Import Summary: {success_count}/{len(imports_to_test)} imports successful")
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        print("\nTo fix missing packages, run:")
        print("pip install -r requirements.txt")
        print("or")
        print("python scripts/install_dependencies.py")
        return False
    else:
        print("\n🎉 All imports working correctly!")
        print("Your environment is ready for the AI Voice Assistant!")
        return True

def test_twilio_specifically():
    """Test Twilio imports specifically since it was missing"""
    print("\n🔧 Testing Twilio Module Specifically")
    print("-" * 40)
    
    try:
        from twilio.rest import Client
        print("✅ Twilio Client: Import successful")
        
        from twilio.twiml import VoiceResponse
        print("✅ Twilio TwiML: Import successful")
        
        # Test basic functionality
        try:
            response = VoiceResponse()
            response.say("Test")
            print("✅ Twilio TwiML: Basic functionality working")
            print(f"   Generated TwiML: {str(response)[:50]}...")
        except Exception as e:
            print(f"⚠️  Twilio TwiML: Functionality test failed - {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Twilio import failed: {e}")
        print("\nTo install Twilio:")
        print("pip install twilio==8.10.0")
        return False

if __name__ == "__main__":
    print("🐍 Python Environment Verification")
    print("=" * 50)
    
    # Test all imports
    imports_ok = test_imports()
    
    # Test Twilio specifically
    twilio_ok = test_twilio_specifically()
    
    print("\n" + "=" * 50)
    if imports_ok and twilio_ok:
        print("🚀 Environment Ready! You can now run the AI Voice Assistant.")
        print("\nNext steps:")
        print("1. python scripts/test_configuration.py")
        print("2. python app.py")
    else:
        print("⚠️  Please install missing dependencies before proceeding.")
