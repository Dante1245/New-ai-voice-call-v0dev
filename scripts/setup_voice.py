#!/usr/bin/env python3
"""
Script to set up ElevenLabs voice cloning for Steve Perry
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_voices():
    """List all available voices in ElevenLabs"""
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": os.environ.get('ELEVENLABS_API_KEY')
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        voices = response.json()
        print("Available voices:")
        for voice in voices['voices']:
            print(f"- {voice['name']}: {voice['voice_id']}")
    else:
        print(f"Error: {response.status_code}")

def create_steve_perry_voice():
    """Create a Steve Perry voice clone (requires audio samples)"""
    print("To create a Steve Perry voice clone:")
    print("1. Collect high-quality audio samples of Steve Perry speaking")
    print("2. Use ElevenLabs Voice Lab to create a custom voice")
    print("3. Copy the voice ID to your .env file")
    print("4. Test the voice using the test_voice() function")

def test_voice(voice_id, text="Hey there! This is Steve Perry from Journey."):
    """Test a voice with sample text"""
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
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("test_voice.mp3", "wb") as f:
            f.write(response.content)
        print("Voice test saved as test_voice.mp3")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    print("ElevenLabs Voice Setup for Steve Perry AI Assistant")
    print("=" * 50)
    
    if not os.environ.get('ELEVENLABS_API_KEY'):
        print("Please set ELEVENLABS_API_KEY in your .env file")
        exit(1)
    
    list_available_voices()
    print("\n")
    create_steve_perry_voice()
    
    # Test with a default voice if no custom voice ID is set
    voice_id = os.environ.get('ELEVENLABS_VOICE_ID')
    if voice_id:
        print(f"\nTesting voice ID: {voice_id}")
        test_voice(voice_id)
    else:
        print("\nSet ELEVENLABS_VOICE_ID in .env to test your custom voice")
