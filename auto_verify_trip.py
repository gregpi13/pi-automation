#!/usr/bin/env python3
"""
Auto-verify and send trip briefing at 8:10 AM
Checks draft, fixes issues, sends without human intervention
"""
import json
import os
import subprocess
from datetime import datetime

def auto_verify_and_send():
    verify_file = '/home/groot13-pi/.openclaw/trip_briefing_verify.json'
    
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
    if not data.get('weather') or 'unavailable' in str(data.get('weather', '')).lower():
        issues.append("Weather missing")
    
    # Check hotel
    if not data.get('hotel'):
        issues.append("Hotel missing")
    
    # If issues found, try to fix
    if issues:
        print(f"⚠️ Issues found: {', '.join(issues)}")
        print("🔄 Attempting to fix...")
        
        # Try to refresh
        try:
            subprocess.run(['python3', '/home/groot13-pi/.openclaw/trip_briefing.py'],
                         timeout=60, capture_output=True)
            print("  Refreshed trip briefing")
        except:
            pass
    
    # Re-check after fixes
    with open(verify_file, 'r') as f:
        data = json.load(f)
    
    # Determine if sendable
    weather_ok = data.get('weather') and 'unavailable' not in str(data.get('weather', '')).lower()
    hotel_ok = bool(data.get('hotel'))
    
    if weather_ok and hotel_ok:
        print("✅ Verification passed - sending")
        result = subprocess.run(['python3', '/home/groot13-pi/.openclaw/trip_briefing.py', '--send-verified'],
                              capture_output=True, text=True, timeout=60)
        if 'sent successfully' in result.stdout or 'Sent to' in result.stdout:
            print("✅ Sent successfully")
            return True
        else:
            print(f"❌ Send failed: {result.stdout}")
            return False
    else:
        print(f"❌ Still has issues after fix attempt:")
        if not weather_ok:
            print("  - Weather unavailable")
        if not hotel_ok:
            print("  - Hotel missing")
        return False

if __name__ == '__main__':
    print(f"🗼 Auto-verify trip briefing at {datetime.now()}")
    success = auto_verify_and_send()
    print(f"Result: {'✅ Sent' if success else '❌ Failed'}")
