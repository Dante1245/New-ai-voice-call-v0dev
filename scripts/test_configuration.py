#!/usr/bin/env python3
"""
Script to test all API configurations and credentials
"""

import os
import requests
from twilio.rest import Client
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure to set environment variables manually.")

def test_twilio_config():
    """Test Twilio configuration and credentials"""
    print("🔧 Testing Twilio Configuration")
    print("-" * 40)
    
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, phone_number]):
        print("❌ Missing Twilio credentials")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        # Test account access
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account Status: {account.status}")
        print(f"✅ Account SID: {account_sid[:8]}...")
        
        # Test phone number
        try:
            incoming_phone_number = client.incoming_phone_numbers.list(
                phone_number=phone_number
            )
            if incoming_phone_number:
                print(f"✅ Phone Number: {phone_number} (verified)")
            else:
                print(f"⚠️  Phone Number: {phone_number} (not found in account)")
        except Exception as e:
            print(f"⚠️  Phone Number: Could not verify - {e}")
        
        # Test call capability
        print("✅ Twilio client initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Twilio Error: {e}")
        return False

def test_elevenlabs_config():
    """Test ElevenLabs configuration and voice"""
    print("\n🎤 Testing ElevenLabs Configuration")
    print("-" * 40)
    
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    voice_id = os.environ.get('ELEVENLABS_VOICE_ID')
    
    if not api_key:
        print("❌ Missing ElevenLabs API key")
        return False
    
    if not voice_id:
        print("❌ Missing ElevenLabs Voice ID")
        return False
    
    try:
        # Test API access
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key
        }
        
        response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=10)
        
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ API Access: Connected successfully")
            print(f"✅ Available Voices: {len(voices.get('voices', []))}")
            
            # Check if our voice ID exists
            voice_found = False
            for voice in voices.get('voices', []):
                if voice.get('voice_id') == voice_id:
                    print(f"✅ Voice Found: {voice.get('name', 'Unknown')} ({voice_id[:8]}...)")
                    voice_found = True
                    break
            
            if not voice_found:
                print(f"⚠️  Voice ID {voice_id[:8]}... not found in your account")
                print("   Available voices:")
                for voice in voices.get('voices', [])[:5]:  # Show first 5
                    print(f"   - {voice.get('name', 'Unknown')}: {voice.get('voice_id', 'No ID')}")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ElevenLabs Error: {e}")
        return False

def test_openai_config():
    """Test OpenAI configuration"""
    print("\n🤖 Testing OpenAI Configuration")
    print("-" * 40)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ Missing or placeholder OpenAI API key")
        print("   Please set OPENAI_API_KEY in your .env file")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✅ OpenAI API: Connected successfully")
            print(f"✅ Test Response: {response.choices[0].message.content.strip()}")
            return True
        else:
            print("❌ OpenAI API: No response received")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return False

def test_voice_synthesis():
    """Test complete voice synthesis pipeline"""
    print("\n🎵 Testing Voice Synthesis Pipeline")
    print("-" * 40)
    
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    voice_id = os.environ.get('ELEVENLABS_VOICE_ID')
    
    if not all([api_key, voice_id]):
        print("❌ Missing ElevenLabs credentials for voice test")
        return False
    
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": "Hey there! This is Steve Perry from Journey. Testing the voice synthesis.",
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Save test audio
            os.makedirs('static/audio', exist_ok=True)
            with open("static/audio/voice_test.mp3", "wb") as f:
                f.write(response.content)
            print("✅ Voice Synthesis: Test successful")
            print("✅ Audio File: Saved as static/audio/voice_test.mp3")
            return True
        else:
            print(f"❌ Voice Synthesis Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice Synthesis Error: {e}")
        return False

def generate_webhook_urls():
    """Generate webhook URLs for Twilio configuration"""
    print("\n🔗 Webhook Configuration")
    print("-" * 40)
    
    base_url = "https://your-app-name.onrender.com"  # Update this with your actual Render URL
    
    print("Configure these webhook URLs in your Twilio Console:")
    print(f"📞 Voice URL: {base_url}/answer")
    print(f"🎵 Recording URL: {base_url}/recording_complete")
    print(f"📱 Status Callback: {base_url}/call_status")
    
    print("\nTwilio Console Steps:")
    print("1. Go to https://console.twilio.com/")
    print("2. Navigate to Phone Numbers > Manage > Active numbers")
    print(f"3. Click on your number: {os.environ.get('TWILIO_PHONE_NUMBER', 'YOUR_NUMBER')}")
    print("4. Set Voice webhook to the Voice URL above")
    print("5. Set HTTP method to POST")

if __name__ == "__main__":
    print("🚀 AI Voice Assistant Configuration Test")
    print("=" * 50)
    
    # Test all configurations
    twilio_ok = test_twilio_config()
    elevenlabs_ok = test_elevenlabs_config()
    openai_ok = test_openai_config()
    
    if elevenlabs_ok:
        voice_ok = test_voice_synthesis()
    else:
        voice_ok = False
    
    # Generate webhook info
    generate_webhook_urls()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Configuration Summary")
    print("-" * 25)
    print(f"Twilio: {'✅ Ready' if twilio_ok else '❌ Needs Setup'}")
    print(f"ElevenLabs: {'✅ Ready' if elevenlabs_ok else '❌ Needs Setup'}")
    print(f"OpenAI: {'✅ Ready' if openai_ok else '❌ Needs Setup'}")
    print(f"Voice Synthesis: {'✅ Ready' if voice_ok else '❌ Needs Setup'}")
    
    if all([twilio_ok, elevenlabs_ok, voice_ok]):
        print("\n🎉 All systems ready! You can start making calls.")
        print("Run: python app.py")
    else:
        print("\n⚠️  Please fix the issues above before proceeding.")
