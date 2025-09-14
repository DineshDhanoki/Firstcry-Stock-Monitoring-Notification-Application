#!/usr/bin/env python3
"""
Test script for Telegram notifications
Run this to verify your Telegram bot is working correctly
"""

import os
import requests
from dotenv import load_dotenv

def test_telegram():
    # Load environment variables
    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("❌ Telegram not configured!")
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env file")
        return False
    
    test_message = "🤖 Test message from HotWheels Monitor!\n\nThis confirms your Telegram bot is working correctly."
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, json={
            "chat_id": chat_id, 
            "text": test_message
        }, timeout=10)
        response.raise_for_status()
        
        print("✅ Telegram test successful!")
        print(f"Message sent to chat ID: {chat_id}")
        return True
        
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Telegram notifications...")
    test_telegram()
