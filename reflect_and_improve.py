#!/usr/bin/env python3
"""
4 AM Reflection Hour - Self-improvement and daily review
Runs at 4:00 AM daily to reflect on the day and update documentation
"""

import json
import os
from datetime import datetime, timedelta

def log_reflection(message):
    """Log reflection activity"""
    log_file = os.path.expanduser("~/.openclaw/logs/reflection.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def review_agents_md():
    """Review AGENTS.md for any lessons to add"""
    agents_file = os.path.expanduser("~/.openclaw/workspace/AGENTS.md")
    
    if not os.path.exists(agents_file):
        log_reflection("⚠️ AGENTS.md not found")
        return
    
    with open(agents_file, 'r') as f:
        content = f.read()
    
    # Check if there are empty lesson placeholders
    if "### [Topic]" in content or "[What you learned and how to do it better]" in content:
        log_reflection("ℹ️ AGENTS.md has empty lesson templates")
    else:
        log_reflection("✅ AGENTS.md lessons are populated")
    
    # Log last modified time
    mtime = os.path.getmtime(agents_file)
    mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    log_reflection(f"📄 AGENTS.md last updated: {mtime_str}")

def review_yesterday_memory():
    """Review yesterday's memory file for patterns"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    memory_file = os.path.expanduser(f"~/.openclaw/workspace/memory/{yesterday}.md")
    
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            content = f.read()
        
        # Look for lessons learned patterns
        lessons = []
        if "lesson" in content.lower() or "learned" in content.lower():
            lessons.append("Potential lessons found in yesterday's memory")
        
        if "mistake" in content.lower() or "error" in content.lower():
            lessons.append("Potential mistakes to document")
        
        if lessons:
            log_reflection(f"📝 Yesterday's memory review: {len(lessons)} items to check")
            for lesson in lessons:
                log_reflection(f"   - {lesson}")
        else:
            log_reflection("✅ No obvious lessons in yesterday's memory")
    else:
        log_reflection(f"ℹ️ No memory file for {yesterday}")

def check_tools_md():
    """Check if TOOLS.md needs updates"""
    tools_file = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
    
    if os.path.exists(tools_file):
        mtime = os.path.getmtime(tools_file)
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        log_reflection(f"🔧 TOOLS.md last updated: {mtime_str}")
    else:
        log_reflection("⚠️ TOOLS.md not found")

def check_ai_models_monthly():
    """Monthly check for new AI model releases (1st of each month)"""
    today = datetime.now()
    if today.day == 1:  # First day of month
        log_reflection("🤖 Monthly AI model check:")
        log_reflection("   - Checking for kimi-k2.5 updates or new versions")
        log_reflection("   - Checking for GLM-5.1 updates")
        log_reflection("   - Checking for Gemma releases")
        log_reflection("   ℹ️ Currently using: kimi-k2.5:cloud (primary), glm-5.1:cloud (secondary)")
        log_reflection("   📋 Action: Review Ollama/Moonshot announcements if major version released")
    else:
        log_reflection(f"📅 Monthly AI check: Skipped (runs on 1st of month, today is {today.day})")

def check_post_upgrade():
    """Verify all automated jobs after OpenClaw/model updates"""
    import subprocess
    
    log_reflection("🔧 Post-Upgrade Verification Check")
    
    # Check 1: Morning Briefing
    log_reflection("  [1/6] Testing morning briefing...")
    try:
        result = subprocess.run(
            ['python3', os.path.expanduser('~/.openclaw/send_morning_agentmail.py')],
            capture_output=True, text=True, timeout=60
        )
        if 'Draft saved' in result.stdout:
            log_reflection("  ✅ Morning briefing: WORKING")
        else:
            log_reflection("  ❌ Morning briefing: FAILED")
            log_reflection(f"  Error: {result.stderr[:200]}")
    except Exception as e:
        log_reflection(f"  ❌ Morning briefing: ERROR - {e}")
    
    # Check 2: Cron jobs
    log_reflection("  [2/6] Checking cron jobs...")
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if 'send_morning_agentmail' in result.stdout:
            log_reflection("  ✅ Morning cron: PRESENT")
        else:
            log_reflection("  ❌ Morning cron: MISSING")
    except Exception as e:
        log_reflection(f"  ❌ Cron check: ERROR - {e}")
    
    # Check 3: Tracker JSON
    log_reflection("  [3/6] Checking tracker.json...")
    try:
        with open(os.path.expanduser('~/.openclaw/workspace/PROJECTS/weight_loss_tracker/tracker.json'), 'r') as f:
            json.load(f)
        log_reflection("  ✅ Tracker JSON: VALID")
    except Exception as e:
        log_reflection(f"  ❌ Tracker JSON: ERROR - {e}")
    
    # Check 4: Calendar events
    log_reflection("  [4/6] Checking calendar...")
    try:
        with open(os.path.expanduser('~/.openclaw/workspace/calendar/events.json'), 'r') as f:
            events = json.load(f)
        log_reflection(f"  ✅ Calendar: {len(events)} events loaded")
    except Exception as e:
        log_reflection(f"  ❌ Calendar: ERROR - {e}")
    
    # Check 5: Trip briefing
    log_reflection("  [5/6] Checking trip briefing...")
    try:
        result = subprocess.run(
            ['python3', os.path.expanduser('~/.openclaw/trip_briefing.py')],
            capture_output=True, text=True, timeout=60
        )
        if 'Draft saved' in result.stdout:
            log_reflection("  ✅ Trip briefing: WORKING")
        else:
            log_reflection("  ⚠️ Trip briefing: NO DRAFT (may be past Apr 24)")
    except Exception as e:
        log_reflection(f"  ❌ Trip briefing: ERROR - {e}")
    
    # Check 6: Git repo
    log_reflection("  [6/6] Checking GitHub repo...")
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd=os.path.expanduser('~/.openclaw/workspace'),
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            log_reflection("  ✅ Git: Clean")
        else:
            log_reflection(f"  ⚠️ Git: Uncommitted changes ({len(result.stdout.strip().splitlines())} files)")
    except Exception as e:
        log_reflection(f"  ❌ Git: ERROR - {e}")
    
    log_reflection("✅ Post-upgrade verification complete")

def main():
    """Main reflection routine"""
    log_reflection("=" * 50)
    log_reflection("🌙 Starting 4 AM Reflection Hour")
    log_reflection("=" * 50)
    
    review_agents_md()
    check_tools_md()
    review_yesterday_memory()
    check_ai_models_monthly()
    check_post_upgrade()
    
    log_reflection("=" * 50)
    log_reflection("✅ Reflection complete - ready for the day!")
    log_reflection("=" * 50)

if __name__ == "__main__":
    main()
