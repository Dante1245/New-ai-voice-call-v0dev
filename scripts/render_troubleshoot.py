#!/usr/bin/env python3
"""
Render deployment troubleshooting and fixes
"""

import os
import sys
import json
import subprocess
import requests
import time
from datetime import datetime

def diagnose_render_issues():
    """Diagnose common Render deployment issues"""
    print("🔍 DIAGNOSING RENDER DEPLOYMENT ISSUES")
    print("=" * 50)
    
    issues_found = []
    fixes_applied = []
    
    # Issue 1: Check Python version compatibility
    print("\n1. Checking Python version...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 11:
        print(f"✅ Python {python_version.major}.{python_version.minor} is compatible")
    else:
        print(f"⚠️  Python {python_version.major}.{python_version.minor} may have issues")
        issues_found.append("Python version compatibility")
    
    # Issue 2: Check requirements.txt
    print("\n2. Checking requirements.txt...")
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Check for problematic packages
        problematic_packages = ['eventlet']
        for package in problematic_packages:
            if package in content:
                print(f"⚠️  Found problematic package: {package}")
                issues_found.append(f"Problematic package: {package}")
        
        # Check for required packages
        required_packages = ['Flask', 'gunicorn', 'twilio', 'openai']
        missing_packages = []
        for package in required_packages:
            if package.lower() not in content.lower():
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            issues_found.append(f"Missing packages: {', '.join(missing_packages)}")
        else:
            print("✅ Required packages found")
    else:
        print("❌ requirements.txt not found")
        issues_found.append("Missing requirements.txt")
        
        # Create requirements.txt
        minimal_requirements = """Flask==2.3.3
Flask-SocketIO==5.3.6
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
twilio==8.10.0
openai==1.3.0
gevent==23.9.1"""
        
        with open('requirements.txt', 'w') as f:
            f.write(minimal_requirements)
        fixes_applied.append("Created requirements.txt")
        print("✅ Created requirements.txt")
    
    # Issue 3: Check Procfile
    print("\n3. Checking Procfile...")
    if os.path.exists('Procfile'):
        with open('Procfile', 'r') as f:
            procfile_content = f.read().strip()
        
        print(f"Current Procfile: {procfile_content}")
        
        # Check for eventlet (problematic)
        if 'eventlet' in procfile_content:
            print("⚠️  Procfile uses eventlet (may cause issues)")
            issues_found.append("Procfile uses eventlet")
            
            # Fix: Replace with gevent
            new_content = "web: gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
            with open('Procfile', 'w') as f:
                f.write(new_content)
            fixes_applied.append("Updated Procfile to use gevent")
            print("✅ Fixed Procfile to use gevent")
        
        elif 'gevent' in procfile_content:
            print("✅ Procfile uses gevent (good)")
        else:
            print("⚠️  Procfile doesn't specify worker class")
    else:
        print("❌ Procfile not found")
        issues_found.append("Missing Procfile")
        
        # Create Procfile
        with open('Procfile', 'w') as f:
            f.write("web: gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app")
        fixes_applied.append("Created Procfile")
        print("✅ Created Procfile")
    
    # Issue 4: Check app.py for production readiness
    print("\n4. Checking app.py...")
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        # Check for port configuration
        if 'PORT' in app_content and 'environ' in app_content:
            print("✅ PORT environment variable handling found")
        else:
            print("⚠️  PORT environment variable handling not found")
            issues_found.append("Missing PORT configuration")
        
        # Check for SocketIO async mode
        if 'async_mode' in app_content:
            if 'eventlet' in app_content:
                print("⚠️  SocketIO uses eventlet (may cause issues)")
                issues_found.append("SocketIO uses eventlet")
            elif 'gevent' in app_content:
                print("✅ SocketIO uses gevent")
            else:
                print("⚠️  SocketIO async mode not specified")
        
        # Check for production error handling
        if 'try:' in app_content and 'except:' in app_content:
            print("✅ Error handling found")
        else:
            print("⚠️  Limited error handling")
            issues_found.append("Limited error handling")
    else:
        print("❌ app.py not found")
        issues_found.append("Missing app.py")
    
    return issues_found, fixes_applied

def create_alternative_configurations():
    """Create alternative deployment configurations"""
    print("\n🔄 CREATING ALTERNATIVE CONFIGURATIONS")
    print("=" * 50)
    
    alternatives_created = []
    
    # Alternative 1: Sync worker Procfile
    sync_procfile = "web: gunicorn -w 1 --bind 0.0.0.0:$PORT app:app"
    with open('Procfile.sync', 'w') as f:
        f.write(sync_procfile)
    alternatives_created.append('Procfile.sync')
    print("✅ Created Procfile.sync (sync worker)")
    
    # Alternative 2: Thread worker Procfile
    thread_procfile = "web: gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app"
    with open('Procfile.thread', 'w') as f:
        f.write(thread_procfile)
    alternatives_created.append('Procfile.thread')
    print("✅ Created Procfile.thread (thread worker)")
    
    # Alternative 3: Development Procfile
    dev_procfile = "web: python app.py"
    with open('Procfile.dev', 'w') as f:
        f.write(dev_procfile)
    alternatives_created.append('Procfile.dev')
    print("✅ Created Procfile.dev (development)")
    
    # Alternative 4: Minimal requirements.txt
    minimal_requirements = """Flask==2.3.3
Flask-SocketIO==5.3.6
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
twilio==8.10.0
openai==1.3.0
gevent==23.9.1"""
    
    with open('requirements.minimal.txt', 'w') as f:
        f.write(minimal_requirements)
    alternatives_created.append('requirements.minimal.txt')
    print("✅ Created requirements.minimal.txt")
    
    return alternatives_created

def test_deployment_locally():
    """Test different deployment configurations locally"""
    print("\n🧪 TESTING DEPLOYMENT CONFIGURATIONS")
    print("=" * 50)
    
    test_results = {}
    
    # Test configurations
    configs = [
        ("gevent", ["gunicorn", "--worker-class", "gevent", "-w", "1", "--bind", "127.0.0.1:5001", "app:app"]),
        ("sync", ["gunicorn", "-w", "1", "--bind", "127.0.0.1:5002", "app:app"]),
        ("thread", ["gunicorn", "--worker-class", "gthread", "--workers", "1", "--threads", "2", "--bind", "127.0.0.1:5003", "app:app"])
    ]
    
    for config_name, command in configs:
        print(f"\nTesting {config_name} configuration...")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=dict(os.environ, PORT="500" + str(configs.index((config_name, command)) + 1))
            )
            
            time.sleep(3)
            
            if process.poll() is None:
                print(f"✅ {config_name} configuration works")
                test_results[config_name] = True
                
                # Test health endpoint
                port = 5001 + configs.index((config_name, command))
                try:
                    response = requests.get(f'http://127.0.0.1:{port}/health', timeout=3)
                    if response.status_code == 200:
                        print(f"✅ {config_name} health check passed")
                    else:
                        print(f"⚠️  {config_name} health check: {response.status_code}")
                except:
                    print(f"⚠️  {config_name} health check failed")
                
                process.terminate()
                process.wait()
            else:
                stdout, stderr = process.communicate()
                print(f"❌ {config_name} configuration failed")
                print(f"Error: {stderr.decode()[:200]}")
                test_results[config_name] = False
                
        except Exception as e:
            print(f"❌ {config_name} test error: {e}")
            test_results[config_name] = False
    
    return test_results

def generate_deployment_recommendations(issues, fixes, test_results):
    """Generate specific deployment recommendations"""
    print("\n🎯 DEPLOYMENT RECOMMENDATIONS")
    print("=" * 40)
    
    recommendations = []
    
    # Determine best configuration
    if test_results.get('gevent', False):
        recommendations.append("✅ Use gevent worker (main Procfile)")
        deployment_command = "gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app"
    elif test_results.get('sync', False):
        recommendations.append("⚠️  Use sync worker (Procfile.sync)")
        deployment_command = "gunicorn -w 1 --bind 0.0.0.0:$PORT app:app"
    elif test_results.get('thread', False):
        recommendations.append("⚠️  Use thread worker (Procfile.thread)")
        deployment_command = "gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app"
    else:
        recommendations.append("❌ Use development mode (Procfile.dev)")
        deployment_command = "python app.py"
    
    # Add specific recommendations based on issues
    if "eventlet" in str(issues):
        recommendations.append("🔧 Remove eventlet dependencies")
    
    if "Missing PORT configuration" in str(issues):
        recommendations.append("🔧 Add PORT environment variable handling to app.py")
    
    if "Limited error handling" in str(issues):
        recommendations.append("🔧 Add comprehensive error handling")
    
    print("📋 RECOMMENDATIONS:")
    for rec in recommendations:
        print(f"   {rec}")
    
    print(f"\n🚀 RENDER START COMMAND:")
    print(f"   {deployment_command}")
    
    return recommendations, deployment_command

def create_troubleshooting_report():
    """Create comprehensive troubleshooting report"""
    print("\n📊 CREATING TROUBLESHOOTING REPORT")
    print("=" * 50)
    
    # Diagnose issues
    issues, fixes = diagnose_render_issues()
    
    # Create alternatives
    alternatives = create_alternative_configurations()
    
    # Test configurations
    test_results = test_deployment_locally()
    
    # Generate recommendations
    recommendations, deployment_command = generate_deployment_recommendations(issues, fixes, test_results)
    
    # Create report
    report = {
        'timestamp': datetime.now().isoformat(),
        'issues_found': issues,
        'fixes_applied': fixes,
        'alternatives_created': alternatives,
        'test_results': test_results,
        'recommendations': recommendations,
        'deployment_command': deployment_command,
        'ready_for_deployment': len(issues) == 0 or len(fixes) > 0
    }
    
    # Save report
    with open('render_troubleshooting_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Report saved: render_troubleshooting_report.json")
    
    return report

def main():
    """Main troubleshooting function"""
    print("🔧 RENDER DEPLOYMENT TROUBLESHOOTING")
    print("=" * 50)
    
    # Create troubleshooting report
    report = create_troubleshooting_report()
    
    print("\n📋 TROUBLESHOOTING SUMMARY:")
    print("=" * 40)
    
    print(f"Issues found: {len(report['issues_found'])}")
    for issue in report['issues_found']:
        print(f"   ❌ {issue}")
    
    print(f"\nFixes applied: {len(report['fixes_applied'])}")
    for fix in report['fixes_applied']:
        print(f"   ✅ {fix}")
    
    print(f"\nAlternatives created: {len(report['alternatives_created'])}")
    for alt in report['alternatives_created']:
        print(f"   📁 {alt}")
    
    print(f"\nTest results:")
    for config, result in report['test_results'].items():
        status = "✅" if result else "❌"
        print(f"   {status} {config}")
    
    print(f"\n🎯 NEXT STEPS:")
    if report['fixes_applied']:
        print("1. Commit the fixes:")
        print("   git add .")
        print("   git commit -m 'Fix deployment issues'")
        print("   git push")
    
    print("2. Deploy on Render with this command:")
    print(f"   {report['deployment_command']}")
    
    if not any(report['test_results'].values()):
        print("3. If deployment still fails:")
        print("   • Try alternative Procfiles")
        print("   • Check Render build logs")
        print("   • Use requirements.minimal.txt")
    
    print(f"\n🎸 Your Steve Perry AI will rock once deployed! 🎤")

if __name__ == "__main__":
    main()
