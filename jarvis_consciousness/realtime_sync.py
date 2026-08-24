"""Real-Time Sync — Jarvis learns constantly from all systems.

Integrates with:
- Command Center (webhook updates)
- Telegram bot (action outcomes via /report)
- NeoSapien (deal updates)
- Family WhatsApp/Telegram (status updates)
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class RealtimeSync:
    """Live sync from all systems into Jarvis consciousness."""

    def __init__(self, outcomes_log_path: str | Path = None):
        if outcomes_log_path is None:
            outcomes_log_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"
        self.log_path = Path(outcomes_log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def from_telegram(self, user_id: str, message: str, action_type: str) -> dict:
        """Receive outcome from Telegram bot."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": "telegram",
            "user_id": user_id,
            "action_type": action_type,  # "ask" | "report" | "update"
            "message": message,
            "parsed": self._parse_telegram_message(message),
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def from_command_center(self, member: str, update_type: str, data: dict) -> dict:
        """Receive update from Command Center."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": "command_center",
            "member": member,
            "update_type": update_type,  # "income_update" | "blocker_set" | "outcome_recorded"
            "data": data,
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def from_neosapien(self, deal_id: str, status_update: dict) -> dict:
        """Receive deal status from Neo-1."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": "neosapien",
            "deal_id": deal_id,
            "status_update": status_update,
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def from_family_whatsapp(self, member: str, message: str) -> dict:
        """Receive status from family WhatsApp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": "family_whatsapp",
            "member": member,
            "message": message,
            "parsed": self._parse_family_message(member, message),
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def _parse_telegram_message(self, message: str) -> dict:
        """Extract structured data from Telegram message."""
        lower_msg = message.lower()

        # Detect action type
        action_type = None
        if any(word in lower_msg for word in ["called", "emailed", "reached", "contacted", "pitch"]):
            action_type = "call"
        elif any(word in lower_msg for word in ["meeting", "discussed", "talked", "spoke"]):
            action_type = "meeting"
        elif any(word in lower_msg for word in ["yes", "success", "win", "close", "deal"]):
            action_type = "success"
        elif any(word in lower_msg for word in ["no", "reject", "failed", "pass"]):
            action_type = "rejection"

        # Detect deal/amount
        deal_value = None
        if "100cr" in lower_msg or "100 cr" in lower_msg:
            deal_value = "100Cr"
        elif "15cr" in lower_msg or "15 cr" in lower_msg:
            deal_value = "15Cr"

        return {
            "action_type": action_type,
            "deal_value": deal_value,
            "extracted_message": message,
        }

    def _parse_family_message(self, member: str, message: str) -> dict:
        """Extract structured data from family message."""
        lower_msg = message.lower()

        status = None
        if any(word in lower_msg for word in ["done", "finished", "complete", "signed"]):
            status = "complete"
        elif any(word in lower_msg for word in ["meeting", "scheduled", "next week"]):
            status = "in_progress"
        elif any(word in lower_msg for word in ["stuck", "waiting", "blocked", "delayed"]):
            status = "blocked"

        return {
            "member": member,
            "status": status,
            "message": message,
        }

    def webhook_handler(self, source: str, data: dict) -> dict:
        """Handle incoming webhook from any system."""
        if source == "telegram":
            return self.from_telegram(
                data.get("user_id", "unknown"),
                data.get("message", ""),
                data.get("action_type", "unknown"),
            )
        elif source == "command_center":
            return self.from_command_center(
                data.get("member", "unknown"),
                data.get("update_type", "unknown"),
                data.get("data", {}),
            )
        elif source == "neosapien":
            return self.from_neosapien(
                data.get("deal_id", "unknown"),
                data.get("status_update", {}),
            )
        elif source == "family_whatsapp":
            return self.from_family_whatsapp(
                data.get("member", "unknown"),
                data.get("message", ""),
            )
        else:
            return {"error": f"Unknown source: {source}"}


class LearningLoop:
    """Continuous learning from real-time data."""

    def __init__(self, outcomes_log_path: str | Path = None):
        if outcomes_log_path is None:
            outcomes_log_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"
        self.log_path = Path(outcomes_log_path)
        self.last_analysis = datetime.now() - timedelta(days=1)

    def should_reanalyze(self) -> bool:
        """Should we re-run analysis? (hourly, or when new data arrives)"""
        now = datetime.now()
        return (now - self.last_analysis).total_seconds() > 3600

    def analyze_recent(self, hours: int = 24) -> dict:
        """Analyze outcomes from last N hours."""
        if not self.log_path.exists():
            return {"message": "No outcome data"}

        cutoff = datetime.now() - timedelta(hours=hours)
        recent = []

        with open(self.log_path) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                try:
                    ts = datetime.fromisoformat(entry["timestamp"])
                    if ts > cutoff:
                        recent.append(entry)
                except (ValueError, KeyError):
                    continue

        # Analyze patterns
        by_source = {}
        by_member = {}

        for entry in recent:
            source = entry.get("source", "unknown")
            by_source[source] = by_source.get(source, 0) + 1

            if "member" in entry:
                member = entry["member"]
                by_member[member] = by_member.get(member, 0) + 1

        self.last_analysis = datetime.now()

        return {
            "period_hours": hours,
            "total_events": len(recent),
            "by_source": by_source,
            "by_member": by_member,
            "recent_entries": recent[-5:] if recent else [],
        }

    def auto_adjust_recommendations(self, engine: Any) -> dict:
        """Auto-adjust Jarvis recommendations based on recent outcomes."""
        analysis = self.analyze_recent(hours=24)

        if analysis["total_events"] == 0:
            return {"adjustment": "No new data; keeping current recommendations"}

        # If lots of failures, suggest different approach
        adjustment = {
            "timestamp": datetime.now().isoformat(),
            "events_analyzed": analysis["total_events"],
            "recommendation_adjustments": [],
        }

        # Check success rates by source
        if analysis["by_source"].get("telegram", 0) > 5:
            # We have Telegram activity; check outcomes
            adjustment["recommendation_adjustments"].append({
                "observation": f"High Telegram activity ({analysis['by_source']['telegram']} events)",
                "suggestion": "User is engaging frequently. Recommend higher-difficulty asks.",
            })

        if analysis["by_member"]:
            for member, count in analysis["by_member"].items():
                if count > 2:
                    adjustment["recommendation_adjustments"].append({
                        "observation": f"{member} has {count} recent updates",
                        "suggestion": f"Focus on {member}'s blockers this week.",
                    })

        return adjustment


class WebhookServer:
    """Simple webhook handler for real-time integrations."""

    def __init__(self, api_instance: Any):
        """api_instance: JarvisAPI instance for processing."""
        self.api = api_instance
        self.sync = RealtimeSync()
        self.learner = LearningLoop()

    def handle_telegram_webhook(self, user_id: str, message: str) -> dict:
        """Handle Telegram /report message."""
        entry = self.sync.from_telegram(user_id, message, "report")
        parsed = entry.get("parsed", {})

        # Auto-extract and record if confident
        if parsed.get("action_type"):
            self.api.record_outcome(
                action=message,
                outcome="recorded_from_telegram",
                person="shreyas" if "shreyas" in message.lower() else "unknown",
            )

        # Check if should reanalyze
        if self.learner.should_reanalyze():
            adjustment = self.learner.auto_adjust_recommendations(self.api.engine)
            return {"recorded": entry, "auto_adjustment": adjustment}

        return {"recorded": entry}

    def handle_cc_webhook(self, member: str, update_type: str, data: dict) -> dict:
        """Handle Command Center webhook."""
        entry = self.sync.from_command_center(member, update_type, data)

        # Update member in family consciousness
        if update_type == "income_update":
            self.api.set_member_income(member, data.get("monthly_income", 0))

        if update_type == "blocker_set":
            self.api.set_member_blocker(member, data.get("blocker", ""))

        return {"recorded": entry}
