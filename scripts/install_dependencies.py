#!/usr/bin/env python3
"""
Script to install all required dependencies for the AI Voice Assistant
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_package(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    """Install all required dependencies"""
    print("🔧 Installing AI Voice Assistant Dependencies")
    print("=" * 50)
    
    # List of required packages
    packages = [
        "Flask==2.3.3",
        "Flask-SocketIO==5.3.6", 
        "twilio==8.10.0",
        "openai==1.3.0",
        "requests==2.31.0",
        "python-socketio==5.9.0",
        "python-engineio==4.7.1",
        "eventlet==0.33.3",
        "gunicorn==21.2.0",
        "python-dotenv==1.0.0"
    ]
    
    # Check which packages need installation
    package_checks = {
        "Flask": "flask",
        "Flask-SocketIO": "flask_socketio",
        "Twilio": "twilio",
        "OpenAI": "openai", 
        "Requests": "requests",
        "Python-SocketIO": "socketio",
        "Python-EngineIO": "engineio",
        "Eventlet": "eventlet",
        "Gunicorn": "gunicorn",
        "Python-Dotenv": "dotenv"
    }
    
    print("📋 Checking existing packages...")
    for name, import_name in package_checks.items():
        if check_package(import_name):
            print(f"✅ {name}: Already installed")
        else:
            print(f"❌ {name}: Not installed")
    
    print("\n🚀 Installing packages...")
    
    # Install packages from requirements
    success_count = 0
    for package in packages:
        package_name = package.split("==")[0]
        print(f"Installing {package_name}...")
        
        if install_package(package):
            print(f"✅ {package_name}: Installed successfully")
            success_count += 1
        else:
            print(f"❌ {package_name}: Installation failed")
    
    print(f"\n📊 Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Run: python scripts/test_configuration.py")
        print("3. Start the app: python app.py")
    else:
        print("⚠️  Some packages failed to install. Please check the errors above.")
        print("You may need to run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
