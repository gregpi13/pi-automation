#!/usr/bin/env python3
"""
Process Greg's daily weight/workout submissions
Updates tracker.json and PROGRESS_LOG.md
"""
import json
import re
from datetime import datetime
from pathlib import Path

TRACKER_FILE = '/home/groot13-pi/.openclaw/workspace/PROJECTS/weight_loss_tracker/tracker.json'
LOG_FILE = '/home/groot13-pi/.openclaw/workspace/PROJECTS/weight_loss_tracker/PROGRESS_LOG.md'

def parse_entry(text):
    """Parse natural language entry for weight/workout data"""
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'weight': None,
        'workout_completed': False,
        'workout_type': None,
        'duration_minutes': None,
        'notes': None
    }
    
    # Extract weight (e.g., "186.5 lbs", "187 pounds", "186")
    weight_patterns = [
        r'(\d+\.?\d*)\s*(?:lbs?|pounds?)',
        r'weight[:\s]*(\d+\.?\d*)',
    ]
    for pattern in weight_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entry['weight'] = float(match.group(1))
            break
    
    # Check for workout
    if re.search(r'\byes\b|\bdid\s+workout\b|\bworkout[:\s]*yes', text, re.IGNORECASE):
        entry['workout_completed'] = True
        
        # Extract duration (e.g., "30 min", "45 minutes", "1 hour")
        duration_patterns = [
            r'(\d+)\s*(?:min|minute)s?',
            r'(\d+)\s*hr(?:s|ours?)?',
            r'(?:for\s+)?(\d+)\s*(?:min|minute|hour)',
        ]
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entry['duration_minutes'] = int(match.group(1))
                break
        
        # Extract workout type
        workout_types = ['cardio', 'strength', 'weights', 'walk', 'run', 'running', 'bike', 'cycling', 'swim', 'yoga', 'hiit']
        for wt in workout_types:
            if wt in text.lower():
                entry['workout_type'] = wt
                break
    elif re.search(r'\bno\b|\bdidn.?t\s+workout\b|\bskip', text, re.IGNORECASE):
        entry['workout_completed'] = False
    
    # Extract notes (anything after workout info)
    entry['notes'] = text.strip()
    
    return entry

def update_tracker(entry):
    """Update JSON tracker and Markdown log"""
    
    # Load tracker
    with open(TRACKER_FILE, 'r') as f:
        tracker = json.load(f)
    
    # Add entry
    tracker['entries'].append(entry)
    
    # Update current weight if provided
    if entry['weight']:
        tracker['currentWeightLbs'] = entry['weight']
        if not tracker['targetWeightLbs'] and tracker['entries']:
            # Set target based on first entry
            first_weight = tracker['entries'][0]['weight']
            if first_weight:
                tracker['targetWeightLbs'] = first_weight - 10
    
    # Save tracker
    with open(TRACKER_FILE, 'w') as f:
        json.dump(tracker, f, indent=2)
    
    # Update markdown log
    update_markdown_log(tracker, entry)
    
    return tracker

def update_markdown_log(tracker, new_entry):
    """Update the human-readable progress log"""
    
    with open(LOG_FILE, 'r') as f:
        content = f.read()
    
    # Find and update the table row for today
    date_str = new_entry['date']
    
    # Build row data
    weight = f"{new_entry['weight']:.1f}" if new_entry['weight'] else ""
    workout = "✓" if new_entry['workout_completed'] else "✗"
    if new_entry['workout_type']:
        workout = f"{new_entry['workout_type']}"
    duration = f"{new_entry['duration_minutes']} min" if new_entry['duration_minutes'] else ""
    notes = new_entry['notes'] if new_entry['notes'] else ""
    
    # Replace the empty row for this date
    old_row = f"| {date_str} | | | | |"
    new_row = f"| {date_str} | {weight} | {workout} | {duration} | {notes} |"
    
    content = content.replace(old_row, new_row)
    
    # Update summary stats
    entries_with_weight = [e for e in tracker['entries'] if e['weight']]
    if entries_with_weight:
        start_weight = entries_with_weight[0]['weight']
        current_weight = entries_with_weight[-1]['weight']
        total_lost = start_weight - current_weight
        
        content = re.sub(r'\*\*Starting weight:\*\* ___ lbs', f'**Starting weight:** {start_weight:.1f} lbs', content)
        content = re.sub(r'\*\*Current weight:\*\* ___ lbs', f'**Current weight:** {current_weight:.1f} lbs', content)
        content = re.sub(r'\*\*Total weight lost:\*\* ___ lbs', f'**Total weight lost:** {total_lost:.1f} lbs', content)
    
    workouts_done = sum(1 for e in tracker['entries'] if e['workout_completed'])
    content = re.sub(r'\*\*Workouts completed:\*\* ___ / 14', f'**Workouts completed:** {workouts_done} / 14', content)
    
    with open(LOG_FILE, 'w') as f:
        f.write(content)

def generate_progress_summary(tracker):
    """Generate a summary of current progress"""
    entries = tracker['entries']
    
    if not entries:
        return "No entries yet. Get started by replying with your weight and workout info!"
    
    # Calculate stats
    weights = [e['weight'] for e in entries if e['weight']]
    workouts = [e for e in entries if e['workout_completed']]
    
    summary = f"📊 **Progress Summary** (Day {len(entries)}/14)\n\n"
    
    if len(weights) >= 2:
        start = weights[0]
        current = weights[-1]
        lost = start - current
        target = tracker.get('targetWeightLbs', start - 10)
        remaining = target - current if target else None
        
        summary += f"📉 **Weight:** {start:.1f} → {current:.1f} lbs ({lost:.1f} lbs lost)\n"
        if remaining:
            summary += f"🎯 **Target:** {target:.1f} lbs ({remaining:.1f} lbs to go)\n"
    elif weights:
        summary += f"📉 **Current Weight:** {weights[-1]:.1f} lbs\n"
    
    summary += f"💪 **Workouts:** {len(workouts)}/{len(entries)} ({len(workouts)/len(entries)*100:.0f}%)\n"
    
    if workouts:
        avg_duration = sum(e['duration_minutes'] for e in workouts if e['duration_minutes']) / len(workouts)
        summary += f"⏱️ **Avg Duration:** {avg_duration:.0f} min\n"
    
    return summary

if __name__ == '__main__':
    # For testing - can be called with text argument
    import sys
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        entry = parse_entry(text)
        print(f"Parsed: {json.dumps(entry, indent=2)}")
        tracker = update_tracker(entry)
        print(generate_progress_summary(tracker))
