#!/usr/bin/env python3
"""
Daily weight/workout reminder for Greg
Sends Telegram message at 6:30 AM ONLY if workout not yet logged
Uses Telegram HTTP API (no OpenClaw runtime dependency)
"""
import json
import requests
from datetime import datetime

# Configuration
TRACKER_FILE = "/home/groot13-pi/.openclaw/workspace/PROJECTS/weight_loss_tracker/tracker.json"
TELEGRAM_BOT_TOKEN = "8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA"
TELEGRAM_CHAT_ID = "7652382077"

def workout_logged_today():
    """Check if workout was already logged for today"""
    try:
        with open(TRACKER_FILE, 'r') as f:
            data = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        for entry in data.get('entries', []):
            entry_date = entry.get('date', '')
            # Check if entry date matches today (handle both formats)
            if entry_date == today or entry_date.startswith(today):
                return True
        
        return False
    except Exception as e:
        print(f"⚠️ Could not check tracker: {e}")
        return False  # Assume not logged if we can't check

def send_telegram_message(message):
    """Send message via Telegram HTTP API"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("✅ Daily reminder sent successfully")
            return True
        else:
            print(f"❌ Failed to send: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    print(f"Checking tracker at {datetime.now()}")
    
    # Check if already logged
    if workout_logged_today():
        print("✅ Workout already logged today - no reminder needed")
        return
    
    # Send reminder
    message = """🌅 Good morning, Greg!

📊 **Daily Check-In Reminder**

Please reply with your:
• Weight this morning (lbs)
• Did you workout? (yes/no)
• If yes: What type and how long?
• Any notes about yesterday?

Example: "186.5 lbs, yes - 30 min cardio, feeling good"

_You can reply whenever convenient — this is just your reminder._"""
    
    send_telegram_message(message)

if __name__ == '__main__':
    main()
