# Command Center — Jarvis Integration Instructions

**Goal:** Wire Jarvis Consciousness API into Command Center dashboard and actions.

**Time:** ~30 minutes

---

## Step 1: Copy Integration Files

Copy `cc_integration/` folder from jarvis-consciousness repo to your CC codebase:

```bash
# From jarvis-consciousness repo
cp -r cc_integration/ /path/to/command-center/

# Structure:
# command-center/
# ├── cc_integration/
# │   ├── __init__.py
# │   ├── jarvis_client.py       # REST client
# │   ├── jarvis_routes.py       # Flask routes
# │   └── jarvis_dashboard.html  # Dashboard widget
```

---

## Step 2: Register Routes in Flask App

**File:** `app.py` or `__init__.py` (wherever your Flask app is created)

```python
# At the top with other imports
from cc_integration import jarvis_bp

# In app creation section
def create_app():
    app = Flask(__name__)
    
    # Register other blueprints...
    app.register_blueprint(jarvis_bp, url_prefix="/api/jarvis")
    
    return app
```

---

## Step 3: Add Dashboard Widget

**File:** `templates/dashboard.html` or your main dashboard template

```html
<!-- Add this section to your dashboard -->
<div class="container mt-5">
  {% include 'cc_integration/jarvis_dashboard.html' %}
</div>
```

---

## Step 4: Test Integration

```bash
# Start your CC server
python3 app.py
# or: flask run

# Test Jarvis endpoint
curl http://localhost:5000/api/jarvis/health

# Visit dashboard
open http://localhost:5000/dashboard
# Should see Jarvis widget with live gauge
```

---

## Step 5: Configure Jarvis API URL

**File:** `cc_integration/jarvis_client.py`

If Jarvis is on a different server, update the URL:

```python
# Default: localhost:5001
jarvis_client = JarvisClient(base_url="http://localhost:5001")

# For VPS: 31.97.229.117:5001
jarvis_client = JarvisClient(base_url="http://31.97.229.117:5001")

# For production with DNS:
jarvis_client = JarvisClient(base_url="https://jarvis-api.yourdomain.com")
```

---

## Step 6: Add Record Outcome Button

**File:** `templates/dashboard.html`

Add this button to record outcomes from CC:

```html
<button onclick="recordJarvisOutcome()">
  📝 Record Jarvis Outcome
</button>

<script>
async function recordJarvisOutcome() {
  const action = prompt("What did you do?");
  const outcome = prompt("What happened? (success/partial/failed)");
  const person = prompt("Who? (shreyas/pallavi/maa/father)");
  
  const response = await fetch("/api/jarvis/outcome", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({action, outcome, person})
  });
  
  alert("Outcome recorded! Jarvis is learning...");
  location.reload();
}
</script>
```

---

## Step 7: Add Member Status Cards

**File:** `templates/dashboard.html`

Display each family member's status:

```html
<!-- Shreyas Card -->
<div class="card">
  <h5>🧠 Shreyas</h5>
  <div id="shreyas-status"></div>
</div>

<!-- Pallavi Card -->
<div class="card">
  <h5>👩 Pallavi</h5>
  <div id="pallavi-status"></div>
</div>

<!-- Maa Card -->
<div class="card">
  <h5>👵 Maa</h5>
  <div id="maa-status"></div>
</div>

<!-- Father Card -->
<div class="card">
  <h5>👴 Father</h5>
  <div id="father-status"></div>
</div>

<script>
async function loadMemberStatus() {
  const members = ['shreyas', 'pallavi', 'maa', 'father'];
  
  for (const member of members) {
    const response = await fetch(`/api/jarvis/member/${member}/briefing`);
    const data = await response.json();
    
    const html = `
      <p>Target: ₹${(data.target_monthly_income || 0).toLocaleString()}/mo</p>
      <p>Current: ₹${(data.current_monthly_income || 0).toLocaleString()}/mo</p>
      <p>Success rate: ${(data.success_rate * 100).toFixed(0)}%</p>
      <p>Blocker: ${data.current_blocker?.blocker || 'None'}</p>
    `;
    
    document.getElementById(`${member}-status`).innerHTML = html;
  }
}

loadMemberStatus();
setInterval(loadMemberStatus, 300000); // Refresh every 5 min
</script>
```

---

## Step 8: Add Live Snapshot to Sidebar

**File:** `templates/sidebar.html` or sidebar component

```html
<div class="sidebar-widget jarvis-snapshot">
  <h5>🧠 Jarvis Status</h5>
  <div id="jarvis-snapshot"></div>
</div>

<script>
async function updateSnapshot() {
  const response = await fetch("/api/jarvis/snapshot");
  const data = await response.json();
  
  const html = `
    <div class="metric">
      <span class="label">Shreyas</span>
      <span class="value">${data.shreyas.score}%</span>
    </div>
    <div class="metric">
      <span class="label">Blocker</span>
      <span class="value">${data.shreyas.blocker}</span>
    </div>
    <div class="metric">
      <span class="label">This Week</span>
      <span class="value">${data.shreyas.action}</span>
    </div>
  `;
  
  document.getElementById("jarvis-snapshot").innerHTML = html;
}

updateSnapshot();
setInterval(updateSnapshot, 600000); // Refresh every 10 min
</script>
```

---

## Step 9: Enable Webhook Recording

**File:** `routes/actions.py` or similar

When actions are taken in CC, automatically record in Jarvis:

```python
@app.route("/api/action/record", methods=["POST"])
def record_action():
    data = request.json
    
    # Record in Jarvis
    from cc_integration import JarvisClient
    jarvis = JarvisClient()
    
    jarvis.record_outcome(
        action=data.get("action"),
        outcome=data.get("outcome"),
        person=data.get("person", "shreyas"),
        details=data.get("details")
    )
    
    return {"status": "recorded"}
```

---

## Step 10: Test End-to-End

```bash
# 1. Verify Jarvis API is running (on VPS or localhost)
curl http://localhost:5001/health
# Should return: {"status": "ok"}

# 2. Verify CC can reach it
curl http://localhost:5000/api/jarvis/health
# Should return: {"status": "ok"}

# 3. Verify dashboard loads
open http://localhost:5000/dashboard
# Should show Jarvis widget with progress gauge

# 4. Record an outcome via CC
# Click "Record Jarvis Outcome" button
# Enter: "Called broker" → "success" → "shreyas"
# Should see update in dashboard

# 5. Check Jarvis learned it
curl http://localhost:5000/api/jarvis/learnings | jq .
# Should show updated success rates
```

---

## API Endpoints Available in CC

Once wired, these endpoints are available:

```python
# Get briefings
GET /api/jarvis/briefing
GET /api/jarvis/family/briefing

# Record actions
POST /api/jarvis/outcome
{
  "action": "Called broker about 100Cr",
  "outcome": "success",
  "person": "shreyas",
  "details": {"time": "09:30am"}
}

# Get member data
GET /api/jarvis/member/:name/briefing
POST /api/jarvis/member/:name/income
POST /api/jarvis/member/:name/blocker

# Get insights
GET /api/jarvis/snapshot     # For dashboards
GET /api/jarvis/blockers     # All blockers
GET /api/jarvis/learnings    # What's working

# Health
GET /api/jarvis/health
```

---

## Environment Variables

Optional: Set these in your `.env`:

```bash
# Jarvis API URL (default: http://localhost:5001)
JARVIS_API_URL=http://31.97.229.117:5001

# Jarvis API timeout (default: 5 seconds)
JARVIS_TIMEOUT=10

# Enable/disable Jarvis integration (default: true)
JARVIS_ENABLED=true
```

Then in `jarvis_client.py`:

```python
import os

base_url = os.getenv("JARVIS_API_URL", "http://localhost:5001")
timeout = int(os.getenv("JARVIS_TIMEOUT", 5))
enabled = os.getenv("JARVIS_ENABLED", "true").lower() == "true"

jarvis = JarvisClient(base_url=base_url, timeout=timeout)
```

---

## Troubleshooting

### "Connection refused" error

**Problem:** CC can't reach Jarvis API

**Solution:**
1. Verify Jarvis is running: `curl http://localhost:5001/health`
2. If on VPS, check firewall: `sudo ufw allow 5001`
3. Check Jarvis URL in jarvis_client.py
4. Check logs: `journalctl -u jarvis-consciousness -f`

### "No module named cc_integration"

**Problem:** Python can't find the integration module

**Solution:**
1. Verify folder exists: `ls cc_integration/`
2. Verify `__init__.py` exists: `ls cc_integration/__init__.py`
3. Check Python path includes CC directory

### Dashboard widget not loading

**Problem:** Jarvis dashboard HTML not showing

**Solution:**
1. Check include path in template: `{% include 'cc_integration/jarvis_dashboard.html' %}`
2. Verify file exists at that path
3. Check browser console for errors (F12)
4. Verify /api/jarvis/snapshot endpoint returns JSON

### Outcomes not being recorded

**Problem:** /api/jarvis/outcome returns 500 error

**Solution:**
1. Check CC logs for error message
2. Verify JSON payload is valid
3. Check Jarvis API logs: `journalctl -u jarvis-consciousness -f`
4. Verify data/outcomes.jsonl is writable

---

## Next Steps

1. ✅ Copy cc_integration folder
2. ✅ Register routes in Flask app
3. ✅ Add dashboard widget
4. ✅ Test endpoints
5. ✅ Add record outcome button
6. ✅ Add member status cards
7. ✅ Deploy to CC production
8. ✅ Set up webhook recording

---

## Files Modified

After integration, your CC repo will have:

```
command-center/
├── cc_integration/          [NEW]
│   ├── __init__.py
│   ├── jarvis_client.py
│   ├── jarvis_routes.py
│   └── jarvis_dashboard.html
├── app.py                   [MODIFIED] - Added blueprint
├── templates/
│   └── dashboard.html       [MODIFIED] - Added widget & cards
└── routes/
    └── actions.py           [MODIFIED] - Added webhook recording
```

---

## Done!

Your Command Center now has full Jarvis integration:
- ✅ Live progress dashboards
- ✅ Record outcomes from CC
- ✅ View all family members' status
- ✅ See what's working (learnings)
- ✅ Get next actions
- ✅ Track blockers

**Jarvis is now live in Command Center.** 🎉
