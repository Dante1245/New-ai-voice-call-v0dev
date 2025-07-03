from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from twilio.rest import Client
from twilio.twiml import VoiceResponse
import openai
import requests
import json
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize clients
twilio_client = Client(
    os.environ.get('TWILIO_ACCOUNT_SID'),
    os.environ.get('TWILIO_AUTH_TOKEN')
)
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Global state
call_state = {
    'status': 'Idle',
    'call_sid': None,
    'transcription': '',
    'conversation_history': [],
    'smart_replies': []
}

# Memory management
def load_memory():
    try:
        with open('memory.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'conversations': [], 'user_preferences': {}}

def save_memory(memory_data):
    with open('memory.json', 'w') as f:
        json.dump(memory_data, f, indent=2)

def add_to_memory(user_input, bot_response):
    memory = load_memory()
    memory['conversations'].append({
        'timestamp': datetime.now().isoformat(),
        'user': user_input,
        'bot': bot_response
    })
    # Keep only last 50 conversations
    memory['conversations'] = memory['conversations'][-50:]
    save_memory(memory)

# ElevenLabs integration
def text_to_speech(text, voice_id=None):
    """Convert text to speech using ElevenLabs API"""
    if not voice_id:
        voice_id = os.environ.get('ELEVENLABS_VOICE_ID', 'default-voice-id')
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ.get('ELEVENLABS_API_KEY')
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # Save audio file
            audio_filename = f"static/audio/response_{int(time.time())}.mp3"
            os.makedirs('static/audio', exist_ok=True)
            with open(audio_filename, 'wb') as f:
                f.write(response.content)
            return audio_filename
        else:
            print(f"ElevenLabs API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

# OpenAI integration
def generate_smart_replies(conversation_context, user_input):
    """Generate smart reply suggestions using OpenAI"""
    memory = load_memory()
    
    # Build context from memory
    context = "Previous conversations:\n"
    for conv in memory['conversations'][-5:]:  # Last 5 conversations
        context += f"User: {conv['user']}\nBot: {conv['bot']}\n"
    
    context += f"\nCurrent conversation:\n{conversation_context}"
    context += f"\nUser just said: {user_input}"
    
    prompt = f"""
    You are Steve Perry, the legendary lead singer of Journey. You're having a phone conversation.
    Based on the context below, generate 3 different response options that sound like Steve Perry would say them.
    Make them conversational, warm, and occasionally reference music or Journey when appropriate.
    
    Context:
    {context}
    
    Generate 3 different responses as a JSON array:
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Steve Perry from Journey. Respond in character."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        # Parse the response to extract suggestions
        content = response.choices[0].message.content
        # Try to extract JSON array, fallback to simple parsing
        try:
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                suggestions = json.loads(json_match.group())
            else:
                # Fallback: split by numbers or newlines
                lines = content.strip().split('\n')
                suggestions = [line.strip('123. ') for line in lines if line.strip()][:3]
        except:
            suggestions = [content[:100] + "..." if len(content) > 100 else content]
        
        return suggestions[:3]  # Ensure max 3 suggestions
        
    except Exception as e:
        print(f"Error generating smart replies: {e}")
        return ["Hey there!", "That's interesting!", "Tell me more about that."]

# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/start_call', methods=['POST'])
def start_call():
    """Initiate a call via Twilio"""
    data = request.json
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({'error': 'Phone number required'}), 400
    
    try:
        call = twilio_client.calls.create(
            to=phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            url=request.url_root + 'answer',
            method='POST'
        )
        
        call_state['status'] = 'Ringing'
        call_state['call_sid'] = call.sid
        
        # Emit status update
        socketio.emit('call_status_update', call_state)
        
        return jsonify({'success': True, 'call_sid': call.sid})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/answer', methods=['POST'])
def answer_call():
    """Handle incoming call and provide greeting"""
    response = VoiceResponse()
    
    # Update call status
    call_state['status'] = 'In Progress'
    call_state['call_sid'] = request.form.get('CallSid')
    
    # Generate greeting audio
    greeting = "Hey there! This is Steve Perry. How are you doing today?"
    audio_file = text_to_speech(greeting)
    
    if audio_file:
        response.play(request.url_root + audio_file)
    else:
        response.say(greeting, voice='man')
    
    # Set up for continuous conversation
    response.gather(
        input='speech',
        action='/process_speech',
        method='POST',
        speech_timeout='auto',
        timeout=10
    )
    
    # Add to conversation history
    call_state['conversation_history'].append({
        'speaker': 'bot',
        'message': greeting,
        'timestamp': datetime.now().isoformat()
    })
    
    # Emit update
    socketio.emit('call_status_update', call_state)
    
    return str(response)

@app.route('/process_speech', methods=['POST'])
def process_speech():
    """Process user speech and generate response"""
    user_speech = request.form.get('SpeechResult', '')
    
    if user_speech:
        # Add user speech to conversation
        call_state['conversation_history'].append({
            'speaker': 'user',
            'message': user_speech,
            'timestamp': datetime.now().isoformat()
        })
        call_state['transcription'] = user_speech
        
        # Generate smart replies
        conversation_context = '\n'.join([
            f"{msg['speaker']}: {msg['message']}" 
            for msg in call_state['conversation_history'][-10:]
        ])
        
        smart_replies = generate_smart_replies(conversation_context, user_speech)
        call_state['smart_replies'] = smart_replies
        
        # Emit updates
        socketio.emit('transcription_update', {
            'transcription': user_speech,
            'smart_replies': smart_replies
        })
        socketio.emit('call_status_update', call_state)
    
    # Continue listening
    response = VoiceResponse()
    response.gather(
        input='speech',
        action='/process_speech',
        method='POST',
        speech_timeout='auto',
        timeout=10
    )
    
    return str(response)

@app.route('/send_reply', methods=['POST'])
def send_reply():
    """Send a reply during active call"""
    data = request.json
    reply_text = data.get('reply', '')
    
    if not reply_text or not call_state['call_sid']:
        return jsonify({'error': 'No reply text or active call'}), 400
    
    try:
        # Generate audio
        audio_file = text_to_speech(reply_text)
        
        # Update the call with the response
        if audio_file:
            twiml = f'<Response><Play>{request.url_root + audio_file}</Play><Gather input="speech" action="/process_speech" method="POST" speechTimeout="auto" timeout="10"/></Response>'
        else:
            twiml = f'<Response><Say voice="man">{reply_text}</Say><Gather input="speech" action="/process_speech" method="POST" speechTimeout="auto" timeout="10"/></Response>'
        
        # Update call
        twilio_client.calls(call_state['call_sid']).update(twiml=twiml)
        
        # Add to conversation history and memory
        call_state['conversation_history'].append({
            'speaker': 'bot',
            'message': reply_text,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save to memory
        if call_state['conversation_history']:
            last_user_msg = next((msg['message'] for msg in reversed(call_state['conversation_history']) if msg['speaker'] == 'user'), '')
            if last_user_msg:
                add_to_memory(last_user_msg, reply_text)
        
        # Emit update
        socketio.emit('call_status_update', call_state)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/end_call', methods=['POST'])
def end_call():
    """End the current call"""
    if call_state['call_sid']:
        try:
            twilio_client.calls(call_state['call_sid']).update(status='completed')
            call_state['status'] = 'Idle'
            call_state['call_sid'] = None
            
            # Emit update
            socketio.emit('call_status_update', call_state)
            
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'No active call'}), 400

@app.route('/get_memory')
def get_memory():
    """Get conversation memory"""
    memory = load_memory()
    return jsonify(memory)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    emit('call_status_update', call_state)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/audio', exist_ok=True)
    
    # Initialize memory file if it doesn't exist
    if not os.path.exists('memory.json'):
        save_memory({'conversations': [], 'user_preferences': {}})
    
    socketio.run(app, debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
