#!/usr/bin/env python3
"""
Test script to verify Telegram bot is working
"""

import requests
import os
from dotenv import load_dotenv

def test_bot():
    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("❌ Bot token or chat ID not found!")
        return
    
    # Test bot info
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print("✅ Bot is running!")
            print(f"Bot Name: {bot_info.get('first_name')}")
            print(f"Bot Username: @{bot_info.get('username')}")
            print(f"Bot ID: {bot_info.get('id')}")
            print()
            print("📱 Now go to Telegram and:")
            print("1. Search for @Hotwheels_stock_bot")
            print("2. Start a chat with the bot")
            print("3. Send /start to see the menu")
            print("4. Use the interactive buttons to browse HotWheels!")
        else:
            print(f"❌ Bot error: {data}")
            
    except Exception as e:
        print(f"❌ Error testing bot: {e}")

if __name__ == "__main__":
    test_bot()
