#!/usr/bin/env python3
"""
Test production configuration locally
"""

import sys
import os
import subprocess
import time
import requests
import threading
from datetime import datetime

def test_gevent_compatibility():
    """Test if gevent works with our configuration"""
    print("🧪 Testing Gevent Compatibility...")
    
    try:
        import gevent
        print("✅ Gevent imported successfully")
        
        # Test gevent monkey patching
        from gevent import monkey
        monkey.patch_all()
        print("✅ Gevent monkey patching works")
        
        return True
        
    except ImportError as e:
        print(f"❌ Gevent import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Gevent warning: {e}")
        return False

def test_flask_socketio_gevent():
    """Test Flask-SocketIO with gevent"""
    print("🧪 Testing Flask-SocketIO with Gevent...")
    
    try:
        from flask import Flask
        from flask_socketio import SocketIO
        
        # Create test app
        app = Flask(__name__)
        socketio = SocketIO(app, async_mode='gevent')
        
        print("✅ Flask-SocketIO with gevent initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Flask-SocketIO gevent test failed: {e}")
        return False

def test_gunicorn_gevent():
    """Test gunicorn with gevent worker"""
    print("🧪 Testing Gunicorn with Gevent Worker...")
    
    try:
        # Test if gunicorn can load gevent worker
        result = subprocess.run([
            'python', '-c', 
            'from gunicorn.workers.ggevent import GeventWorker; print("Gevent worker available")'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Gunicorn gevent worker available")
            return True
        else:
            print(f"❌ Gunicorn gevent worker test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Gunicorn gevent test error: {e}")
        return False

def test_app_startup():
    """Test if the app starts successfully"""
    print("🧪 Testing App Startup...")
    
    try:
        # Start the app in a subprocess
        env = os.environ.copy()
        env['PORT'] = '5001'  # Use different port for testing
        
        process = subprocess.Popen([
            'gunicorn', '--worker-class', 'gevent', '-w', '1', 
            '--bind', '0.0.0.0:5001', 'app:app'
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Check if process is running
        if process.poll() is None:
            print("✅ App started successfully with gevent")
            
            # Test health endpoint
            try:
                response = requests.get('http://localhost:5001/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Health endpoint responding")
                else:
                    print(f"⚠️  Health endpoint returned {response.status_code}")
            except Exception as e:
                print(f"⚠️  Health endpoint test failed: {e}")
            
            # Terminate the process
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ App failed to start: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ App startup test error: {e}")
        return False

def test_sync_fallback():
    """Test sync worker as fallback"""
    print("🧪 Testing Sync Worker Fallback...")
    
    try:
        # Start the app with sync worker
        env = os.environ.copy()
        env['PORT'] = '5002'
        
        process = subprocess.Popen([
            'gunicorn', '-w', '1', '--bind', '0.0.0.0:5002', 'app:app'
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Sync worker fallback works")
            
            # Test basic endpoint
            try:
                response = requests.get('http://localhost:5002/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Sync worker health check passed")
                else:
                    print(f"⚠️  Sync worker health check: {response.status_code}")
            except Exception as e:
                print(f"⚠️  Sync worker health test failed: {e}")
            
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Sync worker failed: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Sync worker test error: {e}")
        return False

def generate_deployment_report():
    """Generate deployment compatibility report"""
    print("\n📊 GENERATING DEPLOYMENT REPORT...")
    
    tests = [
        ("Gevent Compatibility", test_gevent_compatibility),
        ("Flask-SocketIO Gevent", test_flask_socketio_gevent),
        ("Gunicorn Gevent Worker", test_gunicorn_gevent),
        ("App Startup (Gevent)", test_app_startup),
        ("Sync Worker Fallback", test_sync_fallback)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'test_results': results,
        'recommendations': []
    }
    
    # Add recommendations based on results
    if results.get("Gevent Compatibility") and results.get("App Startup (Gevent)"):
        report['recommendations'].append("✅ Use gevent worker (Procfile)")
        report['deployment_command'] = "gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
    elif results.get("Sync Worker Fallback"):
        report['recommendations'].append("⚠️  Use sync worker fallback (Procfile.sync)")
        report['deployment_command'] = "gunicorn -w 1 --bind 0.0.0.0:$PORT app:app"
    else:
        report['recommendations'].append("❌ Manual configuration required")
        report['deployment_command'] = "python app.py"
    
    # Save report
    with open('production_test_report.json', 'w') as f:
        import json
        json.dump(report, f, indent=2)
    
    return report

def main():
    """Main testing function"""
    print("🧪 PRODUCTION CONFIGURATION TESTING")
    print("=" * 50)
    
    # Generate report
    report = generate_deployment_report()
    
    print("\n📋 TEST SUMMARY:")
    print("=" * 30)
    
    for test_name, result in report['test_results'].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 RECOMMENDED DEPLOYMENT:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print(f"\n🚀 DEPLOYMENT COMMAND:")
    print(f"   {report['deployment_command']}")
    
    print(f"\n📄 Full report saved to: production_test_report.json")
    
    # Provide next steps
    print(f"\n🎯 NEXT STEPS:")
    if "gevent" in report['deployment_command']:
        print("1. Use the main Procfile (already configured for gevent)")
        print("2. Deploy to Render with Python 3.11")
        print("3. Your app should work perfectly!")
    elif "sync" in report['deployment_command']:
        print("1. Rename Procfile.sync to Procfile:")
        print("   mv Procfile.sync Procfile")
        print("2. Deploy to Render")
        print("3. WebSocket features may be limited but core functionality will work")
    else:
        print("1. Contact support or use development mode")
        print("2. Consider using a different hosting platform")
    
    print(f"\n🎸 Ready to rock in production! 🎤")

if __name__ == "__main__":
    main()
