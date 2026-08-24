# Jarvis Consciousness — Full Architecture

## Overview

Jarvis is a **family-level goal engine** that:
- Understands your situation (financial, psychological, relational)
- Tracks progress for each person (Shreyas, Pallavi, Maa, Father)
- Learns what works (psychology + world knowledge + AI reasoning)
- Guides all decisions toward the unified family goal (exit + ₹1Cr+/mo)

---

## Core Systems

### 1. Goal Engine (`goal_engine.py`)
- **Purpose:** Understand situation, track progress, rank levers
- **Inputs:** Master blueprint (goals, levers, timeline)
- **Outputs:** Weekly briefing, progress score, top lever, decision gates
- **Key methods:**
  - `score_progress()` — Current score toward ₹1Cr/mo
  - `rank_levers()` — Which opportunity to push this week
  - `primary_blocker()` — What's actually blocking you
  - `weekly_briefing()` — Your weekly briefing

### 2. Family Consciousness (`family_consciousness.py`)
- **Purpose:** Track 4 people's goals + unified family target
- **Actors:** Shreyas, Pallavi, Maa, Father
- **Each person has:**
  - Individual goal + income target
  - Action log (what they did)
  - Outcome log (success/failure)
  - Current blocker
- **Family-level view:** Combined progress, critical path, unified actions

**Example:**
```python
family = FamilyConsciousness()
brief = family.weekly_family_briefing()
# Output: {
#   shreyas: {goal, income_gap, blocker, action},
#   pallavi: {goal, income_gap, blocker, action},
#   maa: {goal, blocker, action},
#   father: {goal, income_gap, blocker, action},
#   critical_path: "Shreyas: close ₹100Cr | Pallavi: decide post-exit",
# }
```

### 3. Bottleneck Detector (`bottleneck_detector.py`)
- **Purpose:** Identify what's REALLY blocking (often not what you think)
- **Root causes it detects:**
  - Signature gate (legal, compliance)
  - Asking gate (rejection aversion)
  - Decision gate (committee fear)
  - System gate (integration gaps)
- **Tracks history:** What was blocking before, how it was unblocked

### 4. Outcome Learner (`outcome_learner.py`)
- **Purpose:** Learn from every action you take
- **Tracks:** What worked, what didn't, patterns
- **Data source:** `data/outcomes.jsonl` (append-only, timestamped)
- **Auto-learns:**
  - Success rates by action type (call vs email vs broker)
  - Timing patterns (morning calls win more?)
  - Deal types that close vs stall

### 5. Knowledge Engine (`knowledge_engine.py`)
- **Incorporates:** Psychology + World Knowledge + AI Reasoning
- **Three sub-systems:**

#### a. PsychologicalModel
- Diagnoses rejection aversion (build-to-ask ratio)
- Suggests best approaches for your personality
- Decision-making patterns from research

#### b. WorldKnowledge
- Trade market data (crude, bitumen, metals)
- Real estate patterns (cycle time, commission ranges)
- Deal playbook (signature gates, acceleration tactics)
- **Public sources:** ICRA reports, startup teardowns, market data

#### c. ReasoningEngine
- Counterfactual analysis ("What if you emailed instead?")
- Pattern extraction ("Best method for your outcomes")
- AI-powered recommendations based on actual history

### 6. Real-Time Sync (`realtime_sync.py`)
- **Purpose:** Jarvis learns constantly from all systems
- **Sources:**
  - Telegram bot (`/report` command)
  - Command Center (webhook updates)
  - NeoSapien (deal status)
  - Family WhatsApp (status messages)
- **Auto-adjusts:** Recommendations update as new data arrives

### 7. API (`api.py`)
- **REST interface** for Command Center integration
- **Endpoints:**
  - `GET /api/briefing` — Shreyas's weekly briefing
  - `GET /api/family/briefing` — Family-level briefing
  - `POST /api/outcome` — Record action outcome
  - `GET /api/learnings` — What's working
  - `GET /api/decision/:gate` — Ask Jarvis
  - `GET /api/member/:name/briefing` — Individual member briefing
  - `POST /api/member/:name/blocker` — Update blocker
  - `POST /api/member/:name/income` — Update income

---

## Data Model

### master_blueprint.json
Your complete situation:
```json
{
  "situation": { goal, deadline, urgency },
  "financial": { burn, in-hand, gap, target },
  "levers": [
    {
      "name": "₹100Cr deal",
      "value": 100000000,
      "commission": "1.5%",
      "potential_monthly": 1500000,
      "status": "STALLED",
      "blocker": "Papers not signed",
      "priority": "CRITICAL"
    }
  ],
  "decision_gates": [
    { gate, decision, data_needed, recommendation }
  ]
}
```

### outcomes.jsonl
Append-only log of every action:
```jsonl
{"timestamp": "2026-08-24T10:30:00", "person": "shreyas", "action": "Called broker X", "outcome": "success"}
{"timestamp": "2026-08-24T14:00:00", "person": "pallavi", "action": "Discussed post-exit role", "outcome": "partial"}
{"timestamp": "2026-08-25T09:00:00", "person": "maa", "action": "Followed up on papers", "outcome": "success"}
```

---

## Weekly Loop

**Every Monday:**
1. Jarvis generates briefing (goal, progress, blocker, action)
2. Family members make their asks/decisions
3. Friday: Report outcomes via Telegram/CC
4. Real-time sync updates Jarvis
5. Learner auto-adjusts recommendations

**Every hour (when new data arrives):**
- Real-time sync processes webhook
- Learning loop re-analyzes outcomes
- Recommendations auto-adjust

---

## Integration with Command Center

### CC → Jarvis Webhooks
```bash
POST /api/outcome
{
  "action": "Updated ₹100Cr deal status in NeoSapien",
  "outcome": "partial",
  "person": "shreyas",
  "details": {"deal_id": "100cr_deal_1", "status": "papers_sent"}
}
```

### Jarvis → CC Dashboard
```bash
GET /api/snapshot
→ {
  shreyas: {score: 9.2%, gap: ₹99.08L, blocker, action},
  pallavi: {score: 0%, target: ₹5L, blocker, action},
  maa: {score: ?, blocker, action},
  father: {score: 50%, income: ₹5L, blocker, action},
}
```

---

## Telegram Integration

```
User: /report Called broker about ₹100Cr land
Bot: ✅ Recorded: Call → awaiting response
     Jarvis learns: Calling works 85% of time
     Next: Follow up Monday if no reply

User: /ask Should I push ₹100Cr now?
Bot: 💡 YES (80% confidence)
     Reason: 3-4 weeks to close; push now
     Tactic: Add 3rd party facilitator
     Next: Call today, follow email tomorrow
```

---

## Family Members' Own Dashboards

### Shreyas Dashboard
- Target: ₹1Cr/month (₹100Cr deal + ₹15Cr land + data center)
- Progress: 9.2%
- Blocker: Asking aversion (fix: 3 calls/week)
- This week: Call ₹100Cr, email broker, call back ₹15Cr

### Pallavi Dashboard
- Target: ₹5L/month post-Oct (board seat / advisor)
- Progress: 0% (starts Oct)
- Blocker: Model not decided (consultant vs board vs advisor)
- This week: Discuss with Shreyas + Maa, decide by Friday

### Maa Dashboard
- Role: Property coordination + decisions + TM
- Blockers: Papers (tribal land, ₹15Cr land, ₹100Cr)
- This week: Sign ₹15Cr mandate, follow up on ₹100Cr lawyer

### Father Dashboard
- Target: ₹20L/month (trade: crude, bitumen, metals)
- Current: ₹5L/month
- Progress: 25%
- Blocker: Buyer network (MSP ladder not built)
- This week: Call 3 new buyers for crude, build MSP list

---

## Learning Over Time

Jarvis builds institutional memory:

**Week 1:**
- Record 5 outcomes
- "Calling works better than email"

**Week 4:**
- Record 20 outcomes
- "Morning calls (6–8am) have 85% success; email has 45%"
- "Personal intro via broker beats cold call"
- "Pallavi's board-seat pitch resonates with board members"

**Week 12:**
- Record 50+ outcomes
- "Critical path: Shreyas closes deal → Pallavi income starts → both can exit"
- "Best sequence: Call → email → call (3-touch system)"
- "Maa's signature authority unblocks everything"

---

## Public GitHub

**Why public?**
- ✅ Accountability (you can't lie to yourself)
- ✅ Auditability (every action timestamped)
- ✅ Family visibility (progress is transparent)
- ✅ Advisor access (share with mentors/lawyers/brokers)

**What's shared:**
- Master blueprint (your goals, levers, timeline)
- Outcomes log (every action and result)
- Weekly briefs (progress, blockers, actions)
- NO: Personal numbers (income, amounts)
- NO: Private decisions

---

## Next Phases

### Phase 2: CC Dashboard
- [ ] Wire Jarvis API to CC frontend
- [ ] Live progress gauge (family + individual)
- [ ] Weekly briefing widget
- [ ] Blocker tracker
- [ ] Action recommendations

### Phase 3: Telegram Bot Integration
- [ ] /report outcome
- [ ] /briefing
- [ ] /ask decision
- [ ] /learnings
- [ ] Auto-sync from TG to Jarvis

### Phase 4: Family Access
- [ ] Pallavi dashboard (post-exit income)
- [ ] Maa dashboard (papers, signatures)
- [ ] Father dashboard (trade ops)
- [ ] WhatsApp webhooks for status updates

### Phase 5: Advanced Learning
- [ ] Predictive modeling (will this deal close?)
- [ ] Counterfactual simulation ("if we pushed harder")
- [ ] Deal success predictor
- [ ] Optimal timing recommender
