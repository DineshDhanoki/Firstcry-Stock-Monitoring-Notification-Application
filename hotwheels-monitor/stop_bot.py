#!/usr/bin/env python3
"""
Script to stop the Telegram bot
"""

import os
import signal
import psutil

def stop_bot():
    """Stop the running Telegram bot"""
    try:
        # Find and kill the telegram_bot.py process
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and 'telegram_bot.py' in ' '.join(proc.info['cmdline']):
                    print(f"🛑 Stopping bot process (PID: {proc.info['pid']})")
                    proc.terminate()
                    proc.wait(timeout=5)
                    print("✅ Bot stopped successfully!")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        
        print("❌ Bot process not found or already stopped")
        
    except Exception as e:
        print(f"❌ Error stopping bot: {e}")

if __name__ == "__main__":
    stop_bot()
