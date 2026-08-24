"""Multi-Person Consciousness — Track goals for Shreyas, Pallavi, Maa, Father.

One unified goal engine that understands the FAMILY exit plan, not just
an individual. Each person's goals feed into shared targets.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class FamilyMember:
    """One person's goals and progress toward family exit."""

    def __init__(self, name: str, role: str, goal: str, target_monthly_income: int = 0):
        self.name = name
        self.role = role  # "founder" | "operator" | "investor" | "advisor"
        self.goal = goal
        self.target_monthly_income = target_monthly_income
        self.current_monthly_income = 0
        self.actions = []
        self.outcomes = []
        self.blockers = []

    def record_action(self, action: str, outcome: str, details: dict = None):
        """Record an action this person took."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "person": self.name,
            "action": action,
            "outcome": outcome,
            "details": details or {},
        }
        self.actions.append(entry)
        if outcome in ["success", "partial"]:
            self.outcomes.append(entry)
        return entry

    def set_blocker(self, blocker: str, priority: str = "HIGH"):
        """What's blocking this person."""
        self.blockers = [{
            "timestamp": datetime.now().isoformat(),
            "blocker": blocker,
            "priority": priority,
        }]

    def to_dict(self) -> dict:
        """Serialize to JSON."""
        return {
            "name": self.name,
            "role": self.role,
            "goal": self.goal,
            "target_monthly_income": self.target_monthly_income,
            "current_monthly_income": self.current_monthly_income,
            "actions_count": len(self.actions),
            "success_count": len(self.outcomes),
            "success_rate": len(self.outcomes) / len(self.actions) if self.actions else 0,
            "current_blocker": self.blockers[0] if self.blockers else None,
        }


class FamilyConsciousness:
    """Family-level goal engine. Each person's goals + unified family exit."""

    def __init__(self, blueprint_path: str | Path = None):
        """Initialize with master blueprint + family setup."""
        if blueprint_path is None:
            blueprint_path = Path(__file__).parent.parent / "data" / "master_blueprint.json"

        with open(blueprint_path) as f:
            self.blueprint = json.load(f)

        # Define family members and their goals
        self.shreyas = FamilyMember(
            name="Shreyas",
            role="founder",
            goal="₹1Cr/mo + family exit + trade/wealth/property verticals",
            target_monthly_income=10000000,  # ₹1Cr
        )
        self.shreyas.current_monthly_income = 92000

        self.pallavi = FamilyMember(
            name="Pallavi",
            role="operator",
            goal="Post-Oct 2026: board seat / advisor role (₹5–10L/mo potential)",
            target_monthly_income=500000,  # ₹5L minimum
        )
        self.pallavi.current_monthly_income = 0  # Off work from Oct 2026

        self.maa = FamilyMember(
            name="Shveta (Maa)",
            role="advisor",
            goal="Property coordination + TM (trademark) + family decisions",
            target_monthly_income=0,  # No income target
        )

        self.father = FamilyMember(
            name="Father",
            role="investor",
            goal="Trade operations (CUOMNS/crude) + MSP ladder",
            target_monthly_income=2000000,  # ₹20L from trade
        )
        self.father.current_monthly_income = 500000

        self.members = {
            "shreyas": self.shreyas,
            "pallavi": self.pallavi,
            "maa": self.maa,
            "father": self.father,
        }

    def family_progress(self) -> dict[str, Any]:
        """Combined progress toward family exit."""
        total_current = sum(m.current_monthly_income for m in self.members.values())
        total_target = sum(m.target_monthly_income for m in self.members.values())
        gap = total_target - total_current

        return {
            "timestamp": datetime.now().isoformat(),
            "total_current_monthly": total_current,
            "total_target_monthly": total_target,
            "total_gap": gap,
            "members": {name: member.to_dict() for name, member in self.members.items()},
            "family_exit_ready": gap <= 1000000,  # Within ₹10L
            "status": "ON_TRACK" if gap > 0 else "ACHIEVED",
        }

    def unified_blockers(self) -> list[dict]:
        """All family blockers ranked by impact."""
        all_blockers = []

        for member in self.members.values():
            if member.blockers:
                blocker = member.blockers[0]
                blocker["person"] = member.name
                blocker["role"] = member.role
                all_blockers.append(blocker)

        return sorted(all_blockers, key=lambda x: x.get("priority", "LOW"))

    def weekly_family_briefing(self) -> dict[str, Any]:
        """What the FAMILY needs to do this week."""
        progress = self.family_progress()
        blockers = self.unified_blockers()

        # Identify the critical path blocker (highest impact across family)
        critical_blocker = blockers[0] if blockers else None

        return {
            "week": datetime.now().isoformat(),
            "goal": "Family exit + ₹1Cr+/mo + Pallavi transition",
            "family_progress": progress,
            "progress_percent": int((progress["total_current_monthly"] / progress["total_target_monthly"]) * 100)
            if progress["total_target_monthly"] > 0
            else 0,
            "critical_path": {
                "blocker": critical_blocker.get("blocker", "None identified") if critical_blocker else "All clear",
                "owner": critical_blocker.get("person", "TBD") if critical_blocker else "N/A",
                "this_week_action": self._recommend_this_week(),
            },
            "each_member": {
                "shreyas": self._member_brief(self.shreyas),
                "pallavi": self._member_brief(self.pallavi),
                "maa": self._member_brief(self.maa),
                "father": self._member_brief(self.father),
            },
        }

    def _member_brief(self, member: FamilyMember) -> dict:
        """Brief for one family member."""
        return {
            "name": member.name,
            "role": member.role,
            "goal": member.goal,
            "current": member.current_monthly_income,
            "target": member.target_monthly_income,
            "gap": member.target_monthly_income - member.current_monthly_income,
            "success_rate": len(member.outcomes) / len(member.actions) if member.actions else 0,
            "blocker": member.blockers[0]["blocker"] if member.blockers else "None",
        }

    def _recommend_this_week(self) -> str:
        """Unified recommendation for what family should do this week."""
        shreyas_blocker = self.shreyas.blockers[0]["blocker"] if self.shreyas.blockers else None
        pallavi_blocker = self.pallavi.blockers[0]["blocker"] if self.pallavi.blockers else None
        maa_blocker = self.maa.blockers[0]["blocker"] if self.maa.blockers else None
        father_blocker = self.father.blockers[0]["blocker"] if self.father.blockers else None

        # Critical path: Shreyas closes ₹100Cr, Pallavi decides post-exit, Maa signs papers
        if shreyas_blocker and "100Cr" in shreyas_blocker:
            return f"Shreyas: {shreyas_blocker} | Pallavi: {pallavi_blocker or 'Standby'} | Maa: {maa_blocker or 'Standby'}"
        elif pallavi_blocker and "post" in pallavi_blocker.lower():
            return f"Pallavi: {pallavi_blocker} | Shreyas: {shreyas_blocker or 'Standby'} | Maa: {maa_blocker or 'Standby'}"
        else:
            return f"Shreyas: {shreyas_blocker or 'Push ₹100Cr'} | Pallavi: {pallavi_blocker or 'Plan post-Oct'} | Maa: {maa_blocker or 'Coordinate papers'}"

    def sync_outcomes(self, outcomes_log_path: str | Path):
        """Sync individual outcomes from outcomes.jsonl into family consciousness."""
        if outcomes_log_path is None:
            outcomes_log_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"

        outcomes_log_path = Path(outcomes_log_path)
        if not outcomes_log_path.exists():
            return {"synced": 0}

        synced = 0
        with open(outcomes_log_path) as f:
            for line in f:
                if not line.strip():
                    continue

                outcome = json.loads(line)
                action = outcome.get("action", "").lower()

                # Route to correct family member based on action keywords
                if any(word in action for word in ["shreyas", "deal", "broker", "commission"]):
                    self.shreyas.record_action(
                        outcome["action"],
                        outcome["outcome"],
                        outcome.get("details"),
                    )
                    synced += 1
                elif any(word in action for word in ["pallavi", "board", "advisor", "exit"]):
                    self.pallavi.record_action(
                        outcome["action"],
                        outcome["outcome"],
                        outcome.get("details"),
                    )
                    synced += 1
                elif any(word in action for word in ["maa", "property", "papers", "papers", "signature"]):
                    self.maa.record_action(
                        outcome["action"],
                        outcome["outcome"],
                        outcome.get("details"),
                    )
                    synced += 1
                elif any(word in action for word in ["father", "trade", "cuomns", "crude"]):
                    self.father.record_action(
                        outcome["action"],
                        outcome["outcome"],
                        outcome.get("details"),
                    )
                    synced += 1

        return {"synced": synced, "total_outcomes": synced}
