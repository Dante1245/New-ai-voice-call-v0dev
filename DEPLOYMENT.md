# 🚀 AI Voice Assistant - Production Deployment Guide

## Quick Start Deployment

### Option 1: Automated Deployment Script (Recommended)
\`\`\`bash
python scripts/deploy_to_render.py
\`\`\`

### Option 2: Manual Deployment

## 📋 Pre-Deployment Checklist

1. **Environment Variables Ready**
   \`\`\`bash
   # Check your .env file has all required variables
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_phone_number
   OPENAI_API_KEY=your_openai_key
   ELEVENLABS_API_KEY=your_elevenlabs_key
   ELEVENLABS_VOICE_ID=your_voice_id
   SECRET_KEY=your_production_secret_key
   \`\`\`

2. **Code Repository**
   \`\`\`bash
   git init
   git add .
   git commit -m "Production-ready AI Voice Assistant"
   git remote add origin https://github.com/yourusername/steve-perry-ai.git
   git push -u origin main
   \`\`\`

3. **Dependencies Verified**
   \`\`\`bash
   pip install -r requirements.txt
   python scripts/production_test.py
   \`\`\`

## 🌐 Deploy to Render (Recommended)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your repository

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your repository
3. Configure settings:
   - **Name**: `steve-perry-ai-voice-assistant`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: `Free` (or `Starter` for better performance)

### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:

| Variable | Value |
|----------|-------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio Phone Number |
| `OPENAI_API_KEY` | Your OpenAI API Key |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API Key |
| `ELEVENLABS_VOICE_ID` | Your Steve Perry Voice ID |
| `SECRET_KEY` | Generate strong random key |

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## 🔧 Deploy to Heroku

### Step 1: Install Heroku CLI
\`\`\`bash
# Install Heroku CLI
# macOS: brew install heroku/brew/heroku
# Windows: Download from heroku.com
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

heroku login
\`\`\`

### Step 2: Create Heroku App
\`\`\`bash
heroku create steve-perry-ai-voice-assistant
heroku buildpacks:set heroku/python
\`\`\`

### Step 3: Set Environment Variables
\`\`\`bash
heroku config:set TWILIO_ACCOUNT_SID=your_account_sid
heroku config:set TWILIO_AUTH_TOKEN=your_auth_token
heroku config:set TWILIO_PHONE_NUMBER=your_phone_number
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set ELEVENLABS_API_KEY=your_elevenlabs_key
heroku config:set ELEVENLABS_VOICE_ID=your_voice_id
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
\`\`\`

### Step 4: Deploy
\`\`\`bash
git push heroku main
heroku open
\`\`\`

## 🔗 Configure Twilio Webhooks

After deployment, configure your Twilio phone number:

1. **Go to Twilio Console**: https://console.twilio.com
2. **Navigate to**: Phone Numbers → Manage → Active Numbers
3. **Select your phone number** and configure:

| Setting | Value |
|---------|-------|
| **Voice URL** | `https://your-app-url.com/answer` |
| **Voice Method** | `POST` |
| **Status Callback URL** | `https://your-app-url.com/call_status` |
| **Status Callback Method** | `POST` |
| **Recording Status Callback** | `https://your-app-url.com/recording_complete` |

4. **Save Configuration**

## ✅ Verify Deployment

### Automated Verification
\`\`\`bash
python scripts/verify_deployment.py https://your-app-url.com
\`\`\`

### Manual Verification
1. **Health Check**: Visit `https://your-app-url.com/health`
   \`\`\`json
   {
     "status": "healthy",
     "services": {
       "twilio": true,
       "openai": true,
       "elevenlabs": true
     }
   }
   \`\`\`

2. **Dashboard**: Visit `https://your-app-url.com`
   - Should show Steve Perry AI Voice Assistant interface

3. **Test Call**: 
   - Enter your phone number
   - Click "Start Call"
   - Answer and talk to Steve Perry!

## 📊 Monitoring & Maintenance

### Health Monitoring
- **Health Endpoint**: `https://your-app-url.com/health`
- **Uptime Monitoring**: Set up external monitoring (UptimeRobot, Pingdom)
- **Log Monitoring**: Check platform logs regularly

### Performance Optimization
\`\`\`bash
# For Render
# Upgrade to Starter plan for better performance
# Enable auto-scaling if needed

# For Heroku
heroku ps:scale web=1
heroku logs --tail
\`\`\`

### Security Best Practices
1. **Rotate API Keys** monthly
2. **Monitor Usage** for unusual activity
3. **Update Dependencies** regularly
4. **Use HTTPS Only** for all webhooks

## 🚨 Troubleshooting

### Common Issues

**1. Build Fails**
\`\`\`bash
# Check build logs
# Ensure requirements.txt is correct
# Verify Python version compatibility
\`\`\`

**2. App Crashes on Startup**
\`\`\`bash
# Check environment variables are set
# Verify all API keys are valid
# Check application logs
\`\`\`

**3. Calls Don't Work**
\`\`\`bash
# Verify Twilio webhooks are configured
# Check webhook URLs use HTTPS
# Ensure phone number format is correct
\`\`\`

**4. Voice Synthesis Fails**
\`\`\`bash
# Verify ElevenLabs API key and voice ID
# Check API rate limits
# Test with shorter text
\`\`\`

### Debug Commands
\`\`\`bash
# Check deployment status
curl https://your-app-url.com/health

# Test API endpoints
curl https://your-app-url.com/get_memory

# View logs (Render)
# Check Render dashboard logs

# View logs (Heroku)
heroku logs --tail
\`\`\`

## 🎯 Production Checklist

- [ ] ✅ Environment variables configured
- [ ] ✅ Repository pushed to GitHub
- [ ] ✅ Web service created and deployed
- [ ] ✅ Health endpoint returns "healthy"
- [ ] ✅ Dashboard loads correctly
- [ ] ✅ Twilio webhooks configured
- [ ] ✅ Test call successful
- [ ] ✅ Voice synthesis working
- [ ] ✅ Conversation memory functioning
- [ ] ✅ Error handling tested
- [ ] ✅ Monitoring set up

## 🎉 Success!

Your Steve Perry AI Voice Assistant is now live in production!

**🌐 Your App**: `https://your-app-name.onrender.com`
**🔍 Health Check**: `https://your-app-name.onrender.com/health`
**📱 Dashboard**: Ready for calls!

**🎤 Time to rock and roll with AI!** 🎸✨

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs
3. Verify all environment variables
4. Test individual components

**Your AI Voice Assistant is production-ready!** 🚀
\`\`\`

```python file="scripts/post_deployment_setup.py"
#!/usr/bin/env python3
"""
Post-deployment setup and configuration
"""

import os
import sys
import requests
import json
from datetime import datetime

def setup_twilio_webhooks(app_url, account_sid, auth_token):
    """Configure Twilio webhooks automatically"""
    print("🔗 Configuring Twilio webhooks...")
    
    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        
        # Get phone numbers
        phone_numbers = client.incoming_phone_numbers.list()
        
        if not phone_numbers:
            print("❌ No Twilio phone numbers found")
            return False
        
        # Configure first phone number
        phone_number = phone_numbers[0]
        
        # Update webhook URLs
        phone_number.update(
            voice_url=f"{app_url}/answer",
            voice_method='POST',
            status_callback=f"{app_url}/call_status",
            status_callback_method='POST'
        )
        
        print(f"✅ Configured webhooks for {phone_number.phone_number}")
        print(f"   Voice URL: {app_url}/answer")
        print(f"   Status Callback: {app_url}/call_status")
        
        return True
        
    except Exception as e:
        print(f"❌ Webhook configuration failed: {e}")
        return False

def test_production_endpoints(app_url):
    """Test all production endpoints"""
    print("🧪 Testing production endpoints...")
    
    endpoints = [
        ('/health', 'Health Check'),
        ('/', 'Dashboard'),
        ('/get_memory', 'Memory System')
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{app_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results[name] = True
                
                if endpoint == '/health':
                    data = response.json()
                    services = data.get('services', {})
                    for service, status in services.items():
                        icon = "✅" if status else "⚠️"
                        print(f"   {icon} {service}: {'Ready' if status else 'Not configured'}")
            else:
                print(f"❌ {name}: Failed ({response.status_code})")
                results[name] = False
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = False
    
    return results

def create_monitoring_script(app_url):
    """Create monitoring script for the deployed app"""
    monitoring_script = f'''#!/usr/bin/env python3
"""
Production monitoring script for {app_url}
"""

import requests
import time
import json
from datetime import datetime

def check_health():
    """Check application health"""
    try:
        response = requests.get("{app_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('status') == 'healthy'
        return False
    except:
        return False

def monitor_app():
    """Monitor application continuously"""
    print("🔍 Monitoring {app_url}")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            if check_health():
                print(f"✅ {{datetime.now().strftime('%H:%M:%S')}} - App is healthy")
            else:
                print(f"❌ {{datetime.now().strftime('%H:%M:%S')}} - App is unhealthy")
            
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            print("\\n👋 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ {{datetime.now().strftime('%H:%M:%S')}} - Monitor error: {{e}}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_app()
'''
    
    with open('monitor_production.py', 'w') as f:
        f.write(monitoring_script)
    
    print("✅ Created monitoring script: monitor_production.py")
    print("   Run with: python monitor_production.py")

def setup_environment_backup():
    """Create backup of environment configuration"""
    print("💾 Creating environment backup...")
    
    env_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER',
        'OPENAI_API_KEY',
        'ELEVENLABS_API_KEY',
        'ELEVENLABS_VOICE_ID'
    ]
    
    backup_config = {
        'timestamp': datetime.now().isoformat(),
        'environment_variables': {}
    }
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Store only first/last few characters for security
            if len(value) > 10:
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
            else:
                masked_value = '*' * len(value)
            backup_config['environment_variables'][var] = {
                'configured': True,
                'masked_value': masked_value
            }
        else:
            backup_config['environment_variables'][var] = {
                'configured': False,
                'masked_value': None
            }
    
    with open('production_config_backup.json', 'w') as f:
        json.dump(backup_config, f, indent=2)
    
    print("✅ Environment backup saved: production_config_backup.json")

def main():
    """Main post-deployment setup"""
    print("🚀 POST-DEPLOYMENT SETUP")
    print("=" * 50)
    
    # Get app URL
    if len(sys.argv) > 1:
        app_url = sys.argv[1].rstrip('/')
    else:
        app_url = input("Enter your deployed app URL: ").strip().rstrip('/')
    
    if not app_url.startswith('http'):
        app_url = 'https://' + app_url
    
    print(f"🎯 Setting up: {app_url}")
    
    # Test endpoints
    test_results = test_production_endpoints(app_url)
    
    # Setup Twilio webhooks if credentials available
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    if account_sid and auth_token:
        setup_twilio_webhooks(app_url, account_sid, auth_token)
    else:
        print("⚠️  Twilio credentials not found - configure webhooks manually")
        print(f"   Voice URL: {app_url}/answer")
        print(f"   Status Callback: {app_url}/call_status")
    
    # Create monitoring tools
    create_monitoring_script(app_url)
    setup_environment_backup()
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 POST-DEPLOYMENT SETUP COMPLETE!")
    print("=" * 50)
    print(f"🌐 App URL: {app_url}")
    print(f"🔍 Health Check: {app_url}/health")
    print(f"📱 Dashboard: {app_url}")
    
    successful_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    print(f"✅ Tests Passed: {successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("\n🎤 Your Steve Perry AI Voice Assistant is LIVE and ready to rock! 🎸")
        print("\n📞 Test it now:")
        print("1. Open the dashboard")
        print("2. Enter your phone number")
        print("3. Click 'Start Call'")
        print("4. Talk to Steve Perry!")
    else:
        print("\n⚠️  Some tests failed - check the issues above")
    
    print(f"\n📊 Monitor your app: python monitor_production.py")

if __name__ == "__main__":
    main()
