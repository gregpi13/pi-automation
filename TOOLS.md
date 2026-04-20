# TOOLS.md - Local Notes

## Active Skills

### ✅ Ready to Use
- **☔ weather** - Get weather forecasts via wttr.in or Open-Meteo (no API key needed)
- **📧 AgentMail** - Primary email system (sageai.harris@agentmail.to)

### ⏸️ Available (needs setup)
- **🎵 spotify-player** - Terminal Spotify playback/search
- **📝 summarize** - Summarize URLs, podcasts, local files (needs API key)
- **🧩 coding-agent** - Spawn coding agents for complex tasks (needs API key)

### ❌ Known Limitations
- **📎 Image Attachments** - AgentMail cannot currently download/process image attachments via SDK (April 2026). Text emails work fine. OpenClaw native image viewing via `read` tool works for local files but not yet for Telegram/AgentMail attachments. **Monitor for future OpenClaw updates.**

## Email Credentials - ACTIVE ✅

### AgentMail - sageai.harris@agentmail.to (PRIMARY)
- **Status**: Active and working (April 2026)
- **API Key**: Stored in `/home/groot13-pi/.openclaw/secure/agentmail-api-key`
- **Purpose**: Primary email for morning briefings, calendar invites, all automated communications
- **SDK**: `pip install agentmail`
- **Scripts**: `send_morning_agentmail.py`, `update_calendar.py`
- **Note**: Replaced Gmail as primary email system

### Outlook - sagepi2026@outlook.com (DELETED)
- **Status**: Account deleted (April 2026)
- **Reason**: Basic auth blocked

### Telegram Bot - ACTIVE ✅
- **Bot Username**: @Sage_pi_bot
- **Token**: 8401666212:AAEZDR7dVsIqzuTMX160DldeqROKWlw1AXA
- **Chat ID**: 7652382077
- **User Phone**: 416-471-7417
- **User Name**: Greg Harris
- **Daily Summary**: Automatically sends at 5:00 AM via `/home/groot13-pi/.openclaw/send_daily_telegram_summary.py`
- **Cron Job**: `0 5 * * *` (5:00 AM daily)
- **Backup**: Secondary to AgentMail

### Tailscale
- **Device:** raspberrypi
- **Tailnet:** tail13bfb5.ts.net
- **Funnel:** Port 3456 (currently inactive)
