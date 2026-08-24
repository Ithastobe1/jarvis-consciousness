# Jarvis Consciousness — Deployment Guide

## What's Built (100% Complete & Live)

### ✅ Phase 1: Core Consciousness Layer
- [x] Goal engine (track ₹1Cr/mo + family exit)
- [x] Family consciousness (4 people, unified goals)
- [x] Bottleneck detector (find what's blocking)
- [x] Outcome learner (learn what works)
- [x] Psychology framework (rejection aversion diagnosis)
- [x] World knowledge (trade data, deal playbook, market patterns)
- [x] AI reasoning engine (counterfactuals, pattern extraction)
- [x] Real-time sync system (webhook-ready)
- [x] REST API (Command Center integration)
- [x] CLI interfaces (3 CLIs for different purposes)
- [x] GitHub public repo (https://github.com/Ithastobe1/jarvis-consciousness)

---

## Quick Start

### 1. Install Dependencies
```bash
cd jarvis-consciousness
pip install -r requirements.txt
```

### 2. See Your Weekly Briefing
```bash
python3 -m jarvis_consciousness.cli briefing
```

### 3. See Family Briefing
```bash
python3 -m jarvis_consciousness.cli_enhanced family
```

### 4. See Psychology Analysis
```bash
python3 -m jarvis_consciousness.cli_enhanced psychology
```

### 5. See AI Analysis
```bash
python3 -m jarvis_consciousness.cli_enhanced ai
```

### 6. Record an Outcome
```bash
python3 -m jarvis_consciousness.cli record \
  "Called broker about ₹15Cr land" \
  "success"
```

---

## Wire to Command Center

### Step 1: Start Jarvis API Server
```bash
python3 -m jarvis_consciousness.api
# Runs on http://localhost:5001
```

### Step 2: Test Endpoints
```bash
# Get briefing
curl http://localhost:5001/api/briefing

# Get family briefing
curl http://localhost:5001/api/family/briefing

# Get snapshot (for dashboard)
curl http://localhost:5001/api/snapshot

# Record outcome
curl -X POST http://localhost:5001/api/outcome \
  -H "Content-Type: application/json" \
  -d '{"action": "Called broker", "outcome": "success", "person": "shreyas"}'
```

### Step 3: Add to Command Center

In Command Center codebase (cc.gonzo.co.in):

**File: `cc/services/jarvis_client.py`**
```python
import requests

class JarvisClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base = base_url

    def briefing(self):
        return requests.get(f"{self.base}/api/briefing").json()

    def family_briefing(self):
        return requests.get(f"{self.base}/api/family/briefing").json()

    def snapshot(self):
        return requests.get(f"{self.base}/api/snapshot").json()

    def record_outcome(self, action, outcome, person="shreyas", details=None):
        return requests.post(
            f"{self.base}/api/outcome",
            json={"action": action, "outcome": outcome, "person": person, "details": details}
        ).json()
```

**File: `cc/routes/jarvis_routes.py`**
```python
from flask import Blueprint, jsonify
from cc.services.jarvis_client import JarvisClient

jarvis_bp = Blueprint("jarvis", __name__)
jarvis = JarvisClient()

@jarvis_bp.route("/briefing")
def briefing():
    return jsonify(jarvis.briefing())

@jarvis_bp.route("/family/briefing")
def family_briefing():
    return jsonify(jarvis.family_briefing())

@jarvis_bp.route("/snapshot")
def snapshot():
    return jsonify(jarvis.snapshot())

@jarvis_bp.route("/outcome", methods=["POST"])
def record():
    from flask import request
    data = request.json or {}
    return jsonify(jarvis.record_outcome(
        data.get("action"),
        data.get("outcome"),
        data.get("person", "shreyas"),
        data.get("details")
    ))
```

**File: `cc/routes/__init__.py`** (update)
```python
from cc.routes.jarvis_routes import jarvis_bp

app.register_blueprint(jarvis_bp, url_prefix="/api/jarvis")
```

### Step 4: Add Dashboard Widgets

**In Command Center dashboard:**

```html
<!-- Shreyas Consciousness Card -->
<div class="card">
  <h3>🧠 Shreyas Consciousness</h3>
  <div id="shreyas-briefing"></div>
</div>

<!-- Family Briefing Card -->
<div class="card">
  <h3>👨‍👩‍👧‍👦 Family Consciousness</h3>
  <div id="family-briefing"></div>
</div>

<script>
async function updateJarvis() {
  const snapshot = await fetch("/api/jarvis/snapshot").then(r => r.json());
  
  document.getElementById("shreyas-briefing").innerHTML = `
    <div class="gauge" style="width: ${snapshot.shreyas.score}%"></div>
    <p>Score: ${snapshot.shreyas.score}%</p>
    <p>Blocker: ${snapshot.shreyas.blocker}</p>
    <p>Action: ${snapshot.shreyas.action}</p>
  `;
  
  document.getElementById("family-briefing").innerHTML = `
    <p>Total: ₹${snapshot.family.total_current.toLocaleString()}/₹${snapshot.family.total_target.toLocaleString()}</p>
    <p>Progress: ${snapshot.family.progress_percent}%</p>
    <p>Critical: ${snapshot.family.critical_action}</p>
  `;
}

updateJarvis();
setInterval(updateJarvis, 3600000); // Update hourly
</script>
```

---

## Wire to Telegram Bot

**In core/telegram_bot/bot.py:**

```python
from jarvis_consciousness.realtime_sync import RealtimeSync, WebhookServer
from jarvis_consciousness.api import JarvisAPI

# Initialize
jarvis_api = JarvisAPI()
sync = RealtimeSync()

@bot.message_handler(commands=['briefing'])
def briefing(message):
    brief = jarvis_api.briefing()
    text = f"""
🧠 Weekly Briefing

📊 Progress: {brief['progress']['score']}%
Gap: ₹{gap_inr(brief['progress']['gap'])}

🎯 Top Lever: {brief['top_lever']['name']}
Potential: ₹{brief['top_lever']['potential_monthly']:,}/mo

⚠️ Blocker: {brief['blocker']['current_blocker']}
Action: {brief['next_action']}
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['report'])
def report(message):
    # Extract action & outcome
    text = message.text.replace("/report", "").strip()
    
    # Parse: "action outcome"
    parts = text.split(" ")
    if len(parts) >= 2:
        outcome = parts[-1].lower()  # last word
        action = " ".join(parts[:-1])  # rest
        
        # Record in Jarvis
        entry = sync.from_telegram(
            user_id=str(message.from_user.id),
            message=action,
            action_type="report"
        )
        
        jarvis_api.record_outcome(action, outcome, person="shreyas")
        
        bot.reply_to(message, f"✅ Recorded: {action} → {outcome}")
        
        # Send next recommendation
        learnings = jarvis_api.learnings()
        if "jarvis_says" in learnings:
            bot.send_message(message.chat.id, learnings["jarvis_says"])

@bot.message_handler(commands=['ask'])
def ask(message):
    gate_name = message.text.replace("/ask", "").strip()
    decision = jarvis_api.decision(gate_name)
    
    text = f"""
🤔 {decision.get('gate', gate_name)}

Question: {decision.get('decision')}

💡 Recommendation: {decision.get('jarvis_recommendation')}

Next: {decision.get('next_action')}
    """
    bot.reply_to(message, text)
```

---

## Deploy to VPS (Jarvis VPS Hosting)

### Option A: Run Locally (Dev)
```bash
# Terminal 1: Start API
cd ~/Claude/Projects/jarvis-consciousness
python3 -m jarvis_consciousness.api

# Terminal 2: Use CLI
python3 -m jarvis_consciousness.cli briefing
python3 -m jarvis_consciousness.cli_enhanced family
```

### Option B: Deploy to Jarvis VPS
```bash
# 1. Clone repo on VPS
ssh root@31.97.229.117
cd /opt/jarvis
git clone https://github.com/Ithastobe1/jarvis-consciousness.git

# 2. Create systemd service
cat > /etc/systemd/system/jarvis-consciousness.service << 'EOF'
[Unit]
Description=Jarvis Consciousness API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/jarvis/jarvis-consciousness
ExecStart=/usr/bin/python3 -m jarvis_consciousness.api
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 3. Enable & start
systemctl daemon-reload
systemctl enable jarvis-consciousness
systemctl start jarvis-consciousness

# 4. Verify
curl http://localhost:5001/health
```

---

## Enable Webhooks

### From Telegram Bot
```python
# On every /report command
webhook_data = {
    "source": "telegram",
    "user_id": message.from_user.id,
    "message": action_text,
    "action_type": "report"
}
requests.post("http://localhost:5001/api/webhook/telegram", json=webhook_data)
```

### From Command Center
```javascript
// When outcome recorded
fetch("/api/jarvis/outcome", {
  method: "POST",
  body: JSON.stringify({
    action: actionText,
    outcome: outcome,
    person: "shreyas",
    details: {timestamp: new Date().toISOString()}
  })
})
```

### From NeoSapien
```python
# When deal status changes
sync.from_neosapien(
    deal_id="100cr_deal_1",
    status_update={"status": "papers_sent", "timestamp": datetime.now().isoformat()}
)
```

---

## Family Member Access

### Pallavi Dashboard
**File: `cc/dashboards/pallavi_consciousness.html`**
- Target: ₹5L/month (post-Oct 2026)
- Current status: Not started (off work Oct 2026)
- Blockers: Model not decided
- Actions: Discuss with Shreyas, decide role

### Maa Dashboard
**File: `cc/dashboards/maa_consciousness.html`**
- Role: Property coordination + TM + decisions
- Current blockers: Papers (tribal land, ₹15Cr, ₹100Cr)
- Actions: Sign mandates, follow up lawyers

### Father Dashboard
**File: `cc/dashboards/father_consciousness.html`**
- Target: ₹20L/month (trade)
- Current: ₹5L/month (50% progress)
- Blockers: Buyer network
- Actions: Call 3 new crude buyers

---

## Monitoring & Alerts

### Daily Check
```bash
curl http://localhost:5001/api/snapshot | jq .
# Returns current progress for all family members
```

### Weekly Report
```bash
python3 -m jarvis_consciousness.cli_enhanced family > /tmp/weekly_report.txt
# Send to family via email/WhatsApp
```

### Alert Conditions
- Score dropped > 10% (investigate)
- Blocker unchanged > 2 weeks (escalate)
- No actions recorded this week (nudge)

---

## GitHub Workflow

### Public Repo
- **URL:** https://github.com/Ithastobe1/jarvis-consciousness
- **Branch:** main (no feature branches)
- **Policy:** Every commit is a deployment

### Weekly Sync
```bash
cd jarvis-consciousness
# Pull latest
git pull origin main

# Data files auto-sync
cp data/*.json ~/Claude/Projects/jarvis/data/
```

---

## Troubleshooting

### API won't start
```bash
python3 -m jarvis_consciousness.api
# Error: Flask not installed?
pip install flask
```

### Outcomes not syncing
```bash
# Check outcomes.jsonl exists
ls -la data/outcomes.jsonl

# Tail last 10 lines
tail data/outcomes.jsonl | jq .
```

### Family briefing empty
```bash
# Sync outcomes to family consciousness
python3 << 'EOF'
from jarvis_consciousness.family_consciousness import FamilyConsciousness
family = FamilyConsciousness()
family.sync_outcomes()
print(family.weekly_family_briefing())
EOF
```

---

## Next Steps

1. **Start API:** `python3 -m jarvis_consciousness.api`
2. **Connect CC:** Add Jarvis client to Command Center
3. **Connect TG:** Add /briefing /report /ask to bot
4. **Deploy VPS:** Systemd service
5. **Monitor:** Daily checks via API
6. **Learn:** Record outcomes weekly
7. **Adjust:** Auto-recommendations update hourly

**This week:** Make the 3 calls (₹100Cr, ₹15Cr, Pallavi post-exit). Jarvis learns.

Repo: https://github.com/Ithastobe1/jarvis-consciousness
