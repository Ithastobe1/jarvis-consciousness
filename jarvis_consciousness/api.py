"""Jarvis API — REST interface for Command Center integration.

Endpoints:
- GET /briefing — Weekly briefing (Shreyas)
- GET /family/briefing — Family-level briefing
- POST /outcome — Record an action outcome
- GET /learnings — What's working
- GET /decision/:gate — Ask Jarvis
- GET /members/:name/briefing — Individual member briefing
"""
import json
from datetime import datetime
from pathlib import Path

from jarvis_consciousness.bottleneck_detector import BottleneckDetector
from jarvis_consciousness.family_consciousness import FamilyConsciousness
from jarvis_consciousness.goal_engine import GoalEngine
from jarvis_consciousness.outcome_learner import OutcomeListener


class JarvisAPI:
    """REST API for Jarvis Consciousness."""

    def __init__(self, blueprint_path: str | Path = None):
        self.engine = GoalEngine(blueprint_path)
        self.family = FamilyConsciousness(blueprint_path)
        self.learner = OutcomeListener()
        self.blueprint_path = blueprint_path or (
            Path(__file__).parent.parent / "data" / "master_blueprint.json"
        )

    def briefing(self, current_income: int = 92000) -> dict:
        """Shreyas's weekly briefing."""
        return self.engine.weekly_briefing(current_income)

    def family_briefing(self) -> dict:
        """Family-level weekly briefing."""
        from pathlib import Path
        outcomes_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"
        self.family.sync_outcomes(outcomes_path)  # Sync latest outcomes
        return self.family.weekly_family_briefing()

    def record_outcome(
        self,
        action: str,
        outcome: str,
        person: str = "shreyas",
        details: dict = None,
    ) -> dict:
        """Record an action outcome for a family member."""
        # Record in learner
        entry = self.learner.record(action, outcome, details)

        # Update family member
        if person.lower() in self.family.members:
            member = self.family.members[person.lower()]
            member.record_action(action, outcome, details)

        return entry

    def learnings(self) -> dict:
        """What's working based on recorded outcomes."""
        return self.learner.learn()

    def decision(self, gate_name: str) -> dict:
        """Ask Jarvis about a decision."""
        return self.engine.decision_gate(gate_name)

    def member_briefing(self, name: str) -> dict:
        """Briefing for one family member."""
        if name.lower() not in self.family.members:
            return {"error": f"Member '{name}' not found"}

        member = self.family.members[name.lower()]
        return member.to_dict()

    def set_member_blocker(self, name: str, blocker: str, priority: str = "HIGH") -> dict:
        """Set what's blocking a family member."""
        if name.lower() not in self.family.members:
            return {"error": f"Member '{name}' not found"}

        member = self.family.members[name.lower()]
        member.set_blocker(blocker, priority)
        return {"person": name, "blocker": blocker, "priority": priority}

    def set_member_income(self, name: str, monthly_income: int) -> dict:
        """Update a member's current income."""
        if name.lower() not in self.family.members:
            return {"error": f"Member '{name}' not found"}

        member = self.family.members[name.lower()]
        member.current_monthly_income = monthly_income
        return {"person": name, "income": monthly_income, "timestamp": datetime.now().isoformat()}

    def unified_blockers(self) -> dict:
        """All family blockers."""
        return {"blockers": self.family.unified_blockers(), "total": len(self.family.unified_blockers())}

    def progress_snapshot(self) -> dict:
        """Current progress snapshot for dashboards."""
        shreyas_brief = self.briefing()
        family_brief = self.family_briefing()

        return {
            "timestamp": datetime.now().isoformat(),
            "shreyas": {
                "score": shreyas_brief["progress"]["score"],
                "gap": shreyas_brief["progress"]["gap"],
                "blocker": shreyas_brief["blocker"]["current_blocker"],
                "action": shreyas_brief["next_action"],
            },
            "family": {
                "total_current": family_brief["family_progress"]["total_current_monthly"],
                "total_target": family_brief["family_progress"]["total_target_monthly"],
                "gap": family_brief["family_progress"]["total_gap"],
                "progress_percent": family_brief["progress_percent"],
                "critical_action": family_brief["critical_path"]["this_week_action"],
            },
            "members": family_brief["each_member"],
        }


# Flask app wrapper
def create_app(blueprint_path: str | Path = None):
    """Create Flask app for Jarvis API."""
    try:
        from flask import Flask, jsonify, request
    except ImportError:
        raise ImportError("Flask required. Install with: pip install flask")

    app = Flask(__name__)
    jarvis = JarvisAPI(blueprint_path)

    @app.route("/api/briefing", methods=["GET"])
    def get_briefing():
        """Shreyas's weekly briefing."""
        income = request.args.get("income", 92000, type=int)
        return jsonify(jarvis.briefing(income))

    @app.route("/api/family/briefing", methods=["GET"])
    def get_family_briefing():
        """Family-level briefing."""
        return jsonify(jarvis.family_briefing())

    @app.route("/api/outcome", methods=["POST"])
    def record():
        """Record an action outcome."""
        data = request.json or {}
        result = jarvis.record_outcome(
            action=data.get("action", ""),
            outcome=data.get("outcome", ""),
            person=data.get("person", "shreyas"),
            details=data.get("details"),
        )
        return jsonify(result), 201

    @app.route("/api/learnings", methods=["GET"])
    def get_learnings():
        """What's working."""
        return jsonify(jarvis.learnings())

    @app.route("/api/decision/<gate_name>", methods=["GET"])
    def get_decision(gate_name):
        """Ask Jarvis."""
        return jsonify(jarvis.decision(gate_name))

    @app.route("/api/member/<name>/briefing", methods=["GET"])
    def get_member(name):
        """Member briefing."""
        return jsonify(jarvis.member_briefing(name))

    @app.route("/api/member/<name>/blocker", methods=["POST"])
    def set_blocker(name):
        """Set member blocker."""
        data = request.json or {}
        result = jarvis.set_member_blocker(
            name=name,
            blocker=data.get("blocker", ""),
            priority=data.get("priority", "HIGH"),
        )
        return jsonify(result)

    @app.route("/api/member/<name>/income", methods=["POST"])
    def set_income(name):
        """Update member income."""
        data = request.json or {}
        result = jarvis.set_member_income(name=name, monthly_income=data.get("income", 0))
        return jsonify(result)

    @app.route("/api/blockers", methods=["GET"])
    def get_blockers():
        """All family blockers."""
        return jsonify(jarvis.unified_blockers())

    @app.route("/api/snapshot", methods=["GET"])
    def get_snapshot():
        """Progress snapshot."""
        return jsonify(jarvis.progress_snapshot())

    @app.route("/health", methods=["GET"])
    def health():
        """Health check."""
        return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
