#!/usr/bin/env python3
"""
TeamLab Ticket Reminder - May 1, 2026
Sends Telegram reminder to book TeamLab tickets for July trip
"""
import requests
from datetime import datetime

def send_teamlab_reminder():
    bot_token = "8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA"
    chat_id = "7652382077"
    
    message = """🎨 **TeamLab Tickets Available TODAY!**

📅 **July 2026 trip tickets** are now on sale!

**Action needed:**
1. Visit: https://teamlabplanets.dmm.com/en
2. Select your July dates
3. Book timed-entry tickets ASAP

**Details:**
- 💰 Price: ~¥3,800 ($38 CAD) per adult
- ⏰ Timed entry (choose your slot)
- 📱 QR code on phone (no printing)
- ⚠️ Weekends sell out fast!

**For your July trip:**
- Tokyo: July (check exact dates)
- Popular attraction - book early!

Need help booking? I'm here! 🚀"""

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ TeamLab reminder sent at {datetime.now()}")
        else:
            print(f"❌ Failed to send: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_teamlab_reminder()
