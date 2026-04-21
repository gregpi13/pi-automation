#!/usr/bin/env python3
"""
Daily Tokyo Trip Briefing Email System
Sends personalized daily emails based on CSV itinerary
Runs at 8:00 AM Toronto time during trip
"""

import csv
import datetime
import requests
import os
import sys

# Add path for imports
sys.path.insert(0, '/home/groot13-pi/.openclaw')

from health_checks import check_ollama, check_agentmail, check_disk_space

def load_itinerary(csv_path='/home/groot13-pi/.openclaw/trip_itinerary.csv'):
    """Load trip itinerary from CSV"""
    itinerary = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
            reader = csv.DictReader(f)
            for row in reader:
                # Find the date column (handles BOM)
                date_key = None
                for key in row.keys():
                    if 'date' in key.lower():
                        date_key = key
                        break
                
                if not date_key:
                    continue
                    
                date_str = row.get(date_key, '').strip()
                if date_str and len(date_str) > 5:  # Skip empty rows
                    # Parse date (format: 20-Apr-26)
                    try:
                        parts = date_str.split('-')
                        if len(parts) == 3:
                            day = int(parts[0])
                            month_str = parts[1].lower()
                            year = int('20' + parts[2])
                            
                            month_map = {
                                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
                                'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
                                'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                            }
                            month = month_map.get(month_str, 4)
                            
                            date_iso = f"{year:04d}-{month:02d}-{day:02d}"
                            
                            # Parse emails (comma-separated)
                            emails_raw = row.get('Person to email', '')
                            emails = [e.strip() for e in emails_raw.split(',') if e.strip()]
                            
                            # Find other columns (handle BOM)
                            travel_col = [k for k in row.keys() if 'travel' in k.lower()][0] if any('travel' in k.lower() for k in row.keys()) else 'Method of travel'
                            hotel_col = [k for k in row.keys() if 'hotel' in k.lower()][0] if any('hotel' in k.lower() for k in row.keys()) else 'Hotel'
                            events_col = [k for k in row.keys() if 'event' in k.lower()][0] if any('event' in k.lower() for k in row.keys()) else 'Daily Events'
                            
                            itinerary[date_iso] = {
                                'date': date_str,
                                'travel': row.get(travel_col, '').strip(),
                                'hotel': row.get(hotel_col, '').strip(),
                                'events': row.get(events_col, '').strip(),
                                'emails': emails
                            }
                    except Exception as e:
                        print(f"Skipping row with date {date_str}: {e}")
                        continue
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}
    
    return itinerary

def get_tokyo_weather():
    """Get current weather for Tokyo"""
    try:
        # Using Open-Meteo API (no key needed)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': 35.6895,
            'longitude': 139.6917,
            'current': 'temperature_2m,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
            'timezone': 'Asia/Tokyo'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            temp = current.get('temperature_2m', 'N/A')
            weather_code = current.get('weather_code', 0)
            
            # Simple weather code mapping
            weather_map = {
                0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
                45: 'Foggy', 48: 'Depositing rime fog',
                51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
                61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
                71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
                95: 'Thunderstorm'
            }
            
            condition = weather_map.get(weather_code, 'Unknown')
            
            return {
                'temp': temp,
                'condition': condition,
                'high': daily.get('temperature_2m_max', ['N/A'])[0] if daily.get('temperature_2m_max') else 'N/A',
                'low': daily.get('temperature_2m_min', ['N/A'])[0] if daily.get('temperature_2m_min') else 'N/A',
                'precip': daily.get('precipitation_probability_max', ['0%'])[0] if daily.get('precipitation_probability_max') else '0%'
            }
    except Exception as e:
        print(f"Weather fetch error: {e}")
    
    return {'temp': 'N/A', 'condition': 'Unavailable', 'high': 'N/A', 'low': 'N/A', 'precip': 'N/A'}

def generate_html_briefing(date_str, day_data, weather):
    """Generate HTML email for a specific day"""
    
    # Build tiles based on available data
    tiles = []
    
    # Weather tile (always present)
    tiles.append(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; margin: 15px 0; color: white;">
        <h3 style="margin-top: 0;">🌤️ Tokyo Weather Today</h3>
        <p style="font-size: 24px; margin: 5px 0;"><strong>{weather['temp']}°C</strong> - {weather['condition']}</p>
        <p style="margin: 5px 0;">High: {weather['high']}°C | Low: {weather['low']}°C</p>
        <p style="margin: 5px 0;">Precipitation: {weather['precip']}%</p>
    </div>
    """)
    
    # Travel tile (only if travel data exists)
    if day_data.get('travel'):
        tiles.append(f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #28a745;">
        <h3 style="margin-top: 0; color: #28a745;">✈️ Travel Today</h3>
        <p style="font-size: 18px; margin: 5px 0;"><strong>{day_data['travel']}</strong></p>
    </div>
    """)
    
    # Hotel tile (only if hotel data exists)
    if day_data.get('hotel'):
        tiles.append(f"""
    <div style="background: #fff3cd; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #ffc107;">
        <h3 style="margin-top: 0; color: #856404;">🏨 Accommodation</h3>
        <p style="font-size: 18px; margin: 5px 0;"><strong>{day_data['hotel']}</strong></p>
    </div>
    """)
    
    # Events tile (only if events data exists)
    if day_data.get('events'):
        tiles.append(f"""
    <div style="background: #d1ecf1; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #17a2b8;">
        <h3 style="margin-top: 0; color: #0c5460;">📍 Today's Activities</h3>
        <p style="font-size: 18px; margin: 5px 0;"><strong>{day_data['events']}</strong></p>
    </div>
    """)
    
    # Email recipients tile
    if day_data.get('emails'):
        email_list = ', '.join(day_data['emails'])
        tiles.append(f"""
    <div style="background: #e2e3e5; padding: 15px; border-radius: 12px; margin: 15px 0; font-size: 14px;">
        <strong>📧 This briefing sent to:</strong> {email_list}
    </div>
    """)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>🗼 Tokyo Trip</h1>
    <h2 style="text-align: center; color: #7f8c8d;">{date_str}</h2>
    
    {''.join(tiles)}
    
    <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center; color: #6c757d; font-size: 14px;">
        <p>Have an amazing day in Japan! 🇯🇵</p>
        <p><em>— Your travel briefing from Sage 🌿</em></p>
    </div>
</body>
</html>"""
    
    return html

def send_trip_briefing():
    """Main function to send daily trip briefing - TWO STEP PROCESS"""
    from agentmail import AgentMail
    import json
    
    # Get today's date
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # CHECK: Was briefing already sent today?
    verify_file = '/home/groot13-pi/.openclaw/trip_briefing_verify.json'
    if os.path.exists(verify_file):
        try:
            with open(verify_file, 'r') as f:
                existing = json.load(f)
            if existing.get('date') == today and existing.get('status') == 'SENT':
                sent_time = existing.get('sent_time', 'unknown')
                print(f"ℹ️ Trip briefing for {today} was already sent at {sent_time}")
                print(f"   Skipping duplicate. Run with --force to override.")
                return True
        except:
            pass  # Continue if file is corrupted
    
    # Load itinerary
    itinerary = load_itinerary()
    if not itinerary:
        print("❌ No itinerary data found")
        return False
    
    # Check if today is in itinerary
    if today not in itinerary:
        print(f"ℹ️ No trip data for {today}")
        return True  # Not an error, just no trip today
    
    day_data = itinerary[today]
    
    # Get weather with retry
    print(f"🌤️ Fetching weather for {today}...")
    weather = None
    for attempt in range(3):  # 3 attempts
        weather = get_tokyo_weather()
        if weather['temp'] != 'N/A' and weather['condition'] != 'Unavailable':
            print(f"   ✓ Weather: {weather['temp']}°C, {weather['condition']}")
            break
        print(f"   ⚠️ Attempt {attempt+1} failed, retrying...")
        import time
        time.sleep(2)
    
    # Check weather status
    if not weather or weather['temp'] == 'N/A':
        weather_status = "❌ FAILED"
        print("❌ Could not fetch weather after retries")
    else:
        weather_status = f"✅ {weather['temp']}°C"
    
    # Generate HTML
    print(f"📄 Generating briefing for {day_data['date']}...")
    html_content = generate_html_briefing(day_data['date'], day_data, weather)
    
    # Save draft
    draft_file = f'/home/groot13-pi/.openclaw/trip_briefing_draft_{today}.html'
    with open(draft_file, 'w') as f:
        f.write(html_content)
    print(f"💾 Draft saved to: {draft_file}")
    
    # Create verification file
    verify_file = '/home/groot13-pi/.openclaw/trip_briefing_verify.json'
    verify_data = {
        'date': today,
        'trip_date': day_data['date'],
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'draft_file': draft_file,
        'weather': weather_status,
        'weather_data': weather,
        'emails': day_data.get('emails', []),
        'travel': day_data.get('travel', ''),
        'hotel': day_data.get('hotel', ''),
        'events': day_data.get('events', ''),
        'status': 'PENDING_VERIFICATION',
        'issues': [] if weather and weather['temp'] != 'N/A' else ['Weather API failed - check manually']
    }
    with open(verify_file, 'w') as f:
        json.dump(verify_data, f, indent=2)
    print(f"📋 Verification file: {verify_file}")
    
    # Notify Sage
    print(f"\n📱 Notifying Sage via Telegram...")
    try:
        import subprocess
        subprocess.run(['python3', '/home/groot13-pi/.openclaw/notify_trip_briefing.py'], 
                      timeout=30, capture_output=True)
        print(f"✅ Sage notified")
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")
    
    print(f"\n✅ Draft ready. Sage will verify and send.")
    print(f"   Weather: {weather_status}")
    print(f"   Emails: {len(day_data.get('emails', []))} recipients")
    print(f"   Run: trip_briefing.py --send-verified\n")
    
    return True

def send_verified_trip_briefing():
    """Send the verified trip briefing (called by Sage after verification)"""
    from agentmail import AgentMail
    import json
    
    verify_file = '/home/groot13-pi/.openclaw/trip_briefing_verify.json'
    
    # Check if verification file exists
    if not os.path.exists(verify_file):
        print("❌ No verification file found. Run send_trip_briefing() first.")
        return False
    
    # Load verification data
    with open(verify_file, 'r') as f:
        verify_data = json.load(f)
    
    # Check if already sent
    if verify_data.get('status') == 'SENT':
        print(f"⚠️ Briefing already sent at {verify_data.get('sent_time', 'unknown')}")
        return False
    
    # Get the draft file
    draft_file = verify_data.get('draft_file')
    if not draft_file or not os.path.exists(draft_file):
        print(f"❌ Draft file not found: {draft_file}")
        return False
    
    # Read the HTML
    with open(draft_file, 'r') as f:
        html_content = f.read()
    
    # Get recipients
    emails = verify_data.get('emails', [])
    if not emails:
        print("⚠️ No email recipients")
        return False
    
    # Send via AgentMail
    print(f"\n{'='*50}")
    print(f"🗼 SENDING VERIFIED TRIP BRIEFING")
    print(f"{'='*50}\n")
    print(f"Date: {verify_data['trip_date']}")
    print(f"Weather: {verify_data['weather']}")
    print(f"Recipients: {len(emails)}\n")
    
    try:
        with open('/home/groot13-pi/.openclaw/secure/agentmail-api-key', 'r') as f:
            api_key = f.read().strip()
        
        client = AgentMail(api_key=api_key)
        
        for email in emails:
            print(f"📧 Sending to {email}...")
            response = client.inboxes.messages.send(
                inbox_id='sageai.harris@agentmail.to',
                to=email,
                subject=f'🗼 Tokyo Trip Briefing - {verify_data["trip_date"]}',
                html=html_content
            )
            print(f"✅ Sent to {email}")
        
        # Mark as sent
        verify_data['status'] = 'SENT'
        verify_data['sent_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(verify_file, 'w') as f:
            json.dump(verify_data, f, indent=2)
        
        print(f"\n✅ Trip briefing sent and logged.")
        return True
        
    except Exception as e:
        print(f"❌ Error sending emails: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--send-verified':
        # Send the verified briefing
        send_verified_trip_briefing()
    else:
        # Create draft (default behavior)
        print(f"🚀 Tokyo Trip Briefing System")
        print(f"📅 Today: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print("-" * 50)
        
        success = send_trip_briefing()
        sys.exit(0 if success else 1)
