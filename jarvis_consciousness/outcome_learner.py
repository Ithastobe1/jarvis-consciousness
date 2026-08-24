"""Outcome Learner — Records what actually works and repeats it."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class OutcomeListener:
    """Listen to outcomes, learn patterns, improve recommendations."""

    def __init__(self, log_path: str | Path = None):
        """Initialize outcome log."""
        if log_path is None:
            log_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"

        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.outcomes = self._load_outcomes()

    def _load_outcomes(self) -> list[dict]:
        """Load all recorded outcomes."""
        if not self.log_path.exists():
            return []

        outcomes = []
        with open(self.log_path) as f:
            for line in f:
                if line.strip():
                    outcomes.append(json.loads(line))
        return outcomes

    def record(
        self,
        action: str,
        outcome: str,
        details: dict = None,
        next_action: str = None
    ) -> dict[str, Any]:
        """Record an action and its outcome.

        Args:
            action: What you did (e.g., "Called broker X about ₹15Cr land")
            outcome: Result ("success" | "partial" | "failed")
            details: Additional context (who, when, what they said)
            next_action: What to do based on this outcome

        Returns:
            Recorded entry
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "outcome": outcome,
            "details": details or {},
            "next_action": next_action,
        }

        # Append to log
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        self.outcomes.append(entry)
        return entry

    def success_rate(self, action_type: str = None) -> dict[str, Any]:
        """What's working? Success rate by action type."""
        if not self.outcomes:
            return {"message": "No outcomes recorded yet"}

        # Filter by action type if specified
        if action_type:
            relevant = [x for x in self.outcomes if action_type.lower() in x["action"].lower()]
        else:
            relevant = self.outcomes

        if not relevant:
            return {"message": f"No outcomes for action: {action_type}"}

        successes = len([x for x in relevant if x["outcome"] == "success"])
        total = len(relevant)
        rate = successes / total if total > 0 else 0

        return {
            "action_type": action_type or "all",
            "total_attempts": total,
            "successes": successes,
            "success_rate_percent": int(rate * 100),
            "recent_outcomes": relevant[-5:],  # Last 5
        }

    def what_works(self) -> dict[str, Any]:
        """Extract patterns of what works."""
        if not self.outcomes:
            return {"message": "No data yet"}

        # Group by action prefix
        actions = {}
        for outcome in self.outcomes:
            action = outcome["action"]
            # Extract action type (first 3-4 words)
            action_type = " ".join(action.split()[:3])

            if action_type not in actions:
                actions[action_type] = {"success": 0, "partial": 0, "failed": 0}

            actions[action_type][outcome["outcome"]] += 1

        # Rank by success rate
        ranked = []
        for action_type, counts in actions.items():
            total = sum(counts.values())
            success_rate = counts["success"] / total if total > 0 else 0
            ranked.append({
                "action_type": action_type,
                "success_rate": success_rate,
                "counts": counts,
            })

        ranked.sort(key=lambda x: x["success_rate"], reverse=True)

        return {
            "best_practices": [x["action_type"] for x in ranked if x["success_rate"] > 0.5],
            "action_scores": ranked,
            "recommendation": ranked[0]["action_type"] if ranked else "Try calling",
        }

    def learn(self) -> dict[str, Any]:
        """Meta-learning: What has Jarvis learned about you?"""
        if len(self.outcomes) < 3:
            return {"message": "Need at least 3 outcomes to learn"}

        # Pattern detection
        early_movers = len([x for x in self.outcomes if "early" in x.get("details", {}).get("timing", "")])
        call_outcomes = self.success_rate("call")
        decision_outcomes = self.success_rate("decision")

        return {
            "total_actions_tracked": len(self.outcomes),
            "what_works": self.what_works(),
            "call_success_rate": call_outcomes.get("success_rate_percent", 0),
            "decision_success_rate": decision_outcomes.get("success_rate_percent", 0),
            "pattern": self._detect_pattern(),
            "jarvis_says": self._jarvis_meta_insight(),
        }

    def _detect_pattern(self) -> str:
        """Detect meta-patterns."""
        if not self.outcomes:
            return "No pattern yet."

        # Look at timing
        success_times = []
        for outcome in self.outcomes:
            if outcome["outcome"] == "success":
                time_str = outcome.get("details", {}).get("time_of_day", "")
                if time_str:
                    success_times.append(time_str)

        if success_times:
            return f"Successes clustered around: {success_times[0] if success_times else 'various times'}"

        # Look at outcome distribution
        success_count = len([x for x in self.outcomes if x["outcome"] == "success"])
        if success_count / len(self.outcomes) > 0.6:
            return "You're winning more often than failing. Keep going."
        elif success_count / len(self.outcomes) < 0.3:
            return "Success rate is low. Try different approach or better preparation."
        else:
            return "Mixed results. Pattern not yet clear."

    def _jarvis_meta_insight(self) -> str:
        """Jarvis's meta-observation about your patterns."""
        outcomes = self.outcomes[-5:] if len(self.outcomes) >= 5 else self.outcomes

        if not outcomes:
            return "No actions yet. Start with the top blocker: call someone this week."

        recent_success = len([x for x in outcomes if x["outcome"] == "success"])

        if recent_success == len(outcomes):
            return "🔥 You're on fire. Push harder on all levers."
        elif recent_success > len(outcomes) / 2:
            return "✅ You're trending up. Keep making the asks."
        else:
            return "⚠️  Recent outcomes are soft. Revisit your pitch or timing."
