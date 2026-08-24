# Jarvis Consciousness — Master Deployment Checklist

**Status:** 🚀 READY TO DEPLOY

**Timeline:** Today (Aug 25, 2026)

---

## Phase 1: VPS Deployment (30 min)

- [ ] SSH to VPS: `ssh root@31.97.229.117`
- [ ] Run deployment script:
  ```bash
  scp deploy.sh root@31.97.229.117:/tmp/
  ssh root@31.97.229.117 'bash /tmp/deploy.sh'
  ```
- [ ] Verify service is running:
  ```bash
  ssh root@31.97.229.117 'systemctl status jarvis-consciousness'
  ```
- [ ] Test API:
  ```bash
  curl http://31.97.229.117:5001/health
  ```
- [ ] Test endpoints:
  ```bash
  curl http://31.97.229.117:5001/api/briefing | jq .
  curl http://31.97.229.117:5001/api/family/briefing | jq .
  ```

**Verification:**
- ✅ Service running: `systemctl status jarvis-consciousness`
- ✅ API responding: `curl http://31.97.229.117:5001/health`
- ✅ Logs healthy: `journalctl -u jarvis-consciousness -n 20`

---

## Phase 2: Command Center Integration (45 min)

### 2.1 Copy Files
- [ ] Copy `cc_integration/` folder to CC codebase
  ```bash
  cp -r cc_integration/ /path/to/command-center/
  ```

### 2.2 Register Routes
- [ ] Edit `app.py` or `__init__.py`
  ```python
  from cc_integration import jarvis_bp
  app.register_blueprint(jarvis_bp, url_prefix="/api/jarvis")
  ```

### 2.3 Update Config
- [ ] Set Jarvis URL (if different from localhost):
  ```python
  # cc_integration/jarvis_client.py
  JARVIS_API_URL = "http://31.97.229.117:5001"
  ```

### 2.4 Add Dashboard
- [ ] Edit `templates/dashboard.html`
  ```html
  {% include 'cc_integration/jarvis_dashboard.html' %}
  ```

### 2.5 Add Member Cards
- [ ] Add member status display to dashboard
  ```html
  <div id="shreyas-status"></div>
  <div id="pallavi-status"></div>
  <div id="maa-status"></div>
  <div id="father-status"></div>
  ```

### 2.6 Add Record Button
- [ ] Add "Record Jarvis Outcome" button to CC
  ```html
  <button onclick="recordJarvisOutcome()">
    📝 Record Jarvis Outcome
  </button>
  ```

### 2.7 Test Integration
- [ ] Start CC: `python3 app.py`
- [ ] Visit dashboard: `http://localhost:5000/dashboard`
- [ ] Verify Jarvis widget loads
- [ ] Test record button
- [ ] Verify outcome appears in Jarvis

**Verification:**
- ✅ Routes registered: `curl http://localhost:5000/api/jarvis/health`
- ✅ Dashboard loads: `http://localhost:5000/dashboard` (no errors)
- ✅ Briefing works: `curl http://localhost:5000/api/jarvis/briefing | jq .`
- ✅ Record works: Test button records an outcome

---

## Phase 3: Telegram Bot Integration (30 min)

### 3.1 Copy Code
- [ ] Copy `telegram_integration/jarvis_commands.py` to bot codebase
  ```bash
  cp telegram_integration/jarvis_commands.py core/telegram_bot/
  ```

### 3.2 Update Bot
- [ ] Edit `core/telegram_bot/bot.py`
  ```python
  from jarvis_commands import (
      get_jarvis_briefing,
      get_family_briefing,
      record_jarvis_outcome,
      ask_jarvis,
      get_jarvis_learnings,
  )
  ```

### 3.3 Add Handlers
- [ ] Add all 5 command handlers to bot.py
  - [ ] `/briefing` handler
  - [ ] `/family` handler
  - [ ] `/report` handler
  - [ ] `/ask` handler
  - [ ] `/learnings` handler

### 3.4 Update Jarvis URL
- [ ] If Jarvis on VPS, update URL in jarvis_commands.py:
  ```python
  JARVIS_API_URL = "http://31.97.229.117:5001"
  ```

### 3.5 Test Commands
- [ ] Start bot: `python3 core/telegram_bot/bot.py`
- [ ] In Telegram, test each command:
  - [ ] `/briefing`
  - [ ] `/family`
  - [ ] `/report Called broker success`
  - [ ] `/ask 100Cr deal`
  - [ ] `/learnings`

**Verification:**
- ✅ /briefing returns briefing
- ✅ /report records outcome
- ✅ /learnings shows patterns
- ✅ Telegram receives all responses

---

## Phase 4: Live Data & Learning (Continuous)

### Starting Today
- [ ] Make first calls (this week):
  - [ ] Call about ₹100Cr deal papers
  - [ ] Discuss Pallavi post-exit role
  - [ ] Follow up on ₹15Cr land
  
- [ ] Record outcomes via Telegram:
  ```
  /report Called broker about 100Cr success
  /report Discussed Pallavi role partial
  /report Followed up on 15Cr land success
  ```

- [ ] Watch Jarvis learn:
  ```
  /learnings
  # See updated success rates and patterns
  ```

### Weekly Cadence
- [ ] Every Monday 9am:
  ```
  /briefing
  # Get weekly action recommendation
  ```

- [ ] After each action (same day):
  ```
  /report <action> <outcome>
  # Record in Jarvis, it learns immediately
  ```

- [ ] Every Friday 5pm:
  ```
  /report <summary of week> success/partial/failed
  # Weekly wrap-up
  ```

- [ ] Next Monday:
  ```
  /briefing
  # Jarvis recommends next week based on learnings
  ```

---

## Deployment Status Tracking

### VPS
- [ ] Deploy started: _________
- [ ] Systemd service running: _________
- [ ] API responding: _________
- [ ] Health check passed: _________
- [ ] Deploy complete: _________

### Command Center
- [ ] Integration copied: _________
- [ ] Routes registered: _________
- [ ] Dashboard widget added: _________
- [ ] Member cards added: _________
- [ ] Integration tested: _________
- [ ] CC deploy complete: _________

### Telegram
- [ ] Commands copied: _________
- [ ] Handlers added: _________
- [ ] Bot restarted: _________
- [ ] Commands tested: _________
- [ ] Telegram integration complete: _________

### Live Usage
- [ ] First outcomes recorded: _________
- [ ] Jarvis learning verified: _________
- [ ] All 4 family members using: _________
- [ ] Weekly loop established: _________

---

## Success Metrics (First Month)

### By Aug 31
- [ ] ✅ VPS deployed
- [ ] ✅ CC integrated
- [ ] ✅ Telegram working
- [ ] [ ] 10+ outcomes recorded
- [ ] [ ] Jarvis patterns visible

### By Sept 1 (CRITICAL)
- [ ] [ ] One deal closes (₹100Cr OR ₹15Cr)
- [ ] [ ] Family income gap reduced ₹20L+
- [ ] [ ] Pallavi post-exit model decided
- [ ] [ ] Papers signing progress

### By Oct 1
- [ ] [ ] Second deal closing
- [ ] [ ] Pallavi post-exit income running
- [ ] [ ] Family progress: 4% → 15%+
- [ ] [ ] Jarvis learned 30+ outcomes

### By Dec 1
- [ ] [ ] Family at 30%+ progress
- [ ] [ ] Exit planning concrete
- [ ] [ ] All systems humming

---

## Rollback Plan (If Needed)

If something breaks, rollback is simple:

### Rollback VPS
```bash
# Stop service
ssh root@31.97.229.117 'systemctl stop jarvis-consciousness'

# It was running before from: git clone ...
# Just git pull latest stable:
ssh root@31.97.229.117 'cd /opt/jarvis-consciousness && git pull origin main'

# Restart
ssh root@31.97.229.117 'systemctl restart jarvis-consciousness'
```

### Rollback CC
```bash
# Remove cc_integration routes from app.py
# Remove dashboard widget from template
# Restart CC
python3 app.py
```

### Rollback Telegram
```bash
# Remove jarvis_commands import from bot.py
# Remove all command handlers
# Restart bot
python3 core/telegram_bot/bot.py
```

All rollbacks are instant — no data loss, just "disable the integration".

---

## Troubleshooting During Deployment

| Issue | Check | Fix |
|-------|-------|-----|
| "API unreachable" | `curl http://31.97.229.117:5001/health` | Check firewall, service running |
| "Module not found" | `ls cc_integration/__init__.py` | Copy files, check paths |
| "/briefing not working" | `curl /api/jarvis/briefing` | Check Jarvis URL in config |
| "Button doesn't record" | Check browser console (F12) | Verify endpoint, JSON format |
| "Bot doesn't respond" | Check bot logs | Verify Jarvis URL, handlers registered |

---

## Communication

### To Shreyas (Aug 25)
- [ ] Jarvis API live on VPS ✅
- [ ] CC dashboard showing progress ✅
- [ ] Telegram /briefing command ready ✅
- [ ] Ready to make calls & record outcomes ✅

### To Pallavi
- [ ] Pallavi dashboard live in CC
- [ ] Can see post-exit income target
- [ ] Can record progress in Telegram
- [ ] Monthly updates auto-generated

### To Maa
- [ ] Maa dashboard shows blockers
- [ ] Can track paper progress
- [ ] Weekly Jarvis reminders sent
- [ ] All decisions logged for reference

### To Father
- [ ] Father dashboard shows trade metrics
- [ ] Can track buyer network growth
- [ ] Monthly ₹ goals visible
- [ ] Learning from past deals

---

## Final Verification

Before declaring "LIVE", verify:

```bash
# 1. Jarvis API healthy
curl http://31.97.229.117:5001/health
# {"status": "ok"}

# 2. CC can reach it
curl http://localhost:5000/api/jarvis/health
# {"status": "ok"}

# 3. Telegram can reach it
/briefing in Telegram
# Returns briefing

# 4. Recording works
/report Called broker success in Telegram
# Records outcome in Jarvis

# 5. Learning works
/learnings in Telegram
# Shows updated stats

# 6. Dashboard live
http://localhost:5000/dashboard
# Shows Jarvis widget
```

**All 6 checks pass = GO LIVE** 🚀

---

## Go-Live Checklist

- [ ] Phase 1: VPS Deployment ✅
- [ ] Phase 2: Command Center ✅
- [ ] Phase 3: Telegram Bot ✅
- [ ] Phase 4: Live Data ✅
- [ ] All 6 verification checks pass ✅
- [ ] Team notified ✅
- [ ] First outcomes recorded ✅
- [ ] Learning loop active ✅

**Status: READY FOR PRODUCTION** 🟢

---

**Deployed by:** _____________  
**Date:** Aug 25, 2026  
**Time:** _____________  
**Verified by:** _____________  

**LIVE AT:** http://31.97.229.117:5001 ✅
