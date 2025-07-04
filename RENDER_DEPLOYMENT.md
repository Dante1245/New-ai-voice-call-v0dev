# Steve Perry AI Voice Assistant - Render Deployment Guide

## 🚀 Quick Deployment

### Prerequisites
- GitHub repository with your code
- Render account (free)
- Environment variables ready

### Step 1: Prepare Repository
\`\`\`bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
\`\`\`

### Step 2: Create Render Web Service
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your AI Voice Assistant repo

### Step 3: Configure Service
- **Name**: `steve-perry-ai-voice-assistant`
- **Environment**: Python 3
- **Region**: Oregon (US West)
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --worker-class gevent -w 1 --bind 0.0.0.0:$PORT app:app`
- **Instance Type**: Free

### Step 4: Environment Variables
Add these in Render dashboard:
\`\`\`
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id
SECRET_KEY=your_secret_key
PYTHON_VERSION=3.11.0
\`\`\`

### Step 5: Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- Your app will be at: `https://steve-perry-ai-voice-assistant.onrender.com`

### Step 6: Configure Twilio Webhooks
In Twilio Console → Phone Numbers → Your Number:
- **Voice URL**: `https://your-app.onrender.com/answer`
- **Status Callback**: `https://your-app.onrender.com/call_status`
- **Recording Callback**: `https://your-app.onrender.com/recording_complete`

## 🔧 Troubleshooting

### If Deployment Fails

#### Option 1: Use Sync Worker
Replace start command with:
\`\`\`
gunicorn -w 1 --bind 0.0.0.0:$PORT app:app
\`\`\`

#### Option 2: Use Thread Worker
Replace start command with:
\`\`\`
gunicorn --worker-class gthread --workers 1 --threads 2 --bind 0.0.0.0:$PORT app:app
\`\`\`

#### Option 3: Development Mode
Replace start command with:
\`\`\`
python app.py
\`\`\`

### Common Issues

1. **Build Fails**: Check Python version (use 3.11.0)
2. **App Won't Start**: Check environment variables
3. **Gevent Issues**: Use sync worker fallback
4. **Import Errors**: Check requirements.txt

### Testing Deployment
After deployment, test these URLs:
- Health Check: `https://your-app.onrender.com/health`
- Dashboard: `https://your-app.onrender.com`

## 📞 Making Test Calls
1. Call your Twilio phone number
2. You should hear Steve Perry's voice
3. Have a conversation with the AI
4. Check the dashboard for real-time updates

## 🎸 You're Ready to Rock!
Your Steve Perry AI Voice Assistant is now live and ready to take calls from around the world!
