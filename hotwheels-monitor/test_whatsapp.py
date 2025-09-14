#!/usr/bin/env python3
"""
Test script for WhatsApp notifications via Twilio
Run this to verify your Twilio WhatsApp setup is working correctly
"""

import os
from dotenv import load_dotenv

def test_whatsapp():
    # Load environment variables
    load_dotenv()
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")
    to_number = os.getenv("TWILIO_WHATSAPP_TO")
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print("❌ WhatsApp not configured!")
        print("Please set all TWILIO_* variables in your .env file")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(account_sid, auth_token)
        
        test_message = "🤖 Test message from HotWheels Monitor!\n\nThis confirms your WhatsApp integration is working correctly."
        
        message = client.messages.create(
            body=test_message,
            from_=from_number,
            to=to_number
        )
        
        print("✅ WhatsApp test successful!")
        print(f"Message SID: {message.sid}")
        print(f"Message sent to: {to_number}")
        return True
        
    except Exception as e:
        print(f"❌ WhatsApp test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if your Twilio account is active")
        print("2. Verify phone numbers are in correct format: whatsapp:+1234567890")
        print("3. Make sure you've joined the WhatsApp sandbox")
        print("4. Check if you have sufficient Twilio credits")
        return False

if __name__ == "__main__":
    print("Testing WhatsApp notifications...")
    test_whatsapp()
