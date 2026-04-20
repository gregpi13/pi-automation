#!/bin/bash
# Daily OpenClaw Update Check Script
# Run: ./check-tts-updates.sh
# Or add to crontab: 0 20 * * * /home/groot13-pi/.openclaw/workspace/scripts/check-tts-updates.sh

LOG_FILE="/tmp/openclaw-version-check.log"
TELEGRAM_BOT_TOKEN="8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA"
TELEGRAM_CHAT_ID="7652382077"
CURRENT_VERSION=$(openclaw --version 2>/dev/null | head -1)

# Function to send Telegram message
send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${message}" \
        -d "parse_mode=Markdown" >/dev/null 2>&1
}

# Build the report
REPORT="*OpenClaw Daily Update Check*\n"
REPORT+="📅 $(date)\n"
REPORT+="📦 Current: ${CURRENT_VERSION}\n\n"

# Check if version changed from last run
NEW_VERSION_DETECTED=false
if [ -f "$LOG_FILE" ]; then
    LAST_VERSION=$(tail -1 "$LOG_FILE" 2>/dev/null | grep -o 'version:.*' | cut -d: -f2 | tr -d ' ')
    if [ "$LAST_VERSION" != "$CURRENT_VERSION" ] && [ -n "$LAST_VERSION" ]; then
        NEW_VERSION_DETECTED=true
        REPORT+="🎉 *NEW VERSION DETECTED!*\n"
        REPORT+="• Previous: ${LAST_VERSION}\n"
        REPORT+="• Current:  ${CURRENT_VERSION}\n\n"
    fi
fi

# Log current version
echo "$(date '+%Y-%m-%d %H:%M:%S'): version: $CURRENT_VERSION" >> "$LOG_FILE"

# Fetch latest release info from GitHub
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null | grep '"tag_name":' | head -1 | cut -d'"' -f4)
if [ -n "$LATEST_RELEASE" ]; then
    REPORT+="📥 Latest GitHub: ${LATEST_RELEASE}\n"
    
    # Check if this mentions TTS fixes
    TTS_FIXES=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null | grep -i "tts\|voice\|#7231" | head -3)
    if [ -n "$TTS_FIXES" ]; then
        REPORT+="🎉 *TTS FIXES IN LATEST RELEASE!*\n"
        REPORT+="Check: https://github.com/openclaw/openclaw/releases\n\n"
    fi
fi

# Check for TTS-related messages in gateway logs
TTS_LOGS=$(tail -100 /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -i "tts\|voice\|audio" | tail -5)
if [ -n "$TTS_LOGS" ]; then
    REPORT+="📝 Recent TTS logs found\n"
fi

REPORT+="\n🔗 Quick Links:\n"
REPORT+="• Issue #7231: github.com/openclaw/openclaw/issues/7231\n"
REPORT+="• Releases: github.com/openclaw/openclaw/releases\n"
REPORT+="• TTS Docs: docs.openclaw.ai/tools/tts"

# Send to Telegram
send_telegram "$REPORT"

# Also print to console for cron logs
echo "Report sent to Telegram"
echo "Current: $CURRENT_VERSION"
echo "Latest: $LATEST_RELEASE"

# If new version detected, send additional alert
if [ "$NEW_VERSION_DETECTED" = true ]; then
    sleep 2
    send_telegram "⚠️ *ACTION NEEDED*\n\nOpenClaw was updated from ${LAST_VERSION} to ${CURRENT_VERSION}\n\nCheck if TTS fixes are included!"
fi
