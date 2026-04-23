#!/usr/bin/env python3
"""
Auto-verify and send morning briefing at 6:00 AM
Checks draft, fixes issues, sends without human intervention
"""
import json
import os
import subprocess
from datetime import datetime

def auto_verify_and_send():
    verify_file = '/home/groot13-pi/.openclaw/morning_briefing_verify.json'
    
    # Check if draft exists
    if not os.path.exists(verify_file):
        print("❌ No draft found")
        return False
    
    with open(verify_file, 'r') as f:
        data = json.load(f)
    
    # Check if already sent
    if data.get('status') == 'SENT':
        print("✅ Already sent")
        return True
    
    # Verify data quality
    issues = []
    
    # Check weather
    if not data.get('weather') or data.get('weather') == 'unavailable':
        issues.append("Weather missing")
    
    # Check if weather is placeholder
    weather_str = str(data.get('weather', ''))
    if 'unavailable' in weather_str.lower() or 'placeholder' in weather_str.lower():
        issues.append("Weather is placeholder")
    
    # Check news
    if data.get('news_count', 0) < 3:
        issues.append(f"Only {data.get('news_count')} news articles")
    
    # If issues found, try to fix
    if issues:
        print(f"⚠️ Issues found: {', '.join(issues)}")
        print("🔄 Attempting to fix...")
        
        # Try to refresh weather
        if 'Weather' in ' '.join(issues):
            try:
                subprocess.run(['python3', '/home/groot13-pi/.openclaw/fetch_weather.py'], 
                             timeout=30, capture_output=True)
                print("  Refreshed weather")
            except:
                pass
        
        # Try to collect more news
        if 'news' in ' '.join(issues).lower():
            try:
                subprocess.run(['python3', '/home/groot13-pi/.openclaw/collect_rss_news.py'],
                             timeout=60, capture_output=True)
                print("  Refreshed news")
            except:
                pass
    
    # Re-check after fixes
    with open(verify_file, 'r') as f:
        data = json.load(f)
    
    # Determine if sendable
    weather_ok = data.get('weather') and 'unavailable' not in str(data.get('weather', '')).lower()
    news_ok = data.get('news_count', 0) >= 3
    
    if weather_ok and news_ok:
        print("✅ Verification passed - sending")
        result = subprocess.run(['python3', '/home/groot13-pi/.openclaw/send_morning_agentmail.py', '--send-verified'],
                              capture_output=True, text=True, timeout=60)
        if 'sent successfully' in result.stdout:
            print("✅ Sent successfully")
            return True
        else:
            print(f"❌ Send failed: {result.stdout}")
            return False
    else:
        print(f"❌ Still has issues after fix attempt:")
        if not weather_ok:
            print("  - Weather unavailable")
        if not news_ok:
            print(f"  - Only {data.get('news_count', 0)} news articles")
        return False

if __name__ == '__main__':
    print(f"🌅 Auto-verify morning briefing at {datetime.now()}")
    success = auto_verify_and_send()
    print(f"Result: {'✅ Sent' if success else '❌ Failed'}")
