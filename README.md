# AI Voice Assistant - Steve Perry Edition

A full-stack AI-powered voice assistant web application that enables real-time phone conversations with an AI version of Steve Perry using Twilio, ElevenLabs, and OpenAI.

## Features

- **Real-time Phone Calls**: Make and receive calls using Twilio
- **AI Voice Synthesis**: ElevenLabs integration for Steve Perry voice cloning
- **Smart Reply Generation**: OpenAI GPT-powered intelligent responses
- **Live Transcription**: Real-time speech-to-text conversion
- **Memory Learning**: Persistent conversation memory and learning
- **Admin Dashboard**: Real-time monitoring and control interface
- **WebSocket Integration**: Live updates and real-time communication

## Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

\`\`\`bash
cp .env.example .env
\`\`\`

Required API keys:
- **Twilio**: Account SID, Auth Token, and Phone Number
- **OpenAI**: API Key for GPT integration
- **ElevenLabs**: API Key and Voice ID for Steve Perry voice

### 2. Local Development

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
\`\`\`

The application will be available at `http://localhost:5000`

### 3. Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 app:app`
4. Add all environment variables from `.env.example`
5. Deploy!

### 4. Twilio Webhook Configuration

In your Twilio Console:
1. Go to Phone Numbers → Manage → Active Numbers
2. Click on your Twilio phone number
3. Set the webhook URL to: `https://your-render-app.onrender.com/answer`
4. Set HTTP method to POST

## Usage

1. **Start a Call**: Enter a phone number and click "Start Call"
2. **Monitor Live**: Watch real-time transcription and conversation
3. **Smart Replies**: Use AI-generated response suggestions
4. **Custom Replies**: Send custom responses during calls
5. **Memory Management**: View and manage conversation history

## API Endpoints

- `GET /` - Dashboard interface
- `POST /start_call` - Initiate a phone call
- `POST /answer` - Handle incoming calls (Twilio webhook)
- `POST /process_speech` - Process user speech (Twilio webhook)
- `POST /send_reply` - Send reply during active call
- `POST /end_call` - End current call
- `GET /get_memory` - Retrieve conversation memory

## Architecture

\`\`\`
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Web Dashboard │    │ Flask Server │    │ Twilio Voice    │
│   (Frontend)    │◄──►│ (Backend)    │◄──►│ (Phone Calls)   │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   AI Services    │
                    │ • OpenAI GPT     │
                    │ • ElevenLabs TTS │
                    │ • Memory System  │
                    └──────────────────┘
\`\`\`

## Technologies Used

- **Backend**: Flask, Flask-SocketIO
- **Voice**: Twilio Voice API
- **AI**: OpenAI GPT-4, ElevenLabs Text-to-Speech
- **Real-time**: WebSockets (Socket.IO)
- **Deployment**: Render, Gunicorn
- **Storage**: JSON file-based memory system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details
