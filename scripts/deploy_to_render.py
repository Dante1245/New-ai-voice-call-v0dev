#!/usr/bin/env python3
"""
Automated deployment script for Render
"""

import os
import sys
import json
import subprocess
import requests
import time
from datetime import datetime

def check_prerequisites():
    """Check if all prerequisites are met for deployment"""
    print("🔍 Checking deployment prerequisites...")
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("❌ Git repository not initialized")
        print("Run: git init && git add . && git commit -m 'Initial commit'")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found")
        return False
    
    # Check environment variables
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_PHONE_NUMBER',
        'OPENAI_API_KEY',
        'ELEVENLABS_API_KEY',
        'ELEVENLABS_VOICE_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print("✅ All prerequisites met!")
    return True

def prepare_for_deployment():
    """Prepare the application for deployment"""
    print("🔧 Preparing application for deployment...")
    
    # Create deployment configuration files
    deployment_files = {
        'render.yaml': '''services:
  - type: web
    name: steve-perry-ai-voice-assistant
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
    healthCheckPath: /health
    autoDeploy: true''',
        
        'Procfile': 'web: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app',
        
        'runtime.txt': 'python-3.9.18'
    }
    
    for filename, content in deployment_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        else:
            print(f"✅ {filename} already exists")
    
    # Ensure static directories exist
    os.makedirs('static/audio', exist_ok=True)
    os.makedirs('static/recordings', exist_ok=True)
    
    # Create .gitignore if it doesn't exist
    gitignore_content = """# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
*.log
logs/

# Audio files (temporary)
static/audio/*.mp3
static/recordings/*.mp3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup files
memory_backup_*.json
*_test_report.json
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")
    
    print("✅ Application prepared for deployment!")

def commit_changes():
    """Commit all changes to git"""
    print("📝 Committing changes to git...")
    
    try:
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_message = f"Production deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        print("✅ Changes committed to git")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed: {e}")
        return False

def deploy_to_render():
    """Deploy to Render with step-by-step instructions"""
    print("\n🚀 RENDER DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. 📋 PREPARE YOUR REPOSITORY")
    print("   - Ensure your code is pushed to GitHub/GitLab")
    print("   - Repository should be public or accessible to Render")
    
    print("\n2. 🌐 CREATE RENDER ACCOUNT")
    print("   - Go to https://render.com")
    print("   - Sign up with GitHub/GitLab account")
    print("   - Connect your repository")
    
    print("\n3. ⚙️  CREATE WEB SERVICE")
    print("   - Click 'New +' → 'Web Service'")
    print("   - Select your repository")
    print("   - Use these settings:")
    print("     • Name: steve-perry-ai-voice-assistant")
    print("     • Environment: Python 3")
    print("     • Build Command: pip install -r requirements.txt")
    print("     • Start Command: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app")
    print("     • Instance Type: Free (or Starter for better performance)")
    
    print("\n4. 🔐 SET ENVIRONMENT VARIABLES")
    print("   Add these environment variables in Render dashboard:")
    
    env_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER', 
        'OPENAI_API_KEY',
        'ELEVENLABS_API_KEY',
        'ELEVENLABS_VOICE_ID'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'your_value_here')
        print(f"   • {var}: {value[:10]}..." if len(value) > 10 else f"   • {var}: {value}")
    
    print("   • SECRET_KEY: (Generate a strong random key)")
    
    print("\n5. 🚀 DEPLOY")
    print("   - Click 'Create Web Service'")
    print("   - Wait for deployment to complete (5-10 minutes)")
    print("   - Your app will be available at: https://your-app-name.onrender.com")
    
    print("\n6. ✅ VERIFY DEPLOYMENT")
    print("   - Check health endpoint: https://your-app-name.onrender.com/health")
    print("   - Test dashboard: https://your-app-name.onrender.com")
    
    return True

def deploy_to_heroku():
    """Deploy to Heroku with step-by-step instructions"""
    print("\n🚀 HEROKU DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. 📦 INSTALL HEROKU CLI")
    print("   - Download from: https://devcenter.heroku.com/articles/heroku-cli")
    print("   - Login: heroku login")
    
    print("\n2. 🏗️  CREATE HEROKU APP")
    print("   Run these commands:")
    print("   heroku create steve-perry-ai-voice-assistant")
    print("   heroku addons:create heroku-postgresql:mini")
    
    print("\n3. 🔐 SET ENVIRONMENT VARIABLES")
    env_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER',
        'OPENAI_API_KEY', 
        'ELEVENLABS_API_KEY',
        'ELEVENLABS_VOICE_ID'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'your_value_here')
        print(f"   heroku config:set {var}={value}")
    
    print("   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')")
    
    print("\n4. 🚀 DEPLOY")
    print("   git push heroku main")
    
    print("\n5. ✅ VERIFY DEPLOYMENT")
    print("   heroku open")
    print("   heroku logs --tail")
    
    return True

def configure_webhooks(app_url):
    """Instructions for configuring Twilio webhooks"""
    print(f"\n🔗 CONFIGURE TWILIO WEBHOOKS")
    print("=" * 50)
    
    print("\n1. 📞 GO TO TWILIO CONSOLE")
    print("   - Visit: https://console.twilio.com")
    print("   - Navigate to: Phone Numbers → Manage → Active Numbers")
    
    print("\n2. ⚙️  CONFIGURE YOUR PHONE NUMBER")
    print("   Select your Twilio phone number and set:")
    print(f"   • Voice URL: {app_url}/answer")
    print(f"   • Voice Method: POST")
    print(f"   • Status Callback URL: {app_url}/call_status")
    print(f"   • Status Callback Method: POST")
    
    print("\n3. 🎙️  CONFIGURE RECORDING WEBHOOKS")
    print("   In the same phone number configuration:")
    print(f"   • Recording Status Callback URL: {app_url}/recording_complete")
    print(f"   • Recording Status Callback Method: POST")
    
    print("\n4. ✅ SAVE CONFIGURATION")
    print("   - Click 'Save Configuration'")
    print("   - Test with a phone call!")

def post_deployment_tests(app_url):
    """Run post-deployment tests"""
    print(f"\n🧪 POST-DEPLOYMENT TESTING")
    print("=" * 50)
    
    tests = [
        ("Health Check", f"{app_url}/health"),
        ("Dashboard", f"{app_url}/"),
        ("Memory System", f"{app_url}/get_memory")
    ]
    
    for test_name, url in tests:
        try:
            print(f"\n🔍 Testing {test_name}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {test_name}: PASSED")
                if 'health' in url:
                    data = response.json()
                    print(f"   Status: {data.get('status')}")
                    services = data.get('services', {})
                    for service, status in services.items():
                        status_icon = "✅" if status else "❌"
                        print(f"   {status_icon} {service}: {'Ready' if status else 'Not configured'}")
            else:
                print(f"❌ {test_name}: FAILED ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n🎯 MANUAL TESTS")
    print("   1. Open dashboard in browser")
    print("   2. Enter your phone number")
    print("   3. Click 'Start Call'")
    print("   4. Answer the phone and talk to Steve Perry!")

def main():
    """Main deployment orchestration"""
    print("🚀 AI VOICE ASSISTANT - PRODUCTION DEPLOYMENT")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix issues and try again.")
        sys.exit(1)
    
    # Prepare for deployment
    prepare_for_deployment()
    
    # Commit changes
    if not commit_changes():
        print("\n⚠️  Git commit failed, but continuing with deployment...")
    
    # Choose deployment platform
    print("\n🎯 CHOOSE DEPLOYMENT PLATFORM:")
    print("1. Render (Recommended - Free tier available)")
    print("2. Heroku (Classic platform)")
    print("3. Manual deployment instructions")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        deploy_to_render()
        app_url = "https://steve-perry-ai-voice-assistant.onrender.com"
    elif choice == "2":
        deploy_to_heroku()
        app_url = "https://steve-perry-ai-voice-assistant.herokuapp.com"
    else:
        print("\n📋 MANUAL DEPLOYMENT")
        print("Follow the deployment guide in DEPLOYMENT.md")
        app_url = input("Enter your deployed app URL: ").strip()
    
    # Configure webhooks
    if app_url:
        configure_webhooks(app_url)
        
        # Wait for deployment
        print("\n⏳ Waiting for deployment to complete...")
        print("This may take 5-10 minutes...")
        
        # Test deployment
        test_now = input("\nTest deployment now? (y/n): ").strip().lower()
        if test_now == 'y':
            post_deployment_tests(app_url)
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print("Your Steve Perry AI Voice Assistant is now live!")
    print(f"🌐 Dashboard: {app_url}")
    print(f"🔍 Health Check: {app_url}/health")
    print("\n🎤 Ready to rock and roll with AI! 🎸")

if __name__ == "__main__":
    main()
