#!/usr/bin/env python3
"""
Script to test Twilio call recording functionality
"""

import requests
import os
import json
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure to set environment variables manually.")

def test_recording_endpoints():
    """Test the recording API endpoints"""
    base_url = "http://localhost:5000"  # Change this for production
    
    print("Testing Call Recording Endpoints")
    print("=" * 40)
    
    # Test get recordings
    try:
        response = requests.get(f"{base_url}/get_recordings", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get recordings: Found {len(data.get('recordings', []))} recordings")
            
            # Display recordings
            for recording in data.get('recordings', [])[:3]:  # Show first 3
                print(f"   - {recording['sid'][:8]}... | Duration: {recording.get('duration', 'N/A')}s")
        else:
            print(f"❌ Get recordings failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get recordings error: {e}")
    
    print("\n" + "=" * 40)
    print("Recording Test Complete!")
    print("\nTo test full recording functionality:")
    print("1. Start the Flask app: python app.py")
    print("2. Open the dashboard: http://localhost:5000")
    print("3. Make a test call and start recording")
    print("4. Check the recordings panel for playback")

def check_twilio_config():
    """Check if Twilio is properly configured for recording"""
    print("Checking Twilio Configuration for Recording")
    print("=" * 45)
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_PHONE_NUMBER'
    ]
    
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    else:
        print("✅ All Twilio environment variables are set")
        return True

def create_test_memory():
    """Create test memory with recording structure"""
    memory = {
        "conversations": [],
        "user_preferences": {
            "preferred_greeting": "Hey there! This is Steve Perry.",
            "conversation_style": "warm and musical",
            "topics_of_interest": ["music", "Journey", "rock and roll", "singing"],
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        },
        "recordings": []
    }
    
    try:
        with open('memory.json', 'w') as f:
            json.dump(memory, f, indent=2)
        print("✅ Created test memory.json with recording structure")
    except Exception as e:
        print(f"❌ Error creating memory.json: {e}")

if __name__ == "__main__":
    print("🎵 Twilio Call Recording Test Suite")
    print("=" * 50)
    
    # Check configuration
    if check_twilio_config():
        print()
        create_test_memory()
        print()
        test_recording_endpoints()
    else:
        print("\nPlease configure your Twilio credentials in .env file:")
        print("TWILIO_ACCOUNT_SID=your_account_sid")
        print("TWILIO_AUTH_TOKEN=your_auth_token") 
        print("TWILIO_PHONE_NUMBER=your_twilio_number")
