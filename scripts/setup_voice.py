#!/usr/bin/env python3
"""
Script to set up ElevenLabs voice cloning for Steve Perry
"""

import requests
import os
import sys

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure to set environment variables manually.")

def list_available_voices():
    """List all available voices in ElevenLabs"""
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment variables")
        return False
    
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            voices = response.json()
            print("Available voices:")
            for voice in voices.get('voices', []):
                print(f"- {voice.get('name', 'Unknown')}: {voice.get('voice_id', 'No ID')}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def create_steve_perry_voice():
    """Create a Steve Perry voice clone (requires audio samples)"""
    print("\nTo create a Steve Perry voice clone:")
    print("1. Collect high-quality audio samples of Steve Perry speaking (not singing)")
    print("2. Go to https://elevenlabs.io/voice-lab")
    print("3. Upload the audio samples and create a custom voice")
    print("4. Copy the voice ID to your .env file as ELEVENLABS_VOICE_ID")
    print("5. Test the voice using the test_voice() function")

def test_voice(voice_id, text="Hey there! This is Steve Perry from Journey."):
    """Test a voice with sample text"""
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment variables")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
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
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            with open("test_voice.mp3", "wb") as f:
                f.write(response.content)
            print("Voice test saved as test_voice.mp3")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("ElevenLabs Voice Setup for Steve Perry AI Assistant")
    print("=" * 50)
    
    # Check for required packages
    try:
        import requests
    except ImportError:
        print("Error: 'requests' package not found. Please install it with: pip install requests")
        sys.exit(1)
    
    if not os.environ.get('ELEVENLABS_API_KEY'):
        print("Error: Please set ELEVENLABS_API_KEY in your .env file")
        print("You can get your API key from: https://elevenlabs.io/")
        sys.exit(1)
    
    # List available voices
    if list_available_voices():
        print("\n")
        create_steve_perry_voice()
        
        # Test with a custom voice if voice ID is set
        voice_id = os.environ.get('ELEVENLABS_VOICE_ID')
        if voice_id:
            print(f"\nTesting voice ID: {voice_id}")
            if test_voice(voice_id):
                print("Voice test completed successfully!")
            else:
                print("Voice test failed. Please check your voice ID.")
        else:
            print("\nSet ELEVENLABS_VOICE_ID in .env to test your custom voice")
    else:
        print("Failed to connect to ElevenLabs API. Please check your API key and internet connection.")
