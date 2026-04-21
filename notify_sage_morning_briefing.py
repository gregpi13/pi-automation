#!/usr/bin/env python3
"""
Notify Sage that morning briefing draft is ready for verification
Runs after draft creation to alert via Telegram
"""
import json
import requests
from datetime import datetime

def notify_sage():
    """Read verification file and send Telegram notification to Sage"""
    
    try:
        # Read verification file
        with open('/home/groot13-pi/.openclaw/morning_briefing_verify.json', 'r') as f:
            data = json.load(f)
        
        # Check if already sent
        if data.get('status') == 'SENT':
            print("Briefing already sent, skipping notification")
            return
        
        # Build status message
        weather_status = data.get('weather', '❌ Unknown')
        events_count = data.get('events_count', 0)
        news_count = data.get('news_count', 0)
        issues = data.get('issues', [])
        
        # Format message for Telegram
        status_emoji = "✅" if "✅" in weather_status else "⚠️"
        
        message = f"""🌅 MORNING BRIEFING READY FOR REVIEW

Date: {data.get('date')}
Time: {data.get('time')}

📊 Status:
• Weather: {weather_status}
• Events: {events_count} found
• News: {news_count} articles

"""
        
        if issues:
            message += "⚠️ ISSUES TO CHECK:\n"
            for issue in issues:
                message += f"• {issue}\n"
            message += "\n"
        
        message += """✅ ACTION NEEDED:
1. Check weather API if needed
2. Verify all sections complete
3. Send briefing by 6:00 AM

Run: python3 /home/groot13-pi/.openclaw/send_morning_agentmail.py --send-verified
"""
        
        # Send Telegram notification
        bot_token = "8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA"
        chat_id = "7652382077"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Sage notified at {datetime.now().strftime('%H:%M:%S')}")
            # Log notification
            with open('/home/groot13-pi/.openclaw/logs/morning_notifications.log', 'a') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Notified Sage: Weather {weather_status}, {events_count} events, {news_count} news\n")
        else:
            print(f"❌ Failed to notify Sage: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error notifying Sage: {e}")

if __name__ == "__main__":
    notify_sage()
