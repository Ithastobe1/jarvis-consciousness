"""CLI — Your weekly interface to Jarvis Consciousness."""
import json
from pathlib import Path

from jarvis_consciousness.bottleneck_detector import BottleneckDetector
from jarvis_consciousness.goal_engine import GoalEngine
from jarvis_consciousness.outcome_learner import OutcomeListener


def briefing(current_income: int = 92000):
    """Your weekly briefing."""
    engine = GoalEngine()
    weekly = engine.weekly_briefing(current_income)

    print("\n" + "=" * 70)
    print("🧠 JARVIS CONSCIOUSNESS — WEEKLY BRIEFING")
    print("=" * 70)
    print(f"\n📍 YOUR GOAL: {weekly['goal']}")
    print(f"\n📊 PROGRESS: {weekly['progress']['score']}%")
    print(f"   Target: ₹{weekly['progress']['target']:,}/month")
    print(f"   Current: ₹{weekly['progress']['current']:,}/month")
    print(f"   Gap: ₹{weekly['progress']['gap']:,}/month")
    print(f"   Days left: {weekly['progress']['days_remaining']} days")
    print(f"   Urgency: {weekly['progress']['urgency_phase']}")

    print(f"\n🎯 TOP LEVER THIS WEEK: {weekly['top_lever']['name']}")
    print(f"   Potential: ₹{weekly['top_lever']['potential_monthly']:,}/month")
    print(f"   Status: {weekly['top_lever']['status']}")
    print(f"   Priority: {weekly['top_lever']['priority']}")

    print(f"\n⚠️  BLOCKER: {weekly['blocker']['current_blocker']}")
    print(f"   Action: {weekly['blocker']['action_needed']}")

    print(f"\n💡 JARVIS SAYS:\n{weekly['jarvis_says']}\n")
    print("=" * 70)

    return weekly


def detect_blockers():
    """What's actually blocking you."""
    blueprint_path = Path(__file__).parent.parent / "data" / "master_blueprint.json"
    with open(blueprint_path) as f:
        blueprint = json.load(f)

    detector = BottleneckDetector(blueprint)
    result = detector.detect()

    print("\n" + "=" * 70)
    print("🔍 BOTTLENECK ANALYSIS")
    print("=" * 70)
    print(f"\n📋 Root cause: {result['root_cause']}")
    print(f"\n📊 Diagnosis:\n{result['diagnosis']}")
    print(f"\n💊 Prescription:\n{result['prescription']}")

    if result["active_blockers"]:
        print("\n🚧 Active blockers (ranked by impact):")
        for i, blocker in enumerate(result["active_blockers"][:3], 1):
            print(f"   {i}. {blocker['lever']}")
            print(f"      Type: {blocker['blocker_type']}")
            print(f"      Blocker: {blocker['blocker_text']}")
            print(f"      Action: {blocker['action']}")
            print(f"      Impact if unblocked: ₹{blocker['cost_monthly']:,}/month")

    print("\n" + "=" * 70)
    return result


def record_outcome(action: str, outcome: str, details: str = ""):
    """Record what happened when you tried something."""
    learner = OutcomeListener()
    entry = learner.record(action, outcome, {"notes": details})

    print(f"✅ Recorded: {action} → {outcome}")
    print(f"   Timestamp: {entry['timestamp']}")
    print(f"   Log: {learner.log_path}")

    return entry


def what_works():
    """What patterns are working?"""
    learner = OutcomeListener()
    learnings = learner.learn()

    print("\n" + "=" * 70)
    print("📚 JARVIS LEARNINGS — WHAT WORKS")
    print("=" * 70)

    if "message" in learnings:
        print(f"\n{learnings['message']}")
    else:
        print(f"\n📊 Total actions tracked: {learnings['total_actions_tracked']}")
        print(f"\n✅ What works:")
        for item in learnings["what_works"].get("action_scores", [])[:3]:
            rate = int(item["success_rate"] * 100)
            print(f"   • {item['action_type']}: {rate}% success")

        print(f"\n💡 Jarvis says: {learnings['jarvis_says']}")

    print("\n" + "=" * 70)
    return learnings


def decision(gate_name: str):
    """Ask Jarvis for a decision."""
    engine = GoalEngine()
    gate = engine.decision_gate(gate_name)

    print("\n" + "=" * 70)
    print(f"🤔 DECISION: {gate.get('gate', gate_name)}")
    print("=" * 70)

    if "error" in gate:
        print(f"\n❌ {gate['error']}")
    else:
        print(f"\nQuestion: {gate.get('decision', 'N/A')}")
        print(f"\n💡 Jarvis recommendation: {gate.get('jarvis_recommendation', 'N/A')}")
        print(f"\nNext action: {gate.get('next_action', 'N/A')}")

    print("\n" + "=" * 70)
    return gate


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        briefing()
    elif sys.argv[1] == "briefing":
        briefing()
    elif sys.argv[1] == "blockers":
        detect_blockers()
    elif sys.argv[1] == "learnings":
        what_works()
    elif sys.argv[1] == "record" and len(sys.argv) >= 4:
        record_outcome(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif sys.argv[1] == "decision" and len(sys.argv) >= 3:
        decision(" ".join(sys.argv[2:]))
    else:
        print("Usage:")
        print("  python -m jarvis_consciousness.cli briefing")
        print("  python -m jarvis_consciousness.cli blockers")
        print("  python -m jarvis_consciousness.cli learnings")
        print("  python -m jarvis_consciousness.cli record '<action>' '<outcome>'")
        print("  python -m jarvis_consciousness.cli decision '<gate name>'")
