#!/usr/bin/env python3
"""
Complete Render Deployment Guide for Steve Perry AI Voice Assistant
"""

import os
import sys
import json
import subprocess
import requests
import time
from datetime import datetime

def check_prerequisites():
    """Check all deployment prerequisites"""
    print("🔍 CHECKING DEPLOYMENT PREREQUISITES")
    print("=" * 50)
    
    checks = {
        'git_repo': False,
        'required_files': False,
        'environment_vars': False,
        'dependencies': False
    }
    
    # Check if we're in a git repository
    try:
        subprocess.run(['git', 'status'], capture_output=True, check=True)
        checks['git_repo'] = True
        print("✅ Git repository detected")
    except:
        print("❌ Not in a git repository")
        print("   Run: git init && git add . && git commit -m 'Initial commit'")
    
    # Check required files
    required_files = ['app.py', 'requirements.txt', 'Procfile', 'runtime.txt']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    checks['required_files'] = len(missing_files) == 0
    
    # Check environment variables
    required_env_vars = [
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER',
        'OPENAI_API_KEY', 'ELEVENLABS_API_KEY', 'ELEVENLABS_VOICE_ID'
    ]
    
    missing_env_vars = []
    for var in required_env_vars:
        if os.environ.get(var):
            print(f"✅ {var} configured")
        else:
            print(f"⚠️  {var} not set (will need to set in Render)")
            missing_env_vars.append(var)
    
    checks['environment_vars'] = len(missing_env_vars) < len(required_env_vars)
    
    # Check if dependencies can be installed
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'check'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies check passed")
            checks['dependencies'] = True
        else:
            print("⚠️  Dependency issues detected")
            print(result.stdout)
    except:
        print("⚠️  Could not check dependencies")
    
    return checks

def create_deployment_files():
    """Create all necessary deployment files"""
    print("\n📝 CREATING DEPLOYMENT FILES")
    print("=" * 40)
    
    files_created = []
    
    # Create requirements.txt
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
cryptography>=41.0.0"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    files_created.append('requirements.txt')
    print("✅ Created requirements.txt")
    
    # Create Procfile
    procfile_content = "web: gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    files_created.append('Procfile')
    print("✅ Created Procfile")
    
    # Create runtime.txt
    runtime_content = "python-3.11.0"
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    files_created.append('runtime.txt')
    print("✅ Created runtime.txt")
    
    # Create fallback Procfiles
    fallback_procfiles = {
        'Procfile.sync': 'web: gunicorn -w 1 --bind 0.0.0.0:$PORT app:app',
        'Procfile.thread': 'web: gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app',
        'Procfile.dev': 'web: python app.py'
    }
    
    for filename, content in fallback_procfiles.items():
        with open(filename, 'w') as f:
            f.write(content)
        files_created.append(filename)
        print(f"✅ Created {filename}")
    
    return files_created

def test_local_deployment():
    """Test the app locally before deploying"""
    print("\n🧪 TESTING LOCAL DEPLOYMENT")
    print("=" * 40)
    
    test_results = {
        'app_import': False,
        'gunicorn_gevent': False,
        'gunicorn_sync': False,
        'health_endpoint': False
    }
    
    # Test app import
    try:
        import app
        print("✅ App imports successfully")
        test_results['app_import'] = True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return test_results
    
    # Test gunicorn with gevent
    print("\nTesting gunicorn with gevent...")
    try:
        process = subprocess.Popen([
            'gunicorn', '--worker-class', 'gevent', '-w', '1',
            '--bind', '127.0.0.1:5001', 'app:app'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Gunicorn with gevent works")
            test_results['gunicorn_gevent'] = True
            
            # Test health endpoint
            try:
                response = requests.get('http://127.0.0.1:5001/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Health endpoint responds")
                    test_results['health_endpoint'] = True
                else:
                    print(f"⚠️  Health endpoint returned {response.status_code}")
            except Exception as e:
                print(f"⚠️  Health endpoint test failed: {e}")
            
            process.terminate()
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Gunicorn with gevent failed: {stderr.decode()}")
    except Exception as e:
        print(f"❌ Gunicorn gevent test error: {e}")
    
    # Test gunicorn sync fallback
    if not test_results['gunicorn_gevent']:
        print("\nTesting gunicorn sync fallback...")
        try:
            process = subprocess.Popen([
                'gunicorn', '-w', '1', '--bind', '127.0.0.1:5002', 'app:app'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(5)
            
            if process.poll() is None:
                print("✅ Gunicorn sync works")
                test_results['gunicorn_sync'] = True
                process.terminate()
                process.wait()
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Gunicorn sync failed: {stderr.decode()}")
        except Exception as e:
            print(f"❌ Gunicorn sync test error: {e}")
    
    return test_results

def generate_render_instructions(test_results):
    """Generate specific Render deployment instructions"""
    print("\n🚀 RENDER DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    # Determine best deployment strategy
    if test_results['gunicorn_gevent']:
        deployment_strategy = "gevent"
        start_command = "gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
    elif test_results['gunicorn_sync']:
        deployment_strategy = "sync"
        start_command = "gunicorn -w 1 --bind 0.0.0.0:$PORT app:app"
    else:
        deployment_strategy = "dev"
        start_command = "python app.py"
    
    print(f"📋 RECOMMENDED STRATEGY: {deployment_strategy.upper()}")
    print(f"🚀 START COMMAND: {start_command}")
    
    print("\n📝 STEP-BY-STEP RENDER DEPLOYMENT:")
    print("1. Commit your changes:")
    print("   git add .")
    print("   git commit -m 'Prepare for Render deployment'")
    print("   git push origin main")
    
    print("\n2. Go to render.com and sign up/login")
    
    print("\n3. Create a new Web Service:")
    print("   • Click 'New +' → 'Web Service'")
    print("   • Connect your GitHub repository")
    print("   • Select your AI Voice Assistant repo")
    
    print("\n4. Configure the service:")
    print("   • Name: steve-perry-ai-voice-assistant")
    print("   • Environment: Python 3")
    print("   • Region: Oregon (US West)")
    print("   • Branch: main")
    print(f"   • Build Command: pip install -r requirements.txt")
    print(f"   • Start Command: {start_command}")
    print("   • Instance Type: Free")
    
    print("\n5. Set Environment Variables:")
    env_vars = [
        "TWILIO_ACCOUNT_SID=your_twilio_account_sid",
        "TWILIO_AUTH_TOKEN=your_twilio_auth_token", 
        "TWILIO_PHONE_NUMBER=your_twilio_phone_number",
        "OPENAI_API_KEY=your_openai_api_key",
        "ELEVENLABS_API_KEY=your_elevenlabs_api_key",
        "ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id",
        "SECRET_KEY=your_secret_key_here",
        "PYTHON_VERSION=3.11.0"
    ]
    
    for var in env_vars:
        print(f"   • {var}")
    
    print("\n6. Deploy:")
    print("   • Click 'Create Web Service'")
    print("   • Wait 5-10 minutes for deployment")
    print("   • Your app will be at: https://steve-perry-ai-voice-assistant.onrender.com")
    
    print("\n7. Configure Twilio Webhooks:")
    print("   In Twilio Console → Phone Numbers → Your Number:")
    print("   • Voice URL: https://your-app.onrender.com/answer")
    print("   • Status Callback: https://your-app.onrender.com/call_status")
    print("   • Recording Callback: https://your-app.onrender.com/recording_complete")
    
    return deployment_strategy

def create_deployment_report():
    """Create a comprehensive deployment report"""
    print("\n📊 CREATING DEPLOYMENT REPORT")
    print("=" * 40)
    
    # Check prerequisites
    prereq_checks = check_prerequisites()
    
    # Create deployment files
    files_created = create_deployment_files()
    
    # Test local deployment
    test_results = test_local_deployment()
    
    # Generate instructions
    deployment_strategy = generate_render_instructions(test_results)
    
    # Create report
    report = {
        'timestamp': datetime.now().isoformat(),
        'prerequisites': prereq_checks,
        'files_created': files_created,
        'test_results': test_results,
        'deployment_strategy': deployment_strategy,
        'ready_for_deployment': all(prereq_checks.values()) and test_results['app_import']
    }
    
    # Save report
    with open('render_deployment_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Report saved: render_deployment_report.json")
    
    return report

def main():
    """Main deployment guide function"""
    print("🚀 STEVE PERRY AI VOICE ASSISTANT - RENDER DEPLOYMENT GUIDE")
    print("=" * 70)
    
    # Create comprehensive deployment report
    report = create_deployment_report()
    
    print("\n🎯 DEPLOYMENT SUMMARY:")
    print("=" * 30)
    
    if report['ready_for_deployment']:
        print("✅ READY FOR DEPLOYMENT!")
        print(f"🚀 Strategy: {report['deployment_strategy'].upper()}")
        print("📋 Follow the instructions above to deploy on Render")
    else:
        print("⚠️  ISSUES DETECTED:")
        for check, passed in report['prerequisites'].items():
            if not passed:
                print(f"   ❌ {check}")
        
        if not report['test_results']['app_import']:
            print("   ❌ App import failed - fix app.py issues first")
    
    print(f"\n📁 Files created: {len(report['files_created'])}")
    for file in report['files_created']:
        print(f"   • {file}")
    
    print(f"\n🎸 Your Steve Perry AI is ready to rock on Render! 🎤")
    
    if not report['ready_for_deployment']:
        print("\n🔧 Fix the issues above and run this script again.")

if __name__ == "__main__":
    main()
