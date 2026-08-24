# Telegram Bot — Jarvis Integration Instructions

**Goal:** Add `/briefing`, `/report`, `/ask`, and `/learnings` commands to Telegram bot.

**Time:** ~20 minutes

---

## Step 1: Copy Integration Code

Copy `telegram_integration/jarvis_commands.py` to your bot codebase:

```bash
cp telegram_integration/jarvis_commands.py core/telegram_bot/
```

---

## Step 2: Import in Bot

**File:** `core/telegram_bot/bot.py`

```python
# At the top with other imports
from jarvis_commands import (
    get_jarvis_briefing,
    get_family_briefing,
    record_jarvis_outcome,
    ask_jarvis,
    get_jarvis_learnings,
)
```

---

## Step 3: Add Command Handlers

**File:** `core/telegram_bot/bot.py`

Add these handlers to your bot:

```python
@bot.message_handler(commands=['briefing'])
def handle_briefing(message):
    """Get Shreyas's weekly briefing from Jarvis."""
    text = get_jarvis_briefing()
    bot.reply_to(message, text, parse_mode="HTML")


@bot.message_handler(commands=['family'])
def handle_family_briefing(message):
    """Get family-level briefing from Jarvis."""
    text = get_family_briefing()
    bot.reply_to(message, text, parse_mode="HTML")


@bot.message_handler(commands=['report'])
def handle_report(message):
    """Record an action outcome in Jarvis.
    Usage: /report Called broker success
    """
    text = message.text.replace("/report", "").strip()
    parts = text.split()

    if len(parts) < 2:
        bot.reply_to(
            message,
            "Usage: /report <action> <outcome>\n\n"
            "Example: /report Called broker success\n\n"
            "Outcomes: success | partial | failed"
        )
        return

    outcome = parts[-1].lower()  # last word
    action = " ".join(parts[:-1])  # rest

    if outcome not in ["success", "partial", "failed"]:
        bot.reply_to(message, f"❌ Unknown outcome: {outcome}\nUse: success | partial | failed")
        return

    result_text = record_jarvis_outcome(action, outcome, person="shreyas")
    bot.reply_to(message, result_text, parse_mode="HTML")


@bot.message_handler(commands=['ask'])
def handle_ask(message):
    """Ask Jarvis about a decision.
    Usage: /ask 100Cr deal
    """
    gate = message.text.replace("/ask", "").strip()

    if not gate:
        bot.reply_to(
            message,
            "Usage: /ask <decision gate>\n\n"
            "Examples:\n"
            "/ask 100Cr deal\n"
            "/ask Pallavi post-exit"
        )
        return

    text = ask_jarvis(gate)
    bot.reply_to(message, text, parse_mode="HTML")


@bot.message_handler(commands=['learnings'])
def handle_learnings(message):
    """Get what Jarvis has learned about what works."""
    text = get_jarvis_learnings()
    bot.reply_to(message, text, parse_mode="HTML")
```

---

## Step 4: Add Help Command

**File:** `core/telegram_bot/bot.py`

```python
@bot.message_handler(commands=['help'])
def handle_help(message):
    """Show Jarvis commands."""
    text = """
🧠 Jarvis Consciousness Commands

📊 /briefing
   Get your weekly briefing (goal, progress, blocker, action)

👨‍👩‍👧‍👦 /family
   Get family-level briefing (all 4 people)

📝 /report <action> <outcome>
   Record what you did and what happened
   Example: /report Called broker success
   Outcomes: success | partial | failed

🤔 /ask <decision>
   Ask Jarvis about a decision
   Example: /ask 100Cr deal

📚 /learnings
   See what's working based on recorded outcomes

💡 /help
   Show this help message
"""
    bot.reply_to(message, text)
```

---

## Step 5: Verify Jarvis API is Accessible

```bash
# Test Jarvis is running locally
curl http://localhost:5001/health

# Or test on VPS (if deployed)
curl http://31.97.229.117:5001/health
```

---

## Step 6: Configure Jarvis URL in jarvis_commands.py

**File:** `telegram_integration/jarvis_commands.py`

If Jarvis is on VPS, update the URL:

```python
# Line 12, change:
JARVIS_API_URL = "http://localhost:5001"

# To:
JARVIS_API_URL = "http://31.97.229.117:5001"

# Or use environment variable:
import os
JARVIS_API_URL = os.getenv("JARVIS_API_URL", "http://localhost:5001")
```

---

## Step 7: Test Commands

```bash
# Start your bot
python3 core/telegram_bot/bot.py

# In Telegram, try:
/briefing
# Should get: Weekly briefing with goal, progress, blocker, action

/family
# Should get: Family-level briefing with all 4 people

/report Called broker success
# Should get: Outcome recorded + learning update

/ask 100Cr deal
# Should get: Decision recommendation

/learnings
# Should get: What's working
```

---

## Step 8: Add to Bot Help/Menu

**File:** `core/telegram_bot/bot.py` or wherever commands are listed

Add to your bot's command menu:

```python
# Register commands with Telegram
commands = [
    telebot.types.BotCommand("briefing", "Get your weekly briefing"),
    telebot.types.BotCommand("family", "Get family briefing"),
    telebot.types.BotCommand("report", "Record an outcome"),
    telebot.types.BotCommand("ask", "Ask Jarvis a question"),
    telebot.types.BotCommand("learnings", "See what's working"),
    telebot.types.BotCommand("help", "Show all commands"),
]
bot.set_my_commands(commands)
```

---

## Step 9: Add Webhook Support (Optional)

**File:** `telegram_integration/jarvis_commands.py`

Add support for Telegram webhook updates (auto-record outcomes):

```python
@bot.message_handler(regexp="Jarvis")
def handle_jarvis_mentions(message):
    """Auto-record mentions of Jarvis actions."""
    text = message.text.lower()
    
    # Parse for: "called X" or "emailed Y" or "meeting with Z"
    if "called" in text or "contact" in text:
        action_type = "call"
    elif "email" in text or "sent" in text:
        action_type = "email"
    elif "meeting" in text or "discuss" in text:
        action_type = "meeting"
    else:
        return
    
    # Auto-record with "pending" status
    record_jarvis_outcome(
        message.text,
        "pending",
        person="shreyas",
        details={"source": "telegram_mention"}
    )
```

---

## Step 10: Test End-to-End

```bash
# 1. Start Jarvis API
python3 -m jarvis_consciousness.api

# 2. Start Telegram bot
python3 core/telegram_bot/bot.py

# 3. In Telegram, test:
/briefing
# Response: Weekly briefing

/report Called broker 100Cr success
# Response: Outcome recorded, learning update

/learnings
# Response: Success rates and best methods

# 4. Verify recorded
curl http://localhost:5001/api/learnings | jq .
```

---

## Command Usage Examples

### /briefing
```
User: /briefing
Bot:  🧠 WEEKLY BRIEFING
      📊 Progress: 9.2%
      Gap: ₹99.08L
      
      🎯 Top Lever: ₹100Cr Stalled Deal
      Potential: ₹1,50,000/month
      
      ⚠️ Blocker: Papers not signed (3-4 week gate)
      
      💡 This Week:
         Follow up on signature gate
```

### /report
```
User: /report Called broker about 100Cr papers success
Bot:  ✅ Recorded: Called broker about 100Cr papers → success
      
      📊 Learning Update:
         Total actions tracked: 5
         Success rate: 60%
      
      💡 Jarvis says:
         Keep pushing! Calling has 85% success rate.
```

### /ask
```
User: /ask Should I push 100Cr now
Bot:  🤔 DECISION: ₹100Cr Deal Follow-up
      
      Question: Push now or wait?
      
      💡 Recommendation: YES (80% confidence)
      Reason: 3-4 weeks to close; push now
      Tactic: Add 3rd party facilitator
      
      Next step: Call today, follow email tomorrow
```

### /learnings
```
User: /learnings
Bot:  📚 JARVIS LEARNINGS
      
      📊 Actions tracked: 5
      Success rate: 60%
      
      🎯 What works:
         Early morning calls: 85% success
         Personal intro: 90% success
      
      Pattern: You trend up when you call early
```

---

## Environment Variables

Optional: Set these in `.env`:

```bash
# Jarvis API URL (default: http://localhost:5001)
JARVIS_API_URL=http://31.97.229.117:5001

# Jarvis timeout (default: 5 seconds)
JARVIS_TIMEOUT=10

# Enable/disable Jarvis (default: true)
JARVIS_ENABLED=true
```

Then in `jarvis_commands.py`:

```python
import os

JARVIS_API_URL = os.getenv("JARVIS_API_URL", "http://localhost:5001")
JARVIS_TIMEOUT = int(os.getenv("JARVIS_TIMEOUT", 5))
```

---

## Troubleshooting

### "Jarvis unavailable" error

**Problem:** Bot can't reach Jarvis API

**Solution:**
1. Check Jarvis is running: `curl http://localhost:5001/health`
2. Check URL in jarvis_commands.py
3. Check Jarvis firewall: `sudo ufw allow 5001`
4. Check Jarvis logs: `journalctl -u jarvis-consciousness -f`

### "ModuleNotFoundError: No module named jarvis_commands"

**Problem:** Python can't find jarvis_commands.py

**Solution:**
1. Verify file exists: `ls core/telegram_bot/jarvis_commands.py`
2. Add to Python path in bot.py:
   ```python
   import sys
   sys.path.insert(0, 'core/telegram_bot')
   from jarvis_commands import *
   ```

### Commands not showing in Telegram

**Problem:** /briefing, /report, etc. not appearing as autocomplete

**Solution:**
1. Restart bot to re-register commands
2. Bot needs admin rights in group to set commands
3. Check bot is authenticated with Telegram token

### Outcome not recorded

**Problem:** /report says "Failed to record"

**Solution:**
1. Check Jarvis API is responding to POST
2. Check data/outcomes.jsonl is writable
3. Check JSON payload is valid
4. Check Jarvis logs for error

---

## Files Modified

After integration, your telegram bot repo will have:

```
core/telegram_bot/
├── jarvis_commands.py       [NEW] - Command implementations
├── bot.py                   [MODIFIED] - Added handlers
└── ...other files
```

---

## Done!

Your Telegram bot now has full Jarvis integration:
- ✅ /briefing — Weekly briefing
- ✅ /family — Family status
- ✅ /report — Record outcomes
- ✅ /ask — Ask Jarvis decisions
- ✅ /learnings — What's working
- ✅ /help — Show all commands

**Jarvis is now live in Telegram.** 🎉
