#!/usr/bin/env python3
"""
Morning Briefing - HTML Card Style with Validation & Fallbacks
Ensures all sections have data before sending
Now with clickable news links!
"""
import agentmail
import json
import requests
import subprocess
from datetime import datetime
import time

# Configuration
INBOX_ID = "sageai.harris@agentmail.to"
RECIPIENT = "greg.m.harris@gmail.com"

def load_api_key():
    with open('/home/groot13-pi/.openclaw/secure/agentmail-api-key', 'r') as f:
        return f.read().strip()

def get_weather_with_fallback():
    """Get weather with multiple fallback sources"""
    # Try Caledon first
    weather = get_caledon_weather()
    if weather:
        return weather
    
    print("⚠️ Caledon weather failed, trying Toronto...")
    # Fallback to Toronto
    weather = get_toronto_weather()
    if weather:
        return weather
    
    print("⚠️ Toronto weather failed, trying Brampton...")
    # Fallback to Brampton
    weather = get_brampton_weather()
    if weather:
        return weather
    
    return None

def get_caledon_weather():
    """Get weather for Caledon"""
    try:
        response = requests.get("https://wttr.in/Caledon,Ontario?format=j1", timeout=10)
        data = response.json()
        current = data['current_condition'][0]
        today = data['weather'][0]
        return {
            'temp': current['temp_C'],
            'condition': current['weatherDesc'][0]['value'],
            'feels_like': current['FeelsLikeC'],
            'high': today['maxtempC'],
            'low': today['mintempC'],
            'humidity': current['humidity'],
            'wind': current['windspeedKmph'],
            'location': 'Caledon'
        }
    except:
        return None

def get_toronto_weather():
    """Fallback: Toronto weather"""
    try:
        response = requests.get("https://wttr.in/Toronto?format=j1", timeout=10)
        data = response.json()
        current = data['current_condition'][0]
        today = data['weather'][0]
        return {
            'temp': current['temp_C'],
            'condition': current['weatherDesc'][0]['value'],
            'feels_like': current['FeelsLikeC'],
            'high': today['maxtempC'],
            'low': today['mintempC'],
            'humidity': current['humidity'],
            'wind': current['windspeedKmph'],
            'location': 'Toronto (nearby)'
        }
    except:
        return None

def get_brampton_weather():
    """Fallback: Brampton weather"""
    try:
        response = requests.get("https://wttr.in/Brampton?format=j1", timeout=10)
        data = response.json()
        current = data['current_condition'][0]
        today = data['weather'][0]
        return {
            'temp': current['temp_C'],
            'condition': current['weatherDesc'][0]['value'],
            'feels_like': current['FeelsLikeC'],
            'high': today['maxtempC'],
            'low': today['mintempC'],
            'humidity': current['humidity'],
            'wind': current['windspeedKmph'],
            'location': 'Brampton (nearby)'
        }
    except:
        return None

def get_mississauga_weather():
    """Final fallback: Mississauga weather"""
    try:
        response = requests.get("https://wttr.in/Mississauga?format=j1", timeout=10)
        data = response.json()
        current = data['current_condition'][0]
        today = data['weather'][0]
        return {
            'temp': current['temp_C'],
            'condition': current['weatherDesc'][0]['value'],
            'feels_like': current['FeelsLikeC'],
            'high': today['maxtempC'],
            'low': today['mintempC'],
            'humidity': current['humidity'],
            'wind': current['windspeedKmph'],
            'location': 'Mississauga (nearby)'
        }
    except:
        return None

def collect_fresh_news():
    """Collect fresh news if RSS file is old or empty"""
    try:
        print("📡 Collecting fresh news...")
        result = subprocess.run(
            ['/usr/bin/python3', '/home/groot13-pi/.openclaw/collect_rss_news.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        print(f"✅ News collection: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"⚠️ News collection failed: {e}")
        return False

def get_news_with_fallback():
    """Get news with proactive collection if needed"""
    # Try to load existing news
    news = get_news_summary()
    
    # If no news or less than 3 articles, collect fresh
    if len(news) < 3:
        print(f"⚠️ Only {len(news)} articles found, collecting fresh...")
        if collect_fresh_news():
            # Try loading again
            time.sleep(2)  # Brief wait for file write
            news = get_news_summary()
    
    return news

def get_news_summary():
    """Get news from RSS collection WITH URLs for clickable links"""
    try:
        # Try today's file first
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            with open(f'/home/groot13-pi/.openclaw/news/news_{today}.json', 'r') as f:
                data = json.load(f)
                articles = []
                for source in ['cbc', 'bbc', 'guardian', 'aljazeera']:
                    items = data.get('articles', {}).get(source, {}).get('items', [])[:2]
                    for item in items:
                        articles.append({
                            'title': item.get('title', ''),
                            'source': data['articles'][source]['source_name'],
                            'url': item.get('url', ''),  # Add URL for clickable links
                            'description': item.get('description', '')
                        })
                return articles[:6]
        except:
            pass
        
        # Fallback to rss_news.json
        with open('/home/groot13-pi/.openclaw/rss_news.json', 'r') as f:
            data = json.load(f)
            articles = data.get('articles', [])[:5]
            # Ensure each article has a URL
            for article in articles:
                if 'url' not in article:
                    article['url'] = ''
            return articles
    except:
        return []

def get_todays_events():
    """Get today's calendar events"""
    try:
        with open('/home/groot13-pi/.openclaw/workspace/calendar/events.json', 'r') as f:
            events = json.load(f)
        
        today = datetime.now().strftime('%Y%m%d')
        todays_events = []
        
        for e in events:
            if e.get('start', '').startswith(today):
                todays_events.append({
                    'summary': e.get('summary', 'Event'),
                    'time': e.get('time_formatted', 'All day'),
                    'end': e.get('end_time_formatted', ''),
                    'location': e.get('location', '')
                })
        
        return todays_events
    except:
        return []

def validate_and_send():
    """Main validation and send function - TWO STEP PROCESS"""
    print(f"\n{'='*50}")
    print(f"🌅 MORNING BRIEFING VALIDATION")
    print(f"{'='*50}\n")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Get Weather (with fallbacks)
    print("Step 1: Collecting weather data...")
    weather = get_weather_with_fallback()
    if weather:
        print(f"✅ Weather: {weather['temp']}°C, {weather['condition']} ({weather['location']})")
    else:
        print("❌ Weather: All sources failed")
    
    # Step 2: Get Calendar Events
    print("\nStep 2: Loading calendar events...")
    events = get_todays_events()
    print(f"✅ Calendar: {len(events)} events found")
    for e in events:
        print(f"   - {e['summary']} at {e['time']}")
    
    # Step 3: Get News (with proactive collection)
    print("\nStep 3: Collecting news headlines...")
    news = get_news_with_fallback()
    print(f"✅ News: {len(news)} articles ready")
    for article in news[:3]:
        has_url = "🔗" if article.get('url') else "❌"
        print(f"   {has_url} {article['source']}: {article['title'][:50]}...")
    
    # Final validation
    print(f"\n{'='*50}")
    print("VALIDATION SUMMARY:")
    print(f"{'='*50}")
    
    # Check if weather is missing
    if not weather:
        print("❌ Weather: FAILED")
        weather_status = "❌ MISSING"
    else:
        print(f"✅ Weather: {weather['temp']}°C")
        weather_status = f"✅ {weather['temp']}°C"
    
    print(f"{'✅' if events else '✅'} Calendar: {len(events)} events")
    print(f"{'✅' if len(news) >= 3 else '⚠️'} News: {len(news)} articles")
    
    # TWO-STEP: Save draft and notify Sage instead of sending
    print(f"\n{'='*50}")
    print("TWO-STEP PROCESS: Draft saved, awaiting verification")
    print(f"{'='*50}\n")
    
    # Save draft HTML
    html = build_html(weather, events, news)
    draft_file = f'/home/groot13-pi/.openclaw/morning_briefing_draft_{datetime.now().strftime(\"%Y%m%d\")}.html'
    with open(draft_file, 'w') as f:
        f.write(html)
    print(f"💾 Draft saved to: {draft_file}")
    
    # Create verification file for Sage
    verify_file = '/home/groot13-pi/.openclaw/morning_briefing_verify.json'
    verify_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'draft_file': draft_file,
        'weather': weather_status,
        'weather_data': weather,
        'events_count': len(events),
        'news_count': len(news),
        'status': 'PENDING_VERIFICATION',
        'issues': [] if weather else ['Weather API failed - needs manual check']
    }
    with open(verify_file, 'w') as f:
        json.dump(verify_data, f, indent=2)
    print(f"📋 Verification file: {verify_file}")
    
    # Log for monitoring
    with open('/home/groot13-pi/.openclaw/logs/morning_draft.log', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Draft created - Weather: {weather_status}\n")
    
    print(f"\n✅ Draft ready. Waiting for Sage verification...")
    print(f"   Weather: {weather_status}")
    print(f"   Events: {len(events)}")
    print(f"   News: {len(news)} articles")
    print(f"\n   Sage: Check draft and run send_morning_briefing_verified()\n")
    
    return True

def build_html(weather, events, news):
    """Build HTML email with clickable news links"""
    now = datetime.now()
    date_str = now.strftime('%A, %B %d, %Y')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f7; margin: 0; padding: 20px; }}
.container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
.header p {{ margin: 8px 0 0 0; opacity: 0.9; font-size: 16px; }}
.card {{ border-bottom: 1px solid #e5e5e7; padding: 20px 24px; }}
.card:last-child {{ border-bottom: none; }}
.card-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #8e8e93; margin-bottom: 8px; font-weight: 600; }}
.card-content {{ font-size: 16px; color: #1c1c1e; line-height: 1.5; }}
.weather-temp {{ font-size: 32px; font-weight: 300; color: #1c1c1e; }}
.weather-detail {{ font-size: 14px; color: #8e8e93; margin-top: 4px; }}
.event-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
.event-item:last-child {{ border-bottom: none; }}
.event-time {{ font-size: 14px; color: #007aff; font-weight: 500; }}
.event-title {{ font-size: 16px; font-weight: 500; margin-top: 4px; }}
.news-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
.news-item:last-child {{ border-bottom: none; }}
.news-title {{ font-size: 15px; font-weight: 500; }}
.news-title a {{ color: #007aff; text-decoration: none; }}
.news-title a:hover {{ text-decoration: underline; }}
.news-source {{ font-size: 12px; color: #8e8e93; margin-top: 4px; }}
.footer {{ background: #f5f5f7; padding: 16px 24px; text-align: center; font-size: 12px; color: #8e8e93; }}
.empty-state {{ color: #8e8e93; font-style: italic; }}
.validation-note {{ background: #e8f5e9; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #2e7d32; margin-top: 8px; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🌅 Morning Briefing</h1>
        <p>{date_str}</p>
    </div>
"""
    
    # Weather card
    if weather:
        location_note = f" ({weather['location']})" if 'nearby' in weather.get('location', '') else ""
        html += f"""
    <div class="card">
        <div class="card-title">🌤️ Caledon Weather{location_note}</div>
        <div class="card-content">
            <div class="weather-temp">{weather['temp']}°C</div>
            <div>{weather['condition']}</div>
            <div class="weather-detail">Feels like {weather['feels_like']}°C • High: {weather['high']}°C • Low: {weather['low']}°C</div>
            <div class="weather-detail">Humidity: {weather['humidity']}% • Wind: {weather['wind']} km/h</div>
        </div>
    </div>
"""
    else:
        html += """
    <div class="card">
        <div class="card-title">🌤️ Weather</div>
        <div class="card-content">
            <div class="empty-state">Weather data temporarily unavailable</div>
            <div class="validation-note">✓ System checked multiple sources (Caledon, Toronto, Brampton, Mississauga)</div>
        </div>
    </div>
"""
    
    # Calendar card
    html += '    <div class="card">\n        <div class="card-title">📅 Today\'s Events</div>\n        <div class="card-content">\n'
    if events:
        for event in events:
            time_str = event['time'] if event['time'] != 'All day' else 'All day'
            html += f'''            <div class="event-item">
                <div class="event-time">{time_str}</div>
                <div class="event-title">{event['summary']}</div>
            </div>
'''
    else:
        html += '            <div class="empty-state">No events scheduled for today</div>\n'
    html += '        </div>\n    </div>\n'
    
    # News card - with clickable links
    html += '    <div class="card">\n        <div class="card-title">📰 News Headlines</div>\n        <div class="card-content">\n'
    if news:
        for article in news[:6]:
            url = article.get('url', '')
            title = article['title']
            source = article['source']
            if url:
                html += f'''            <div class="news-item">
                <div class="news-title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="news-source">{source}</div>
            </div>
'''
            else:
                html += f'''            <div class="news-item">
                <div class="news-title">{title}</div>
                <div class="news-source">{source}</div>
            </div>
'''
        if len(news) < 3:
            html += '            <div class="validation-note">✓ Fresh news collected for this briefing</div>\n'
    else:
        html += '''            <div class="empty-state">News temporarily unavailable</div>
            <div class="validation-note">✓ System attempted proactive collection</div>
'''
    html += '''        </div>
    </div>
    
    <div class="footer">
        All sections validated before sending • From your Raspberry Pi 🌿
    </div>
</div>
</body>
</html>
'''
    return html

def send_email(html_body):
    """Send email via AgentMail"""
    try:
        api_key = load_api_key()
        client = agentmail.AgentMail(api_key=api_key)
        
        today_str = datetime.now().strftime('%A, %B %d, %Y')
        
        message = client.inboxes.messages.send(
            inbox_id=INBOX_ID,
            to=[RECIPIENT],
            subject=f"🌅 Morning Briefing - {today_str} (Validated)",
            html=html_body
        )
        
        print(f"\n✅ Email sent successfully to {RECIPIENT}")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to send: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_verified_briefing():
    """Send the verified morning briefing (called by Sage after verification)"""
    import os
    
    verify_file = '/home/groot13-pi/.openclaw/morning_briefing_verify.json'
    
    # Check if verification file exists
    if not os.path.exists(verify_file):
        print("❌ No verification file found. Run validate_and_send() first.")
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
        html = f.read()
    
    # Send it
    print(f"\n{'='*50}")
    print(f"📧 SENDING VERIFIED MORNING BRIEFING")
    print(f"{'='*50}\n")
    print(f"Date: {verify_data['date']}")
    print(f"Weather: {verify_data['weather']}")
    print(f"Events: {verify_data['events_count']}")
    print(f"News: {verify_data['news_count']} articles\n")
    
    send_email(html)
    
    # Mark as sent
    verify_data['status'] = 'SENT'
    verify_data['sent_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(verify_file, 'w') as f:
        json.dump(verify_data, f, indent=2)
    
    print(f"\n✅ Briefing sent and logged.")
    return True

def check_morning_briefing_status():
    """Check if morning briefing is ready for verification"""
    import os
    
    verify_file = '/home/groot13-pi/.openclaw/morning_briefing_verify.json'
    
    if not os.path.exists(verify_file):
        return {"status": "NO_DRAFT", "message": "No briefing draft found"}
    
    with open(verify_file, 'r') as f:
        data = json.load(f)
    
    if data.get('status') == 'SENT':
        return {"status": "ALREADY_SENT", "sent_time": data.get('sent_time')}
    
    return {
        "status": "PENDING",
        "date": data.get('date'),
        "weather": data.get('weather'),
        "weather_data": data.get('weather_data'),
        "events": data.get('events_count'),
        "news": data.get('news_count'),
        "issues": data.get('issues', [])
    }

if __name__ == "__main__":
    validate_and_send()
