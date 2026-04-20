#!/usr/bin/env python3
"""
Parse calendar invites from AgentMail and save to local calendar
"""

import agentmail
import json
import os
import re
import requests
from datetime import datetime

def load_api_key():
    """Load AgentMail API key from secure storage"""
    with open('/home/groot13-pi/.openclaw/secure/agentmail-api-key', 'r') as f:
        return f.read().strip()

def parse_ics_datetime(dt_str, tzid=None):
    """Parse ICS datetime and return formatted strings
    
    Handles formats:
    - DTSTART;TZID=America/Toronto:20260407T090000 (with timezone)
    - DTSTART:20260407T090000 (without timezone)  
    - DTSTART:20260407 (date only)
    """
    try:
        # Extract datetime part after the colon
        if ':' in dt_str:
            dt_part = dt_str.split(':')[-1]
        else:
            dt_part = dt_str
        
        # Handle date part (YYYYMMDD)
        if len(dt_part) >= 8:
            date_part = dt_part[:8]
            formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
            
            # Check if date is today
            today = datetime.now().strftime('%Y-%m-%d')
            is_today = formatted_date == today
            
            # Handle time component if present (HHMMSS)
            time_formatted = ""
            if len(dt_part) >= 15 and 'T' in dt_part:
                time_part = dt_part[9:15]
                time_formatted = f"{time_part[:2]}:{time_part[2:4]}"
            
            return {
                'date': formatted_date,
                'time': time_formatted,
                'is_today': is_today,
                'tzid': tzid
            }
        else:
            return {'date': dt_str, 'time': '', 'is_today': False, 'tzid': tzid}
    except Exception:
        return {'date': dt_str, 'time': '', 'is_today': False, 'tzid': tzid}

def download_attachment(client, inbox_id, message_id, attachment_id):
    """Download attachment using AgentMail SDK"""
    try:
        # Use SDK method to get attachment
        result = client.inboxes.messages.get_attachment(
            inbox_id=inbox_id,
            message_id=message_id,
            attachment_id=attachment_id
        )
        
        if hasattr(result, 'download_url') and result.download_url:
            # Download actual file content
            file_response = requests.get(result.download_url, timeout=30)
            file_response.raise_for_status()
            return file_response.text
        else:
            print(f"⚠️ No download_url in attachment response")
            return None
    except Exception as e:
        print(f"⚠️ Error downloading attachment: {e}")
        return None

def parse_calendar_invites():
    """Check AgentMail for calendar invites with .ics attachments"""
    INBOX_ID = "sageai.harris@agentmail.to"
    
    try:
        api_key = load_api_key()
        client = agentmail.AgentMail(api_key=api_key)
        
        # Get recent messages from AgentMail
        response = client.inboxes.messages.list(inbox_id=INBOX_ID, limit=50)
        messages = response.messages if hasattr(response, 'messages') else []
        
        events = []
        
        for msg in messages:
            # Check if this is a calendar invite (subject contains "invited you")
            subject = msg.subject or ''
            if 'invited you' not in subject.lower():
                continue
            
            print(f"\n📧 Processing: {subject}")
            
            # Check for .ics attachments (already included in list response)
            if hasattr(msg, 'attachments') and msg.attachments:
                for attachment in msg.attachments:
                    filename = attachment.filename or ''
                    if filename.endswith('.ics'):
                        print(f"   Found .ics: {filename}")
                        
                        # Download the .ics file using SDK
                        message_id = msg.message_id
                        attachment_id = attachment.attachment_id
                        
                        if message_id and attachment_id:
                            ics_text = download_attachment(client, INBOX_ID, message_id, attachment_id)
                            
                            if ics_text:
                                # Parse the ICS content
                                event_info = {
                                    'summary': '',
                                    'start': '',
                                    'end': '',
                                    'location': '',
                                    'description': '',
                                    'invite_received': str(msg.created_at) if msg.created_at else '',
                                    'email_id': str(message_id),
                                    'date_formatted': '',
                                    'time_formatted': '',
                                    'end_time_formatted': '',
                                    'is_today': False,
                                    'tzid': ''
                                }
                                
                                found_main_start = False
                                found_main_end = False
                                
                                for line in ics_text.split('\r\n'):
                                    if line.startswith('SUMMARY:'):
                                        event_info['summary'] = line[8:].strip()
                                    elif line.startswith('DTSTART;TZID=') and not found_main_start:
                                        match = re.match(r'DTSTART;TZID=([^:]+):(.+)', line)
                                        if match:
                                            tzid = match.group(1)
                                            dt_str = match.group(2)
                                            event_info['start'] = dt_str
                                            event_info['tzid'] = tzid
                                            parsed = parse_ics_datetime(dt_str, tzid)
                                            if parsed:
                                                event_info['date_formatted'] = parsed['date']
                                                event_info['time_formatted'] = parsed['time']
                                                event_info['is_today'] = parsed['is_today']
                                            found_main_start = True
                                    elif line.startswith('DTEND;TZID=') and not found_main_end:
                                        match = re.match(r'DTEND;TZID=([^:]+):(.+)', line)
                                        if match:
                                            dt_str = match.group(2)
                                            event_info['end'] = dt_str
                                            parsed = parse_ics_datetime(dt_str)
                                            if parsed:
                                                event_info['end_time_formatted'] = parsed['time']
                                            found_main_end = True
                                    elif line.startswith('DTSTART:') and not found_main_start:
                                        dt_str = line[8:].strip()
                                        if len(dt_str) >= 8:
                                            year = int(dt_str[:4])
                                            if year >= 2024:
                                                event_info['start'] = dt_str
                                                parsed = parse_ics_datetime(dt_str)
                                                if parsed:
                                                    event_info['date_formatted'] = parsed['date']
                                                    event_info['time_formatted'] = parsed['time']
                                                    event_info['is_today'] = parsed['is_today']
                                                found_main_start = True
                                    elif line.startswith('DTEND:') and not found_main_end:
                                        dt_str = line[6:].strip()
                                        if len(dt_str) >= 8:
                                            year = int(dt_str[:4])
                                            if year >= 2024:
                                                event_info['end'] = dt_str
                                                parsed = parse_ics_datetime(dt_str)
                                                if parsed:
                                                    event_info['end_time_formatted'] = parsed['time']
                                                found_main_end = True
                                    elif line.startswith('LOCATION:'):
                                        event_info['location'] = line[9:].strip()
                                    elif line.startswith('DESCRIPTION:'):
                                        event_info['description'] = line[12:].strip()
                                
                                if event_info['summary'] and event_info['date_formatted']:
                                    events.append(event_info)
                                    print(f"   ✅ Added: {event_info['summary']} on {event_info['date_formatted']}")
                            else:
                                print(f"   ⚠️ Could not download .ics content")
                        else:
                            print(f"   ⚠️ Missing message_id or attachment_id")
            else:
                print(f"   ℹ️ No attachments in message")
        
        # Save to calendar file
        calendar_dir = os.path.expanduser("~/.openclaw/workspace/calendar")
        os.makedirs(calendar_dir, exist_ok=True)
        
        calendar_file = os.path.join(calendar_dir, "events.json")
        with open(calendar_file, 'w') as f:
            json.dump(events, f, indent=2)
        
        print(f"\n✅ Updated calendar with {len(events)} events")
        return events
        
    except Exception as e:
        print(f"❌ Error checking AgentMail: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    parse_calendar_invites()
