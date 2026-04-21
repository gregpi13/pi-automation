#!/usr/bin/env python3
"""
Notify Sage that Tokyo trip briefing draft is ready
Runs after draft creation to alert via Telegram
"""
import json
import requests
from datetime import datetime

def notify_sage():
    """Read verification file and send Telegram notification to Sage"""
    
    try:
        # Read verification file
        with open('/home/groot13-pi/.openclaw/trip_briefing_verify.json', 'r') as f:
            data = json.load(f)
        
        # Check if already sent
        if data.get('status') == 'SENT':
            print("Trip briefing already sent, skipping notification")
            return
        
        # Build status message
        weather_status = data.get('weather', '❌ Unknown')
        trip_date = data.get('trip_date', 'Unknown')
        emails_count = len(data.get('emails', []))
        issues = data.get('issues', [])
        
        # Format message for Telegram
        status_emoji = "✅" if "✅" in weather_status else "⚠️"
        
        message = f"""🗼 TOKYO TRIP BRIEFING READY FOR REVIEW

Trip Date: {trip_date}
Draft Time: {data.get('time')}

📊 Status:
• Weather: {weather_status}
• Recipients: {emails_count} emails
• Travel: {data.get('travel', 'N/A')[:30]}...
• Hotel: {data.get('hotel', 'N/A')[:30]}...

"""
        
        if issues:
            message += "⚠️ ISSUES TO CHECK:\n"
            for issue in issues:
                message += f"• {issue}\n"
            message += "\n"
        
        message += """✅ ACTION NEEDED:
1. Check weather if needed
2. Verify itinerary details
3. Send briefing ASAP

Run: python3 /home/groot13-pi/.openclaw/trip_briefing.py --send-verified
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
        else:
            print(f"❌ Failed to notify Sage: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error notifying Sage: {e}")

if __name__ == "__main__":
    notify_sage()
