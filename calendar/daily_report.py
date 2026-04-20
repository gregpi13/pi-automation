#!/usr/bin/env python3
"""
Generate daily calendar summary email
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from datetime import datetime
import os

def send_daily_calendar_summary():
    EMAIL = "sage.ai.pi.2026@gmail.com"
    PASSWORD_FILE = os.path.expanduser("~/.openclaw/.gmail-app-password")
    
    with open(PASSWORD_FILE, 'r') as f:
        PASSWORD = f.read().strip()
    
    # Load calendar events
    calendar_file = os.path.expanduser("~/.openclaw/workspace/calendar/events.json")
    
    if not os.path.exists(calendar_file):
        print("No calendar data yet")
        return
    
    with open(calendar_file, 'r') as f:
        events = json.load(f)
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    today_short = datetime.now().strftime("%A, %B %d")
    
    # Create summary email
    msg = MIMEMultipart()
    msg['From'] = f'Sage AI <{EMAIL}>'
    msg['To'] = 'Greg Harris <greg.m.harris@gmail.com>'
    msg['Subject'] = f'📅 Daily Schedule - {today_short}'
    msg['Date'] = formatdate(localtime=True)
    
    body = f"📅 GOOD MORNING, GREG\n"
    body += f"Daily Schedule for {today_short}\n"
    body += "="*50 + "\n\n"
    
    # Group events
    todays_events = []
    upcoming_events = []
    
    for event in events:
        # Parse date from start time (format: 20260404T180000)
        if event.get('start'):
            try:
                event_date = event['start'][:8]  # YYYYMMDD
                if event_date == today.replace('-', ''):
                    todays_events.append(event)
                else:
                    upcoming_events.append(event)
            except:
                upcoming_events.append(event)
    
    if todays_events:
        body += "🗓️ TODAY'S EVENTS:\n"
        body += "-" * 40 + "\n"
        for event in todays_events:
            body += f"\n• {event.get('summary', 'Unknown event')}\n"
            if event.get('location'):
                body += f"  Location: {event['location']}\n"
            if event.get('start'):
                # Parse time from start
                try:
                    time_str = event['start'][9:13]  # HHMM
                    if time_str:
                        time_formatted = f"{time_str[:2]}:{time_str[2:]}"
                        body += f"  Time: {time_formatted}\n"
                except:
                    pass
        body += "\n"
    else:
        body += "✅ No events scheduled for today.\n\n"
    
    if upcoming_events[:5]:
        body += "📋 UPCOMING EVENTS:\n"
        body += "-" * 40 + "\n"
        for event in upcoming_events[:5]:
            body += f"\n• {event.get('summary', 'Unknown event')}\n"
            if event.get('start'):
                try:
                    event_date = event['start'][:8]
                    formatted_date = f"{event_date[4:6]}/{event_date[6:]}"
                    body += f"  Date: {formatted_date}\n"
                except:
                    pass
        body += "\n"
    
    body += "="*50 + "\n"
    body += "Reply if you need me to take action on any of these.\n\n"
    body += "Sage 🌿"
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
    
    print(f"✅ Daily calendar summary sent to greg.m.harris@gmail.com")

if __name__ == "__main__":
    send_daily_calendar_summary()
