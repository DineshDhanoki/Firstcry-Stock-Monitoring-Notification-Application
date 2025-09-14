#!/usr/bin/env python3
"""
Quick test to verify bot is working
"""

import requests
import os
from dotenv import load_dotenv

def test_bot_status():
    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("❌ Bot token or chat ID not found!")
        return False
    
    try:
        # Test bot info
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print("✅ Bot is running!")
            print(f"Bot Name: {bot_info.get('first_name')}")
            print(f"Bot Username: @{bot_info.get('username')}")
            print()
            print("📱 Now go to Telegram and:")
            print("1. Search for @Hotwheels_stock_bot")
            print("2. Send /start")
            print("3. Click 'Browse HotWheels'")
            print("4. Select your pincode")
            print("5. You should see 48+ real HotWheels products!")
            return True
        else:
            print(f"❌ Bot error: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing bot: {e}")
        return False

if __name__ == "__main__":
    test_bot_status()
