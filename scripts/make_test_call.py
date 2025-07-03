#!/usr/bin/env python3
"""
Script to make a test call to verify the complete system
"""

import os
import time
from twilio.rest import Client

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure to set environment variables manually.")

def make_test_call():
    """Make a test call to verify the system"""
    print("📞 Making Test Call")
    print("-" * 30)
    
    # Get credentials
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')
    to_number = os.environ.get('TEST_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print("❌ Missing required credentials")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url='http://your-ngrok-url.ngrok.io/answer',  # Update with your ngrok URL for testing
            method='POST'
        )
        
        print(f"✅ Call initiated successfully!")
        print(f"📱 Call SID: {call.sid}")
        print(f"📞 From: {from_number}")
        print(f"📱 To: {to_number}")
        print(f"⏰ Status: {call.status}")
        
        # Monitor call status
        print("\n⏳ Monitoring call status...")
        for i in range(10):  # Check for 10 seconds
            time.sleep(1)
            updated_call = client.calls(call.sid).fetch()
            print(f"Status: {updated_call.status}")
            
            if updated_call.status in ['completed', 'failed', 'canceled']:
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Call Error: {e}")
        return False

if __name__ == "__main__":
    print("🎤 AI Voice Assistant Test Call")
    print("=" * 40)
    
    print("⚠️  IMPORTANT: Make sure your Flask app is running with ngrok!")
    print("1. Start Flask: python app.py")
    print("2. Start ngrok: ngrok http 5000")
    print("3. Update the webhook URL in this script")
    print("4. Run this test")
    
    proceed = input("\nReady to make test call? (y/n): ")
    if proceed.lower() == 'y':
        make_test_call()
    else:
        print("Test call cancelled.")
