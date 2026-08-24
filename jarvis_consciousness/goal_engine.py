"""Goal Engine — Understands situation, tracks progress toward ₹1Cr/mo + family exit."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class GoalEngine:
    """Parse your situation into structured goals and track progress."""

    def __init__(self, blueprint_path: str | Path = None):
        """Load master blueprint (situation, levers, timeline)."""
        if blueprint_path is None:
            blueprint_path = Path(__file__).parent.parent / "data" / "master_blueprint.json"

        with open(blueprint_path) as f:
            self.blueprint = json.load(f)

        self.goal = self.blueprint["situation"]["root_goal"]
        self.target_monthly = self.blueprint["financial"]["target"]["amount_inr"]
        self.deadline = datetime.fromisoformat(self.blueprint["situation"]["deadline"])
        self.now = datetime.now()
        self.days_remaining = (self.deadline - self.now).days
        self.months_remaining = max(1, self.days_remaining // 30)

    def score_progress(self, current_monthly_income: int = 92000) -> dict[str, Any]:
        """Score progress toward ₹1Cr/mo.

        Args:
            current_monthly_income: Current in-hand monthly income

        Returns:
            Progress score (0–100), gap, levers ranking
        """
        gap = self.target_monthly - current_monthly_income
        score = min(100, int((current_monthly_income / self.target_monthly) * 100))

        return {
            "score": score,
            "target": self.target_monthly,
            "current": current_monthly_income,
            "gap": gap,
            "gap_monthly": gap,
            "gap_12months": gap * 12,
            "deadline": self.deadline.isoformat(),
            "days_remaining": self.days_remaining,
            "months_remaining": self.months_remaining,
            "urgency_phase": "CRITICAL" if self.days_remaining < 30 else "HIGH" if self.days_remaining < 60 else "MEDIUM",
        }

    def rank_levers(self) -> list[dict[str, Any]]:
        """Rank all levers by impact × likelihood × urgency.

        Returns:
            Sorted list of levers (highest impact first)
        """
        levers = self.blueprint["levers"]
        scored = []

        for lever in levers:
            monthly = lever.get("monthly_equivalent", 0)
            likelihood = lever.get("likelihood_if_pushed", lever.get("likelihood", 0.5))

            # Score: monthly impact × likelihood × urgency boost
            priority_boost = 2.0 if lever["priority"] == "CRITICAL" else 1.5 if lever["priority"] == "HIGH" else 1.0
            score = (monthly * likelihood) * priority_boost

            scored.append({
                "rank_score": score,
                **lever
            })

        return sorted(scored, key=lambda x: x["rank_score"], reverse=True)

    def top_lever(self) -> dict[str, Any]:
        """The single highest-impact lever to push this week."""
        return self.rank_levers()[0]

    def primary_blocker(self) -> dict[str, Any]:
        """What's actually blocking progress (the root bottleneck)."""
        blocker = self.blueprint["bottleneck"]

        # Current blocker = top lever's blocker
        top = self.top_lever()

        return {
            "root_cause": blocker["root_cause"],
            "manifestation": blocker["manifestation"],
            "current_blocker": top["blocker"],
            "on_lever": top["name"],
            "action_needed": top["action_needed"],
            "jarvis_recommendation": f"Push {top['name']} this week — call about: {top['blocker']}"
        }

    def weekly_briefing(self, current_monthly_income: int = 92000) -> dict[str, Any]:
        """Your weekly briefing: goal, progress, blocker, next action."""
        progress = self.score_progress(current_monthly_income)
        blocker = self.primary_blocker()
        top = self.top_lever()

        return {
            "week": datetime.now().isoformat(),
            "goal": self.goal,
            "progress": progress,
            "top_lever": {
                "name": top["name"],
                "potential_monthly": top.get("monthly_equivalent", 0),
                "status": top["status"],
                "priority": top["priority"],
            },
            "blocker": blocker,
            "next_action": f"{blocker['action_needed']}",
            "jarvis_says": f"📊 Score: {progress['score']}%. Gap: ₹{gap_inr(progress['gap'])}. "
                          f"Blocker: {blocker['current_blocker']}. "
                          f"Do this: {blocker['action_needed']}",
        }

    def decision_gate(self, gate_name: str) -> dict[str, Any]:
        """Get Jarvis recommendation for a specific decision."""
        for gate in self.blueprint["decision_gates"]:
            if gate["gate"].lower() == gate_name.lower():
                return gate
        return {"error": f"Gate '{gate_name}' not found"}


def gap_inr(amount: int) -> str:
    """Format INR gap nicely."""
    if amount >= 10000000:
        return f"{amount / 10000000:.1f}Cr"
    elif amount >= 100000:
        return f"{amount / 100000:.0f}L"
    else:
        return f"₹{amount:,}"
