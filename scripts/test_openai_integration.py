#!/usr/bin/env python3
"""
Test OpenAI integration with the provided API key
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system environment variables.")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("❌ OpenAI SDK not installed. Run: pip install openai==1.3.0")
    sys.exit(1)

def test_openai_connection():
    """Test OpenAI API connection and functionality"""
    print("🤖 Testing OpenAI Integration")
    print("=" * 40)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    if api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key is still placeholder")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
        
        # Test basic completion
        print("\n🧪 Testing basic completion...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'OpenAI API test successful'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Basic test response: {result}")
        
        # Test Steve Perry character response
        print("\n🎤 Testing Steve Perry character...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Steve Perry from Journey. Respond in character with warmth and occasional music references."},
                {"role": "user", "content": "Hey Steve, how are you doing today?"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        steve_response = response.choices[0].message.content.strip()
        print(f"✅ Steve Perry response: {steve_response}")
        
        # Test smart reply generation
        print("\n💬 Testing smart reply generation...")
        prompt = """You are Steve Perry, the legendary lead singer of Journey. 
        Respond to what the user said with 3 different warm, conversational responses.
        Keep each response under 30 words and occasionally reference music.
        
        User said: I'm having a tough day at work
        
        Give exactly 3 numbered responses:"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Steve Perry from Journey. Be warm and conversational."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        smart_replies = response.choices[0].message.content.strip()
        print(f"✅ Smart replies generated:")
        for line in smart_replies.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        
        print("\n🎉 All OpenAI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_steve_perry_knowledge():
    """Test Steve Perry knowledge integration"""
    print("\n🎵 Testing Steve Perry Knowledge Integration")
    print("-" * 40)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test with Steve Perry knowledge
        steve_context = """You are Steve Perry, the legendary lead singer of Journey. 
        Key facts about you:
        - Born January 22, 1949, in Hanford, California
        - Joined Journey in 1977 and transformed their sound
        - Known for hits like "Don't Stop Believin'", "Open Arms", "Faithfully"
        - Left Journey in 1998 due to health issues
        - Made a comeback with "Traces" album in 2018
        - Currently in a relationship with Donna Handa who helps you stay grounded
        - You're warm, conversational, and occasionally reference music and Journey
        """
        
        test_questions = [
            "Tell me about your time with Journey",
            "What's your favorite song you recorded?",
            "How do you feel about your comeback?",
            "What keeps you motivated these days?"
        ]
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": steve_context},
                    {"role": "user", "content": question}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            print(f"🎤 Steve Perry: {answer}")
        
        print("\n✅ Steve Perry knowledge integration working!")
        return True
        
    except Exception as e:
        print(f"❌ Knowledge integration error: {e}")
        return False

def run_complete_openai_test():
    """Run complete OpenAI integration test"""
    print("🚀 Complete OpenAI Integration Test")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = test_openai_connection()
    
    if connection_ok:
        # Test Steve Perry knowledge
        knowledge_ok = test_steve_perry_knowledge()
        
        print("\n" + "=" * 50)
        print("📋 OpenAI Test Summary")
        print("-" * 25)
        print(f"API Connection: {'✅ Working' if connection_ok else '❌ Failed'}")
        print(f"Steve Perry AI: {'✅ Working' if knowledge_ok else '❌ Failed'}")
        
        if connection_ok and knowledge_ok:
            print("\n🎉 OpenAI integration fully operational!")
            print("✅ Your AI Voice Assistant is ready for intelligent conversations")
            print("\nNext steps:")
            print("1. python app.py")
            print("2. Open http://localhost:5000")
            print("3. Make a test call to experience Steve Perry AI")
        else:
            print("\n⚠️  Some issues found. Check the errors above.")
    else:
        print("\n❌ OpenAI connection failed. Please check your API key.")

if __name__ == "__main__":
    run_complete_openai_test()
