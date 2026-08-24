"""Bottleneck Detector — Identifies what's actually blocking progress."""
from datetime import datetime
from typing import Any


class BottleneckDetector:
    """Find the real blocker (usually it's not what you think)."""

    def __init__(self, blueprint: dict):
        """Initialize with master blueprint."""
        self.blueprint = blueprint
        self.blockers_history = []  # Track what's blocked before

    def detect(self, lever_status: dict[str, Any] = None) -> dict[str, Any]:
        """Detect current blocker based on lever status."""
        levers = self.blueprint["levers"]

        if not lever_status:
            # Default: use first lever as proxy
            lever_status = {"₹100Cr deal": "STALLED"}

        detected = []

        for lever in levers:
            if lever["status"] == "STALLED" or lever["status"] == "NOT_PLANNED":
                blocker = {
                    "lever": lever["name"],
                    "status": lever["status"],
                    "blocker_type": self._classify_blocker(lever),
                    "blocker_text": lever["blocker"],
                    "action": lever["action_needed"],
                    "cost_monthly": lever.get("monthly_equivalent", 0),
                    "is_root": self._is_root_blocker(lever),
                }
                detected.append(blocker)

        # Sort by cost (highest impact first)
        detected.sort(key=lambda x: x["cost_monthly"], reverse=True)

        return {
            "timestamp": datetime.now().isoformat(),
            "root_cause": self.blueprint["bottleneck"]["root_cause"],
            "active_blockers": detected,
            "top_blocker": detected[0] if detected else None,
            "diagnosis": self._diagnose(),
            "prescription": self._prescribe(detected[0] if detected else None)
        }

    def _classify_blocker(self, lever: dict) -> str:
        """Classify blocker type."""
        blocker_text = lever["blocker"].lower()

        if "paper" in blocker_text or "signature" in blocker_text or "sign" in blocker_text:
            return "SIGNATURE_GATE"
        elif "call" in blocker_text or "broker" in blocker_text or "contact" in blocker_text:
            return "ASKING_GATE"
        elif "decision" in blocker_text or "decide" in blocker_text or "plan" in blocker_text:
            return "DECISION_GATE"
        elif "connect" in blocker_text or "wire" in blocker_text or "integration" in blocker_text:
            return "SYSTEM_GATE"
        else:
            return "OTHER"

    def _is_root_blocker(self, lever: dict) -> bool:
        """Is this blocker root (not just a symptom)?"""
        root_causes = ["asking aversion", "rejection aversion", "decision delay"]
        blocker_text = lever["blocker"].lower()

        for root in root_causes:
            if root in blocker_text:
                return True

        # If it requires an "ask", it's hitting the root cause
        if any(word in blocker_text for word in ["call", "ask", "contact", "reach out", "follow up"]):
            return True

        return False

    def _diagnose(self) -> str:
        """Root cause diagnosis."""
        return (
            "Root cause: You're rejection-averse (not risk-averse). "
            "You build instead of asking. Opportunities stall because you won't make the call. "
            "Example: ₹100Cr deal waiting for you to follow up on signatures. "
            "Example: Brokers never called about ₹15Cr land. "
            "Example: Pallavi's post-exit income never discussed with her."
        )

    def _prescribe(self, top_blocker: dict = None) -> str:
        """Prescription to unblock."""
        if not top_blocker:
            return "No active blockers detected."

        action = top_blocker.get("action", "")
        lever = top_blocker.get("lever", "")

        return (
            f"This week: {action}\n"
            f"Why: Unblocks {lever} ({top_blocker['cost_monthly']:,} INR/month potential).\n"
            f"Jarvis commitment: Track whether you ask. Report outcome Friday."
        )

    def track_outcome(self, blocker_id: str, outcome: str, notes: str = ""):
        """Record what happened when you tried to unblock."""
        self.blockers_history.append({
            "timestamp": datetime.now().isoformat(),
            "blocker_id": blocker_id,
            "outcome": outcome,  # "success" | "partial" | "failed"
            "notes": notes,
        })
        return self.blockers_history[-1]

    def learnings(self) -> dict[str, Any]:
        """What patterns have we learned about blockers?"""
        if not self.blockers_history:
            return {"message": "No outcomes recorded yet. Start tracking!"}

        successes = [x for x in self.blockers_history if x["outcome"] == "success"]
        failures = [x for x in self.blockers_history if x["outcome"] == "failed"]

        return {
            "total_attempts": len(self.blockers_history),
            "success_rate": len(successes) / len(self.blockers_history) if self.blockers_history else 0,
            "successes": successes,
            "failures": failures,
            "pattern": "Early calls work better than waiting" if successes else "Too early to tell — start tracking!"
        }
