#!/usr/bin/env python3
"""
AI Voice Assistant - Production Ready
Professional Steve Perry AI Voice Assistant with Twilio, OpenAI, and ElevenLabs
"""

import sys
import os
import logging
import json
import time
import threading
import traceback
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import required modules with comprehensive error handling
try:
    from flask import Flask, request, render_template, jsonify, send_from_directory
    from flask_socketio import SocketIO, emit
    from werkzeug.utils import secure_filename
    import requests
    logger.info("✅ Core dependencies loaded successfully")
except ImportError as e:
    logger.error(f"❌ Critical dependency missing: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

# Optional dependencies with graceful fallbacks
TWILIO_AVAILABLE = False
OPENAI_AVAILABLE = False
DOTENV_AVAILABLE = False

try:
    from twilio.rest import Client
    from twilio.twiml import VoiceResponse
    TWILIO_AVAILABLE = True
    logger.info("✅ Twilio SDK loaded")
except ImportError:
    logger.warning("⚠️  Twilio SDK not available")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    logger.info("✅ OpenAI SDK loaded")
except ImportError:
    logger.warning("⚠️  OpenAI SDK not available")

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
    logger.info("✅ Environment variables loaded")
except ImportError:
    logger.warning("⚠️  python-dotenv not available")

class AIVoiceAssistant:
    """Professional AI Voice Assistant Application"""
    
    def __init__(self):
        """Initialize the application with all components"""
        self.app = None
        self.socketio = None
        self.twilio_client = None
        self.openai_client = None
        self.call_state = {
            'status': 'Idle',
            'call_sid': None,
            'transcription': '',
            'conversation_history': [],
            'smart_replies': [],
            'recording_sid': None,
            'is_recording': False,
            'start_time': None,
            'duration': 0
        }
        self.memory_cache = {}
        self.config = self._load_configuration()
        
        # Initialize components
        self._initialize_flask()
        self._initialize_clients()
        self._setup_routes()
        self._setup_websockets()
        
        logger.info("🚀 AI Voice Assistant initialized successfully")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load and validate configuration"""
        config = {
            'twilio': {
                'account_sid': os.environ.get('TWILIO_ACCOUNT_SID'),
                'auth_token': os.environ.get('TWILIO_AUTH_TOKEN'),
                'phone_number': os.environ.get('TWILIO_PHONE_NUMBER')
            },
            'openai': {
                'api_key': os.environ.get('OPENAI_API_KEY')
            },
            'elevenlabs': {
                'api_key': os.environ.get('ELEVENLABS_API_KEY'),
                'voice_id': os.environ.get('ELEVENLABS_VOICE_ID')
            },
            'flask': {
                'secret_key': os.environ.get('SECRET_KEY', 'production-secret-key-change-me'),
                'port': int(os.environ.get('PORT', 5000)),
                'debug': os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
            },
            'app': {
                'max_conversation_history': 100,
                'max_audio_duration': 1800,  # 30 minutes
                'request_timeout': 30,
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.5
                }
            }
        }
        
        # Validate critical configuration
        missing_config = []
        if not config['twilio']['account_sid']:
            missing_config.append('TWILIO_ACCOUNT_SID')
        if not config['twilio']['auth_token']:
            missing_config.append('TWILIO_AUTH_TOKEN')
        if not config['openai']['api_key']:
            missing_config.append('OPENAI_API_KEY')
        
        if missing_config:
            logger.warning(f"⚠️  Missing configuration: {', '.join(missing_config)}")
        
        return config
    
    def _initialize_flask(self):
        """Initialize Flask application with proper configuration"""
        try:
            self.app = Flask(__name__)
            self.app.config['SECRET_KEY'] = self.config['flask']['secret_key']
            self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
            
            # Initialize SocketIO with production settings
            self.socketio = SocketIO(
                self.app,
                cors_allowed_origins="*",
                async_mode='eventlet',
                logger=False,
                engineio_logger=False,
                ping_timeout=60,
                ping_interval=25
            )
            
            logger.info("✅ Flask application initialized")
            
        except Exception as e:
            logger.error(f"❌ Flask initialization failed: {e}")
            raise
    
    def _initialize_clients(self):
        """Initialize external API clients with error handling"""
        # Initialize Twilio client
        if TWILIO_AVAILABLE and self.config['twilio']['account_sid']:
            try:
                self.twilio_client = Client(
                    self.config['twilio']['account_sid'],
                    self.config['twilio']['auth_token']
                )
                
                # Test connection
                account = self.twilio_client.api.accounts(
                    self.config['twilio']['account_sid']
                ).fetch()
                logger.info(f"✅ Twilio client initialized - Account: {account.status}")
                
            except Exception as e:
                logger.error(f"❌ Twilio initialization failed: {e}")
                self.twilio_client = None
        
        # Initialize OpenAI client
        if OPENAI_AVAILABLE and self.config['openai']['api_key']:
            try:
                self.openai_client = OpenAI(
                    api_key=self.config['openai']['api_key'],
                    timeout=self.config['app']['request_timeout']
                )
                
                # Test connection
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                logger.info("✅ OpenAI client initialized and tested")
                
            except Exception as e:
                logger.error(f"❌ OpenAI initialization failed: {e}")
                self.openai_client = None
    
    def _setup_routes(self):
        """Setup all Flask routes with comprehensive error handling"""
        
        @self.app.route('/')
        def dashboard():
            """Serve the main dashboard"""
            try:
                return render_template('dashboard.html')
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
                return jsonify({'error': 'Dashboard unavailable'}), 500
        
        @self.app.route('/health')
        def health_check():
            """Comprehensive health check endpoint"""
            try:
                health_status = {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'version': '2.0.0',
                    'services': {
                        'twilio': self.twilio_client is not None,
                        'openai': self.openai_client is not None,
                        'elevenlabs': bool(self.config['elevenlabs']['api_key'])
                    },
                    'call_state': self.call_state['status'],
                    'memory_entries': len(self.load_memory().get('conversations', []))
                }
                return jsonify(health_status)
            except Exception as e:
                logger.error(f"Health check error: {e}")
                return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
        
        @self.app.route('/start_call', methods=['POST'])
        def start_call():
            """Start a new call with comprehensive validation"""
            try:
                if not self.twilio_client:
                    return jsonify({'error': 'Twilio service unavailable'}), 503
                
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'Invalid request data'}), 400
                
                phone_number = self._validate_phone_number(data.get('phone_number'))
                if not phone_number:
                    return jsonify({'error': 'Invalid phone number format'}), 400
                
                # Check if call is already active
                if self.call_state['status'] != 'Idle':
                    return jsonify({'error': 'Call already in progress'}), 409
                
                # Create webhook URL
                base_url = request.url_root.rstrip('/')
                webhook_url = f"{base_url}/answer"
                
                # Initiate call
                call = self.twilio_client.calls.create(
                    to=phone_number,
                    from_=self.config['twilio']['phone_number'],
                    url=webhook_url,
                    method='POST',
                    timeout=30,
                    record=True
                )
                
                # Update call state
                self.call_state.update({
                    'status': 'Ringing',
                    'call_sid': call.sid,
                    'start_time': datetime.now(),
                    'transcription': '',
                    'conversation_history': [],
                    'smart_replies': []
                })
                
                # Emit status update
                self.socketio.emit('call_status_update', self.call_state)
                
                logger.info(f"Call started: {call.sid} to {phone_number}")
                return jsonify({
                    'success': True,
                    'call_sid': call.sid,
                    'status': 'ringing'
                })
                
            except Exception as e:
                logger.error(f"Start call error: {e}")
                return jsonify({'error': f'Call failed: {str(e)}'}), 500
        
        @self.app.route('/answer', methods=['POST'])
        def answer_call():
            """Handle incoming call with TwiML response"""
            try:
                response = VoiceResponse()
                call_sid = request.form.get('CallSid')
                
                # Update call state
                self.call_state.update({
                    'status': 'In Progress',
                    'call_sid': call_sid,
                    'is_recording': True
                })
                
                # Start recording
                response.record(
                    action='/recording_complete',
                    method='POST',
                    max_length=self.config['app']['max_audio_duration'],
                    play_beep=False,
                    transcribe=True,
                    transcribe_callback='/transcription_complete'
                )
                
                # Generate greeting
                greeting = self._generate_greeting()
                
                # Try ElevenLabs TTS, fallback to Twilio
                audio_url = self._text_to_speech(greeting)
                if audio_url:
                    response.play(audio_url)
                else:
                    response.say(greeting, voice='man', rate='medium')
                
                # Listen for user speech
                gather = response.gather(
                    input='speech',
                    action='/process_speech',
                    method='POST',
                    timeout=10,
                    speech_timeout='auto'
                )
                
                # Add conversation to history
                self._add_to_conversation_history('assistant', greeting)
                
                # Emit updates
                self.socketio.emit('call_status_update', self.call_state)
                
                logger.info(f"Call answered: {call_sid}")
                return str(response)
                
            except Exception as e:
                logger.error(f"Answer call error: {e}")
                response = VoiceResponse()
                response.say("Sorry, there was a technical issue. Please try again later.")
                response.hangup()
                return str(response)
        
        @self.app.route('/process_speech', methods=['POST'])
        def process_speech():
            """Process user speech input"""
            try:
                user_speech = request.form.get('SpeechResult', '').strip()
                confidence = float(request.form.get('Confidence', 0))
                
                if user_speech and confidence > 0.5:
                    # Add to conversation history
                    self._add_to_conversation_history('user', user_speech)
                    
                    # Update transcription
                    self.call_state['transcription'] = user_speech
                    
                    # Generate smart replies
                    smart_replies = self._generate_smart_replies(user_speech)
                    self.call_state['smart_replies'] = smart_replies
                    
                    # Emit updates
                    self.socketio.emit('transcription_update', {
                        'transcription': user_speech,
                        'confidence': confidence,
                        'smart_replies': smart_replies
                    })
                    self.socketio.emit('call_status_update', self.call_state)
                
                # Continue listening
                response = VoiceResponse()
                response.gather(
                    input='speech',
                    action='/process_speech',
                    method='POST',
                    timeout=10,
                    speech_timeout='auto'
                )
                
                return str(response)
                
            except Exception as e:
                logger.error(f"Process speech error: {e}")
                response = VoiceResponse()
                response.gather(input='speech', action='/process_speech', method='POST')
                return str(response)
        
        @self.app.route('/send_reply', methods=['POST'])
        def send_reply():
            """Send AI-generated reply during call"""
            try:
                if not self.twilio_client:
                    return jsonify({'error': 'Twilio service unavailable'}), 503
                
                data = request.get_json()
                if not data or not data.get('reply'):
                    return jsonify({'error': 'Reply text required'}), 400
                
                reply_text = data['reply'].strip()
                if len(reply_text) > 1000:
                    return jsonify({'error': 'Reply too long (max 1000 characters)'}), 400
                
                if not self.call_state['call_sid']:
                    return jsonify({'error': 'No active call'}), 400
                
                # Generate TwiML response
                response = VoiceResponse()
                
                # Try ElevenLabs TTS
                audio_url = self._text_to_speech(reply_text)
                if audio_url:
                    response.play(audio_url)
                else:
                    response.say(reply_text, voice='man', rate='medium')
                
                # Continue listening
                response.gather(
                    input='speech',
                    action='/process_speech',
                    method='POST',
                    timeout=10
                )
                
                # Update call with new TwiML
                try:
                    self.twilio_client.calls(self.call_state['call_sid']).update(
                        twiml=str(response)
                    )
                except Exception as update_error:
                    logger.warning(f"TwiML update failed: {update_error}")
                
                # Add to conversation history
                self._add_to_conversation_history('assistant', reply_text)
                
                # Save to memory
                self._save_conversation_to_memory()
                
                # Emit updates
                self.socketio.emit('call_status_update', self.call_state)
                
                logger.info(f"Reply sent: {reply_text[:50]}...")
                return jsonify({'success': True})
                
            except Exception as e:
                logger.error(f"Send reply error: {e}")
                return jsonify({'error': f'Reply failed: {str(e)}'}), 500
        
        @self.app.route('/end_call', methods=['POST'])
        def end_call():
            """End the current call gracefully"""
            try:
                if self.call_state['call_sid'] and self.twilio_client:
                    try:
                        self.twilio_client.calls(self.call_state['call_sid']).update(
                            status='completed'
                        )
                        logger.info(f"Call ended: {self.call_state['call_sid']}")
                    except Exception as e:
                        logger.warning(f"Call termination warning: {e}")
                
                # Calculate duration
                if self.call_state['start_time']:
                    duration = (datetime.now() - self.call_state['start_time']).total_seconds()
                    self.call_state['duration'] = duration
                
                # Save final conversation to memory
                self._save_conversation_to_memory()
                
                # Reset call state
                self.call_state.update({
                    'status': 'Idle',
                    'call_sid': None,
                    'transcription': '',
                    'smart_replies': [],
                    'recording_sid': None,
                    'is_recording': False,
                    'start_time': None
                })
                
                # Emit updates
                self.socketio.emit('call_status_update', self.call_state)
                
                return jsonify({'success': True})
                
            except Exception as e:
                logger.error(f"End call error: {e}")
                return jsonify({'error': f'End call failed: {str(e)}'}), 500
        
        @self.app.route('/get_memory')
        def get_memory():
            """Retrieve conversation memory"""
            try:
                memory = self.load_memory()
                return jsonify(memory)
            except Exception as e:
                logger.error(f"Get memory error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/clear_memory', methods=['POST'])
        def clear_memory():
            """Clear conversation memory"""
            try:
                success = self.save_memory({
                    'conversations': [],
                    'user_preferences': self._get_default_preferences(),
                    'recordings': []
                })
                
                if success:
                    self.memory_cache = {}
                    logger.info("Memory cleared successfully")
                
                return jsonify({'success': success})
            except Exception as e:
                logger.error(f"Clear memory error: {e}")
                return jsonify({'error': str(e)}), 500
        
        # Recording endpoints
        @self.app.route('/recording_complete', methods=['POST'])
        def recording_complete():
            """Handle recording completion webhook"""
            try:
                recording_sid = request.form.get('RecordingSid')
                recording_url = request.form.get('RecordingUrl')
                duration = request.form.get('RecordingDuration')
                
                if recording_sid:
                    self.call_state['recording_sid'] = recording_sid
                    
                    # Save recording info to memory
                    memory = self.load_memory()
                    memory['recordings'].append({
                        'sid': recording_sid,
                        'url': recording_url,
                        'duration': duration,
                        'timestamp': datetime.now().isoformat(),
                        'call_sid': self.call_state['call_sid']
                    })
                    self.save_memory(memory)
                    
                    self.socketio.emit('recording_complete', {
                        'recording_sid': recording_sid,
                        'duration': duration
                    })
                    
                    logger.info(f"Recording completed: {recording_sid}")
                
                return '', 200
            except Exception as e:
                logger.error(f"Recording complete error: {e}")
                return '', 500
        
        @self.app.route('/transcription_complete', methods=['POST'])
        def transcription_complete():
            """Handle transcription completion webhook"""
            try:
                transcription_text = request.form.get('TranscriptionText', '')
                recording_sid = request.form.get('RecordingSid')
                
                if transcription_text and recording_sid:
                    # Update memory with transcription
                    memory = self.load_memory()
                    for recording in memory.get('recordings', []):
                        if recording.get('sid') == recording_sid:
                            recording['transcription'] = transcription_text
                            break
                    
                    self.save_memory(memory)
                    
                    self.socketio.emit('transcription_complete', {
                        'recording_sid': recording_sid,
                        'transcription': transcription_text
                    })
                    
                    logger.info(f"Transcription completed for: {recording_sid}")
                
                return '', 200
            except Exception as e:
                logger.error(f"Transcription complete error: {e}")
                return '', 500
        
        # Static file serving
        @self.app.route('/static/<path:filename>')
        def serve_static(filename):
            """Serve static files securely"""
            try:
                return send_from_directory('static', filename)
            except Exception as e:
                logger.error(f"Static file error: {e}")
                return jsonify({'error': 'File not found'}), 404
        
        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Endpoint not found'}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.errorhandler(413)
        def too_large(error):
            return jsonify({'error': 'File too large'}), 413
    
    def _setup_websockets(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            try:
                emit('call_status_update', self.call_state)
                logger.info("Client connected")
            except Exception as e:
                logger.error(f"WebSocket connect error: {e}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            try:
                logger.info("Client disconnected")
            except Exception as e:
                logger.error(f"WebSocket disconnect error: {e}")
        
        @self.socketio.on_error_default
        def default_error_handler(e):
            logger.error(f"WebSocket error: {e}")
    
    def _validate_phone_number(self, phone_number: str) -> Optional[str]:
        """Validate and format phone number"""
        if not phone_number:
            return None
        
        # Remove all non-digit characters except +
        cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        
        # Add + if not present
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        
        # Basic validation (10-15 digits after +)
        digits = cleaned[1:]
        if len(digits) >= 10 and len(digits) <= 15 and digits.isdigit():
            return cleaned
        
        return None
    
    def _generate_greeting(self) -> str:
        """Generate personalized greeting"""
        greetings = [
            "Hey there! This is Steve Perry. How are you doing today?",
            "Hello! Steve Perry here from Journey. What's on your mind?",
            "Hi there! It's Steve Perry. Great to hear from you!",
            "Hey! This is Steve Perry. How can I brighten your day?"
        ]
        
        # Use memory to personalize if available
        memory = self.load_memory()
        user_prefs = memory.get('user_preferences', {})
        preferred_greeting = user_prefs.get('preferred_greeting')
        
        if preferred_greeting:
            return preferred_greeting
        
        import random
        return random.choice(greetings)
    
    def _text_to_speech(self, text: str) -> Optional[str]:
        """Convert text to speech using ElevenLabs"""
        try:
            if not text or len(text) > 1000:
                return None
            
            api_key = self.config['elevenlabs']['api_key']
            voice_id = self.config['elevenlabs']['voice_id']
            
            if not api_key or not voice_id:
                logger.warning("ElevenLabs credentials not configured")
                return None
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": self.config['app']['voice_settings']
            }
            
            response = requests.post(
                url, 
                json=data, 
                headers=headers, 
                timeout=self.config['app']['request_timeout']
            )
            
            if response.status_code == 200:
                # Create audio directory
                os.makedirs('static/audio', exist_ok=True)
                
                # Generate unique filename
                timestamp = int(time.time())
                audio_filename = f"static/audio/response_{timestamp}_{uuid.uuid4().hex[:8]}.mp3"
                
                with open(audio_filename, 'wb') as f:
                    f.write(response.content)
                
                # Return URL for Twilio
                base_url = request.url_root.rstrip('/') if request else 'http://localhost:5000'
                return f"{base_url}/{audio_filename}"
            else:
                logger.warning(f"ElevenLabs API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return None
    
    def _generate_smart_replies(self, user_input: str) -> List[str]:
        """Generate intelligent reply suggestions"""
        fallback_replies = [
            "That's really something! Tell me more about that.",
            "You know, that reminds me of a song we used to play.",
            "I hear you, friend. Music has taught me that every story has its rhythm.",
            "That's beautiful, man. Life's like a melody, isn't it?",
            "Hey, that's really interesting! What else is on your mind?"
        ]
        
        if not self.openai_client or not user_input:
            return fallback_replies[:3]
        
        try:
            # Build context from conversation history
            context = self._build_conversation_context()
            
            prompt = f"""You are Steve Perry, the legendary lead singer of Journey. 
            You're having a warm, conversational phone call. The user just said: "{user_input}"
            
            Based on this context: {context}
            
            Generate 3 different warm, conversational responses that Steve Perry would give.
            Keep each response under 30 words and occasionally reference music or Journey.
            Be authentic to Steve Perry's warm, caring personality.
            
            Format as numbered responses:"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Steve Perry from Journey. Be warm, conversational, and authentic."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
                timeout=10
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse numbered responses
            suggestions = []
            for line in content.split('\n'):
                line = line.strip()
                if line and any(char.isdigit() for char in line[:3]):
                    clean_line = line.lstrip('123456789. ').strip()
                    if clean_line and len(clean_line) > 5:
                        suggestions.append(clean_line[:150])
            
            # Ensure we have exactly 3 suggestions
            while len(suggestions) < 3:
                suggestions.extend(fallback_replies)
            
            return suggestions[:3]
            
        except Exception as e:
            logger.error(f"Smart replies error: {e}")
            return fallback_replies[:3]
    
    def _build_conversation_context(self) -> str:
        """Build conversation context for AI responses"""
        history = self.call_state.get('conversation_history', [])
        if not history:
            return "This is the start of the conversation."
        
        # Get last few exchanges
        recent_history = history[-6:]  # Last 3 exchanges
        context_parts = []
        
        for entry in recent_history:
            speaker = "User" if entry['speaker'] == 'user' else "Steve"
            context_parts.append(f"{speaker}: {entry['message']}")
        
        return " | ".join(context_parts)
    
    def _add_to_conversation_history(self, speaker: str, message: str):
        """Add message to conversation history"""
        entry = {
            'speaker': speaker,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        self.call_state['conversation_history'].append(entry)
        
        # Limit history size
        max_history = self.config['app']['max_conversation_history']
        if len(self.call_state['conversation_history']) > max_history:
            self.call_state['conversation_history'] = self.call_state['conversation_history'][-max_history:]
    
    def _save_conversation_to_memory(self):
        """Save conversation to persistent memory"""
        try:
            if not self.call_state['conversation_history']:
                return
            
            memory = self.load_memory()
            
            # Create conversation summary
            conversation_summary = {
                'call_sid': self.call_state['call_sid'],
                'timestamp': datetime.now().isoformat(),
                'duration': self.call_state.get('duration', 0),
                'messages': self.call_state['conversation_history'].copy(),
                'summary': self._generate_conversation_summary()
            }
            
            memory['conversations'].append(conversation_summary)
            
            # Keep only recent conversations
            memory['conversations'] = memory['conversations'][-50:]
            
            self.save_memory(memory)
            
        except Exception as e:
            logger.error(f"Save conversation error: {e}")
    
    def _generate_conversation_summary(self) -> str:
        """Generate a summary of the conversation"""
        history = self.call_state.get('conversation_history', [])
        if not history:
            return "No conversation content"
        
        # Simple summary based on message count and topics
        user_messages = [msg['message'] for msg in history if msg['speaker'] == 'user']
        
        if not user_messages:
            return "Greeting only"
        
        # Basic keyword extraction
        all_text = ' '.join(user_messages).lower()
        keywords = []
        
        topic_keywords = {
            'music': ['music', 'song', 'journey', 'band', 'singing'],
            'personal': ['life', 'feeling', 'day', 'work', 'family'],
            'advice': ['advice', 'help', 'problem', 'question'],
            'fan': ['fan', 'love', 'favorite', 'amazing']
        }
        
        for topic, words in topic_keywords.items():
            if any(word in all_text for word in words):
                keywords.append(topic)
        
        if keywords:
            return f"Conversation about: {', '.join(keywords)}"
        else:
            return f"General conversation ({len(user_messages)} exchanges)"
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default user preferences"""
        return {
            'preferred_greeting': "Hey there! This is Steve Perry.",
            'conversation_style': "warm and musical",
            'topics_of_interest': ["music", "Journey", "rock and roll", "singing"],
            'voice_settings': self.config['app']['voice_settings'].copy()
        }
    
    def load_memory(self) -> Dict[str, Any]:
        """Load memory with caching and error handling"""
        try:
            # Check cache first
            if self.memory_cache:
                return self.memory_cache
            
            if not os.path.exists('memory.json'):
                default_memory = {
                    'conversations': [],
                    'user_preferences': self._get_default_preferences(),
                    'recordings': []
                }
                self.save_memory(default_memory)
                return default_memory
            
            with open('memory.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            if not isinstance(data, dict):
                raise ValueError("Invalid memory format")
            
            # Ensure required keys exist
            required_keys = ['conversations', 'user_preferences', 'recordings']
            for key in required_keys:
                if key not in data:
                    data[key] = [] if key != 'user_preferences' else self._get_default_preferences()
            
            # Cache the data
            self.memory_cache = data
            return data
            
        except Exception as e:
            logger.error(f"Load memory error: {e}")
            default_memory = {
                'conversations': [],
                'user_preferences': self._get_default_preferences(),
                'recordings': []
            }
            return default_memory
    
    def save_memory(self, memory_data: Dict[str, Any]) -> bool:
        """Save memory with validation and backup"""
        try:
            if not isinstance(memory_data, dict):
                logger.error("Memory data must be a dictionary")
                return False
            
            # Create backup of existing memory
            if os.path.exists('memory.json'):
                backup_name = f"memory_backup_{int(time.time())}.json"
                try:
                    os.rename('memory.json', backup_name)
                    # Keep only last 5 backups
                    backups = sorted([f for f in os.listdir('.') if f.startswith('memory_backup_')])
                    for old_backup in backups[:-5]:
                        os.remove(old_backup)
                except Exception as backup_error:
                    logger.warning(f"Backup creation failed: {backup_error}")
            
            # Save new memory
            with open('memory.json', 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            # Update cache
            self.memory_cache = memory_data.copy()
            
            return True
            
        except Exception as e:
            logger.error(f"Save memory error: {e}")
            return False
    
    def run(self):
        """Run the application with proper error handling"""
        try:
            # Create required directories
            os.makedirs('static/audio', exist_ok=True)
            os.makedirs('static/recordings', exist_ok=True)
            
            # Initialize memory if it doesn't exist
            if not os.path.exists('memory.json'):
                self.save_memory({
                    'conversations': [],
                    'user_preferences': self._get_default_preferences(),
                    'recordings': []
                })
            
            # Log startup information
            logger.info("🚀 Starting AI Voice Assistant...")
            logger.info(f"📱 Dashboard: http://localhost:{self.config['flask']['port']}")
            logger.info(f"🔧 Twilio: {'✅ Ready' if self.twilio_client else '⚠️  Not configured'}")
            logger.info(f"🤖 OpenAI: {'✅ Ready' if self.openai_client else '⚠️  Not configured'}")
            logger.info(f"🎤 ElevenLabs: {'✅ Ready' if self.config['elevenlabs']['api_key'] else '⚠️  Not configured'}")
            
            # Start the application
            self.socketio.run(
                self.app,
                debug=self.config['flask']['debug'],
                host='0.0.0.0',
                port=self.config['flask']['port'],
                use_reloader=False,
                log_output=True
            )
            
        except KeyboardInterrupt:
            logger.info("👋 Shutting down gracefully...")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            logger.error(traceback.format_exc())
            sys.exit(1)

# Application factory
def create_app():
    """Create and configure the application"""
    return AIVoiceAssistant()

if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run()
