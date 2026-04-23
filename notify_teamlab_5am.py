#!/usr/bin/env python3
"""
5 AM TeamLab Notification
Checks 1 AM scan results and notifies Greg
"""
import json
import requests
from datetime import datetime

def send_teamlab_notification():
    bot_token = "8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA"
    chat_id = "7652382077"
    
    # Load 1 AM check result
    result_file = '/home/groot13-pi/.openclaw/teamlab_check_result.json'
    
    try:
        with open(result_file, 'r') as f:
            result = json.load(f)
        
        if result.get('status') == 'july_available':
            message = """🎨 **TeamLab July Tickets ARE AVAILABLE!**

✅ July 2026 dates found on calendar!

**Action needed NOW:**
1. Visit: https://teamlabplanets.dmm.com/en/ticket
2. Select your July dates
3. Book immediately - weekends sell out fast!

**Details:**
- 💰 Price: ~¥3,800 ($38 CAD)
- ⏰ Timed entry slots
- 📱 QR code on phone

Don't wait - book today! 🚀"""
        else:
            message = """📅 **TeamLab Update**

⏳ July 2026 tickets NOT YET available

**Status:** Still waiting for late April release

**Your action:**
- Check website today: https://teamlabplanets.dmm.com/en/ticket
- July dates should appear any day now
- Book immediately when you see them!

I'll keep checking every night at 1 AM ✅"""
        
        # Send Telegram message
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ TeamLab notification sent at {datetime.now()}")
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except FileNotFoundError:
        print("⚠️ No 1 AM check result found")
        # Send reminder anyway
        message = """📅 **TeamLab Reminder**

⚠️ Couldn't check website automatically

**Please check manually:**
https://teamlabplanets.dmm.com/en/ticket

Look for July 2026 dates on the calendar!

Red triangle = limited tickets
Circle = available  
X = sold out"""
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(url, data=payload, timeout=10)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    send_teamlab_notification()
