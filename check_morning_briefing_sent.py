#!/usr/bin/env python3
"""
Backup reminder - checks if morning briefing was sent by 5:55 AM
If not sent, alerts Sage to send ASAP
"""
import json
import os
from datetime import datetime

def check_and_remind():
    verify_file = '/home/groot13-pi/.openclaw/morning_briefing_verify.json'
    
    if not os.path.exists(verify_file):
        print("No verification file found - draft may not have been created")
        return
    
    with open(verify_file, 'r') as f:
        data = json.load(f)
    
    # Check if already sent
    if data.get('status') == 'SENT':
        print(f"✅ Briefing already sent at {data.get('sent_time')}")
        return
    
    # Not sent - create reminder
    reminder = f"""
⚠️ MORNING BRIEFING NOT YET SENT

Time: {datetime.now().strftime('%H:%M')}
Status: Draft created but not sent

Draft: {data.get('date')}
Weather: {data.get('weather')}
Events: {data.get('events_count')}
News: {data.get('news_count')}

⏰ ACTION REQUIRED: Send now!
Command: python3 /home/groot13-pi/.openclaw/send_morning_agentmail.py --send-verified
"""
    
    print(reminder)
    
    # Log reminder
    with open('/home/groot13-pi/.openclaw/logs/morning_reminders.log', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - REMINDER: Briefing not sent\n")

if __name__ == "__main__":
    check_and_remind()
