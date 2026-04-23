#!/usr/bin/env python3
"""
1 AM TeamLab Calendar Check
Scans for July 2026 ticket availability
Runs daily at 1:00 AM
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def check_teamlab_calendar():
    """Check TeamLab calendar for July dates"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(
            'https://teamlabplanets.dmm.com/en/ticket/admission_date/55efba2e24517ee07f1466ac42bb05d5',
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            return {'status': 'error', 'message': f'HTTP {response.status_code}'}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for July indicators
        july_found = 'July' in response.text or '2026-07' in response.text
        
        # Look for calendar cells with specific classes
        # Red triangle = limited, Circle = available, X = sold out
        calendar_cells = soup.find_all(['td', 'div'], class_=lambda x: x and any(
            term in str(x).lower() for term in ['calendar', 'date', 'day']
        ))
        
        # Check for availability indicators
        indicators = {
            'red_triangle': len(soup.find_all(class_=lambda x: x and 'triangle' in str(x).lower())),
            'circle': len(soup.find_all(class_=lambda x: x and 'circle' in str(x).lower())),
            'x_mark': len(soup.find_all(class_=lambda x: x and 'x' in str(x).lower())),
            'available': 'available' in response.text.lower(),
            'sold_out': 'sold out' in response.text.lower()
        }
        
        # Look for specific July dates
        july_dates = []
        for cell in calendar_cells:
            text = cell.get_text(strip=True)
            if '7/' in text or '07/' in text:
                july_dates.append(text)
        
        # Determine status
        if july_found or len(july_dates) > 0:
            status = 'july_available'
        else:
            status = 'not_yet'
        
        # Save result
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'july_found': july_found,
            'july_dates_count': len(july_dates),
            'indicators': indicators,
            'sample_dates': july_dates[:5] if july_dates else []
        }
        
        # Save to file for morning check
        result_file = '/home/groot13-pi/.openclaw/teamlab_check_result.json'
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    result = check_teamlab_calendar()
    print(f"TeamLab Check: {result['status']}")
    if result['status'] == 'july_available':
        print("🎉 July tickets are available!")
    elif result['status'] == 'not_yet':
        print("⏳ July tickets not yet released")
    else:
        print(f"❌ Error: {result.get('message', 'Unknown')}")
