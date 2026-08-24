"""Jarvis Telegram Bot Commands Integration.

Add these commands to core/telegram_bot/bot.py
"""
import requests
from datetime import datetime


JARVIS_API_URL = "http://localhost:5001"


def format_inr(amount: int) -> str:
    """Format INR nicely."""
    if amount >= 10000000:
        return f"₹{amount / 10000000:.1f}Cr"
    elif amount >= 100000:
        return f"₹{amount / 100000:.0f}L"
    else:
        return f"₹{amount:,}"


def get_jarvis_briefing() -> str:
    """Fetch Shreyas's weekly briefing from Jarvis."""
    try:
        response = requests.get(f"{JARVIS_API_URL}/api/briefing", timeout=5)
        data = response.json()

        if "error" in data:
            return f"❌ Jarvis error: {data['error']}"

        progress = data.get("progress", {})
        blocker = data.get("blocker", {})
        top_lever = data.get("top_lever", {})

        return f"""
🧠 WEEKLY BRIEFING

📊 Progress: {progress.get('score', 0)}%
   Gap: {format_inr(progress.get('gap', 0))}
   Days left: {progress.get('days_remaining', 0)} days

🎯 Top Lever: {top_lever.get('name', 'Unknown')}
   Potential: ₹{top_lever.get('potential_monthly', 0):,}/month
   Priority: {top_lever.get('priority', 'N/A')}

⚠️ Blocker: {blocker.get('current_blocker', 'Unknown')}

💡 This Week:
   {data.get('next_action', 'Make the ask')}
"""
    except Exception as e:
        return f"⚠️ Jarvis unavailable: {str(e)}"


def get_family_briefing() -> str:
    """Fetch family-level briefing."""
    try:
        response = requests.get(f"{JARVIS_API_URL}/api/family/briefing", timeout=5)
        data = response.json()

        if "error" in data:
            return f"❌ Jarvis error: {data['error']}"

        family = data.get("family_progress", {})
        members = data.get("each_member", {})

        text = f"""
👨‍👩‍👧‍👦 FAMILY BRIEFING

📊 Family Progress: {data.get('progress_percent', 0)}%
   Current: {format_inr(family.get('total_current_monthly', 0))}/month
   Target: {format_inr(family.get('total_target_monthly', 0))}/month
   Gap: {format_inr(family.get('total_gap', 0))}

⚡ Critical Path:
   {data.get('critical_path', {}).get('this_week_action', 'TBD')}

👥 Members:
"""

        for name, member in members.items():
            if member.get("target"):
                rate = int(member.get("success_rate", 0) * 100)
                text += f"\n   {member['name'].upper()}: {rate}% success rate"
                if member.get("gap"):
                    text += f" | Gap: {format_inr(member['gap'])}"
                if member.get("blocker"):
                    text += f"\n      Blocker: {member['blocker']}"

        return text

    except Exception as e:
        return f"⚠️ Jarvis unavailable: {str(e)}"


def record_jarvis_outcome(action: str, outcome: str, person: str = "shreyas") -> str:
    """Record an action outcome in Jarvis."""
    try:
        response = requests.post(
            f"{JARVIS_API_URL}/api/outcome",
            json={"action": action, "outcome": outcome, "person": person},
            timeout=5,
        )
        data = response.json()

        if "error" in data:
            return f"❌ Failed to record: {data['error']}"

        # Get updated learnings
        learnings_response = requests.get(
            f"{JARVIS_API_URL}/api/learnings", timeout=5
        )
        learnings = learnings_response.json()

        return f"""
✅ Recorded: {action} → {outcome}

📊 Learning Update:
   Total actions tracked: {learnings.get('total_actions_tracked', 0)}
   Success rate: {int(learnings.get('success_count', 0) / max(learnings.get('total_actions_tracked', 1), 1) * 100)}%

💡 Jarvis says:
   {learnings.get('jarvis_says', 'Keep pushing!')}
"""

    except Exception as e:
        return f"⚠️ Failed to record: {str(e)}"


def ask_jarvis(gate_name: str) -> str:
    """Ask Jarvis about a decision."""
    try:
        response = requests.get(
            f"{JARVIS_API_URL}/api/decision/{gate_name}",
            timeout=5,
        )
        data = response.json()

        if "error" in data:
            return f"❌ Decision not found: {data.get('error', 'Unknown gate')}"

        return f"""
🤔 {data.get('gate', gate_name).upper()}

Question: {data.get('decision', 'N/A')}

💡 Recommendation: {data.get('jarvis_recommendation', 'N/A')}

Next step: {data.get('next_action', 'TBD')}
"""

    except Exception as e:
        return f"⚠️ Jarvis unavailable: {str(e)}"


def get_jarvis_learnings() -> str:
    """Get what Jarvis has learned."""
    try:
        response = requests.get(f"{JARVIS_API_URL}/api/learnings", timeout=5)
        data = response.json()

        if "message" in data:
            return f"📚 {data['message']}"

        return f"""
📚 JARVIS LEARNINGS

📊 Actions tracked: {data.get('total_actions_tracked', 0)}
   Success rate: {int(data.get('success_count', 0) / max(data.get('total_actions_tracked', 1), 1) * 100)}%

🎯 What works:
   {data.get('jarvis_says', 'Early calls and personal intros.')}

Pattern: {data.get('pattern', 'Building data...')}
"""

    except Exception as e:
        return f"⚠️ Jarvis unavailable: {str(e)}"


# ============================================================================
# TELEGRAM BOT COMMAND HANDLERS
# Add these to core/telegram_bot/bot.py
# ============================================================================

# @bot.message_handler(commands=['briefing'])
# def handle_briefing(message):
#     """Get weekly briefing from Jarvis."""
#     text = get_jarvis_briefing()
#     bot.reply_to(message, text, parse_mode="HTML")
#
#
# @bot.message_handler(commands=['family'])
# def handle_family_briefing(message):
#     """Get family-level briefing."""
#     text = get_family_briefing()
#     bot.reply_to(message, text, parse_mode="HTML")
#
#
# @bot.message_handler(commands=['report'])
# def handle_report(message):
#     """Record an action outcome.
#     Usage: /report Called broker success
#     """
#     text = message.text.replace("/report", "").strip()
#     parts = text.split()
#
#     if len(parts) < 2:
#         bot.reply_to(
#             message,
#             "Usage: /report <action> <outcome>\n\n"
#             "Example: /report Called broker success\n\n"
#             "Outcomes: success | partial | failed"
#         )
#         return
#
#     outcome = parts[-1].lower()  # last word
#     action = " ".join(parts[:-1])  # rest
#
#     if outcome not in ["success", "partial", "failed"]:
#         bot.reply_to(message, f"❌ Unknown outcome: {outcome}\nUse: success | partial | failed")
#         return
#
#     result_text = record_jarvis_outcome(action, outcome, person="shreyas")
#     bot.reply_to(message, result_text, parse_mode="HTML")
#
#
# @bot.message_handler(commands=['ask'])
# def handle_ask(message):
#     """Ask Jarvis about a decision.
#     Usage: /ask 100Cr deal
#     """
#     gate = message.text.replace("/ask", "").strip()
#
#     if not gate:
#         bot.reply_to(message, "Usage: /ask <decision gate>\n\nExamples:\n/ask 100Cr deal\n/ask Pallavi post-exit")
#         return
#
#     text = ask_jarvis(gate)
#     bot.reply_to(message, text, parse_mode="HTML")
#
#
# @bot.message_handler(commands=['learnings'])
# def handle_learnings(message):
#     """Get what Jarvis has learned."""
#     text = get_jarvis_learnings()
#     bot.reply_to(message, text, parse_mode="HTML")
