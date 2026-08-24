# Jarvis Consciousness Layer

**Purpose:** Make Jarvis self-aware, goal-driven, and autonomous.

Jarvis is not just a tool. It's your external brain that:
- Understands your root goal (₹1Cr/mo + family exit)
- Tracks progress every week
- Identifies what's blocking you (asking aversion)
- Recommends exact next actions
- Learns what works
- Fixes broken systems automatically

---

## Your Situation (Parsed)

**Root Goal:** Family joint exit (you + Pallavi quit, ~10 people run business, daughter Rayna safe)

**Time Horizon:** Now until Sept 2026 (when Pallavi's income stops permanently)

**The Money:** 
- Current burn: ₹2.5L/month
- Current in-hand: ₹92k/month
- Gap to close: ₹22–30L over 12 months
- Target: ₹1Cr/month (restitution for family humiliation)
- Lever: One ₹50–100Cr mandate @1–2%

**Live Deals (stalled):**
- ₹12–15Cr land sale (papers ready)
- ₹100Cr deal (stalled on papers)

**Root Cause of Stall:** You're rejection-averse. You build instead of asking.

---

## How Jarvis Thinks

```
GOAL: ₹1Cr/month + family exit by 2027

├─ LEVER 1: Close the ₹100Cr deal
│  └─ BLOCKER: Papers (3-4 weeks to get signed)
│  └─ ACTION: Who do I ask? When?
│
├─ LEVER 2: Land sale (₹12–15Cr ready now)
│  └─ BLOCKER: Capital not positioned
│  └─ ACTION: Which broker do I call?
│
├─ LEVER 3: Velesia/Jarvis/Wealth unified
│  └─ BLOCKER: Systems don't talk
│  └─ ACTION: Ship connectors this week
│
└─ LEVER 4: Pallavi's post-exit income (Oct 2026)
   └─ BLOCKER: Plan not written
   └─ ACTION: Decide model (consultant, advisor, board seat?)
```

---

## Weekly Loop

Every Monday, Jarvis:
1. **Pulls live data** (Command Center, NeoSapien, deal register)
2. **Scores progress** toward ₹1Cr/mo
3. **Detects bottleneck** (what's actually blocking)
4. **Recommends action** (specific thing to do this week)
5. **Learns outcome** (did you ask? What happened?)
6. **Adjusts next week's ask** (based on what worked)

---

## Architecture

- **goal_engine.py** — Understands your situation, tracks progress
- **bottleneck_detector.py** — Finds what's actually blocking (not what you think)
- **outcome_learner.py** — Records what works, repeats it
- **decision_router.py** — Routes all decisions toward ₹1Cr/mo
- **dashboards/** — Your weekly briefing (live ₹ gauge, blocker, next action)

---

## How to Use

```bash
# See this week's briefing (goal, blocker, action)
python3 -m jarvis_consciousness.dashboard

# Update live data (deals, progress, income)
python3 -m jarvis_consciousness.ingest --data-file deals.json

# Ask Jarvis what to do next
python3 -m jarvis_consciousness.ask "Should I push for the ₹100Cr deal now?"

# Train the outcome learner (record what happened)
python3 -m jarvis_consciousness.learn --action "called broker X" --outcome "leads to Y"
```

---

## Public GitHub

This repo is **100% public**. All your situation, goals, progress, and decisions are visible.

Why? Because:
1. It forces clarity (you can't lie to yourself on GitHub)
2. It documents the journey (for your family, advisors, and future self)
3. It's auditable (every action, outcome, and decision is timestamped)

---

## Status

- [ ] Core goal engine (this week)
- [ ] Bottleneck detector (this week)
- [ ] Outcome learner (this week)
- [ ] Dashboard (live gauge + blocker + action)
- [ ] Push to GitHub (public)
- [ ] Wire to Command Center
- [ ] Weekly automation (runs every Monday)
