#!/usr/bin/env python3
"""
Comprehensive module error checker and fixer
"""

import sys
import subprocess
import importlib
import os

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python Version")
    print("-" * 30)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version compatible")
        return True

def install_missing_module(module_name, pip_name=None):
    """Install a missing module"""
    if pip_name is None:
        pip_name = module_name
    
    try:
        print(f"📦 Installing {pip_name}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", pip_name
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_fix_modules():
    """Check all required modules and install missing ones"""
    print("\n🔍 Checking Required Modules")
    print("-" * 30)
    
    # Core modules (should be available in Python standard library)
    core_modules = [
        ("json", None),
        ("os", None),
        ("sys", None),
        ("time", None),
        ("datetime", None),
        ("threading", None),
        ("urllib.parse", None),
        ("glob", None)
    ]
    
    # Third-party modules with their pip install names
    third_party_modules = [
        ("flask", "Flask==2.3.3"),
        ("flask_socketio", "Flask-SocketIO==5.3.6"),
        ("requests", "requests==2.31.0"),
        ("eventlet", "eventlet==0.33.3"),
        ("werkzeug", "Werkzeug==2.3.7"),
        ("socketio", "python-socketio==5.9.0"),
        ("engineio", "python-engineio==4.7.1")
    ]
    
    # Optional modules
    optional_modules = [
        ("twilio", "twilio==8.10.0"),
        ("openai", "openai==1.3.0"),
        ("dotenv", "python-dotenv==1.0.0")
    ]
    
    all_good = True
    
    # Check core modules
    print("Core Python modules:")
    for module_name, _ in core_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"❌ {module_name} - CRITICAL ERROR")
            all_good = False
    
    # Check and install third-party modules
    print("\nThird-party modules:")
    for module_name, pip_name in third_party_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"❌ {module_name} - Installing...")
            if install_missing_module(module_name, pip_name):
                print(f"✅ {module_name} - Installed successfully")
            else:
                print(f"❌ {module_name} - Installation failed")
                all_good = False
    
    # Check optional modules
    print("\nOptional modules:")
    for module_name, pip_name in optional_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"⚠️  {module_name} - Installing...")
            if install_missing_module(module_name, pip_name):
                print(f"✅ {module_name} - Installed successfully")
            else:
                print(f"⚠️  {module_name} - Installation failed (optional)")
    
    return all_good

def test_specific_imports():
    """Test specific import statements that might fail"""
    print("\n🧪 Testing Specific Import Statements")
    print("-" * 30)
    
    import_tests = [
        ("Flask basics", "from flask import Flask, request, render_template, jsonify"),
        ("Flask-SocketIO", "from flask_socketio import SocketIO, emit"),
        ("Werkzeug utils", "from werkzeug.utils import secure_filename"),
        ("Requests", "import requests"),
        ("JSON", "import json"),
        ("OS operations", "import os"),
        ("Date/Time", "from datetime import datetime"),
        ("Threading", "import threading"),
        ("Time", "import time"),
        ("URL parsing", "import urllib.parse"),
        ("File globbing", "import glob")
    ]
    
    optional_tests = [
        ("Twilio Client", "from twilio.rest import Client"),
        ("Twilio TwiML", "from twilio.twiml import VoiceResponse"),
        ("OpenAI", "from openai import OpenAI"),
        ("Python-dotenv", "from dotenv import load_dotenv")
    ]
    
    success_count = 0
    total_count = len(import_tests)
    
    # Test required imports
    for test_name, import_stmt in import_tests:
        try:
            exec(import_stmt)
            print(f"✅ {test_name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {test_name}: {e}")
        except Exception as e:
            print(f"⚠️  {test_name}: {e}")
    
    # Test optional imports
    optional_success = 0
    for test_name, import_stmt in optional_tests:
        try:
            exec(import_stmt)
            print(f"✅ {test_name}")
            optional_success += 1
        except ImportError as e:
            print(f"⚠️  {test_name}: {e} (optional)")
        except Exception as e:
            print(f"❌ {test_name}: {e}")
    
    print(f"\n📊 Required imports: {success_count}/{total_count}")
    print(f"📊 Optional imports: {optional_success}/{len(optional_tests)}")
    
    return success_count == total_count

def check_flask_compatibility():
    """Check Flask and related modules compatibility"""
    print("\n🌶️  Checking Flask Compatibility")
    print("-" * 30)
    
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        
        # Test Flask app creation
        app = flask.Flask(__name__)
        print("✅ Flask app creation works")
        
        # Test Flask-SocketIO
        try:
            import flask_socketio
            print(f"✅ Flask-SocketIO version: {flask_socketio.__version__}")
            
            # Test SocketIO creation
            socketio = flask_socketio.SocketIO(app)
            print("✅ SocketIO creation works")
            
        except ImportError:
            print("❌ Flask-SocketIO not available")
            return False
        except Exception as e:
            print(f"❌ Flask-SocketIO error: {e}")
            return False
            
        return True
        
    except ImportError:
        print("❌ Flask not available")
        return False
    except Exception as e:
        print(f"❌ Flask error: {e}")
        return False

def create_requirements_txt():
    """Create a comprehensive requirements.txt file"""
    print("\n📝 Creating Fixed requirements.txt")
    print("-" * 30)
    
    requirements = """# Core Flask and Web Framework
Flask==2.3.3
Flask-SocketIO==5.3.6
Werkzeug==2.3.7

# WebSocket and Async Support
python-socketio==5.9.0
python-engineio==4.7.1
eventlet==0.33.3

# HTTP Requests
requests==2.31.0

# WSGI Server for Production
gunicorn==21.2.0

# Environment Variables
python-dotenv==1.0.0

# Twilio SDK
twilio==8.10.0

# OpenAI SDK
openai==1.3.0

# Additional utilities
urllib3==1.26.18
certifi>=2023.7.22
"""
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print("✅ requirements.txt created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
        return False

def install_all_requirements():
    """Install all requirements from requirements.txt"""
    print("\n📦 Installing All Requirements")
    print("-" * 30)
    
    try:
        # Upgrade pip first
        print("⬆️  Upgrading pip...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], stdout=subprocess.DEVNULL)
        
        # Install requirements
        print("📦 Installing requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("✅ All requirements installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def fix_common_module_issues():
    """Fix common module-related issues"""
    print("\n🔧 Fixing Common Module Issues")
    print("-" * 30)
    
    fixes_applied = []
    
    # Fix 1: Ensure pip is up to date
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fixes_applied.append("Updated pip")
    except:
        pass
    
    # Fix 2: Install wheel for better package building
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "wheel"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fixes_applied.append("Installed wheel")
    except:
        pass
    
    # Fix 3: Clear pip cache if needed
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "cache", "purge"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fixes_applied.append("Cleared pip cache")
    except:
        pass
    
    # Fix 4: Install setuptools
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "setuptools"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fixes_applied.append("Updated setuptools")
    except:
        pass
    
    if fixes_applied:
        print("✅ Applied fixes:", ", ".join(fixes_applied))
    else:
        print("ℹ️  No fixes needed")

def run_module_check():
    """Run comprehensive module check"""
    print("🔍 AI Voice Assistant - Module Error Checker")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    if not python_ok:
        print("\n❌ Python version incompatible. Please upgrade to Python 3.8+")
        return False
    
    # Apply common fixes
    fix_common_module_issues()
    
    # Create fixed requirements.txt
    create_requirements_txt()
    
    # Install all requirements
    install_ok = install_all_requirements()
    
    # Check modules
    modules_ok = check_and_fix_modules()
    
    # Test specific imports
    imports_ok = test_specific_imports()
    
    # Check Flask compatibility
    flask_ok = check_flask_compatibility()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Module Check Summary")
    print("-" * 25)
    print(f"Python Version: {'✅' if python_ok else '❌'}")
    print(f"Requirements Install: {'✅' if install_ok else '❌'}")
    print(f"Module Availability: {'✅' if modules_ok else '❌'}")
    print(f"Import Tests: {'✅' if imports_ok else '❌'}")
    print(f"Flask Compatibility: {'✅' if flask_ok else '❌'}")
    
    all_ok = all([python_ok, install_ok, modules_ok, imports_ok, flask_ok])
    
    if all_ok:
        print("\n🎉 All modules working correctly!")
        print("✅ Your environment is ready for the AI Voice Assistant")
        print("\nNext steps:")
        print("1. python app.py")
        print("2. Open http://localhost:5000")
    else:
        print("\n⚠️  Some issues found. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure you have Python 3.8+")
        print("2. Try: pip install --upgrade pip")
        print("3. Try: pip install -r requirements.txt --force-reinstall")
        print("4. Check your internet connection")
    
    return all_ok

if __name__ == "__main__":
    run_module_check()
