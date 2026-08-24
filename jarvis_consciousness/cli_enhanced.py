"""Enhanced CLI — Full Jarvis capabilities with world knowledge + psychology + family."""
import json
from pathlib import Path

from jarvis_consciousness.api import JarvisAPI
from jarvis_consciousness.family_consciousness import FamilyConsciousness
from jarvis_consciousness.knowledge_engine import PsychologicalModel, ReasoningEngine, WorldKnowledge


def family_briefing():
    """Family-level weekly briefing."""
    api = JarvisAPI()
    brief = api.family_briefing()

    print("\n" + "=" * 80)
    print("👨‍👩‍👧‍👦 FAMILY CONSCIOUSNESS — UNIFIED BRIEFING")
    print("=" * 80)

    print(f"\n🎯 FAMILY GOAL: {brief['goal']}")
    print(f"\n📊 FAMILY PROGRESS: {brief['progress_percent']}%")
    print(f"   Current: ₹{brief['family_progress']['total_current_monthly']:,}/month")
    print(f"   Target: ₹{brief['family_progress']['total_target_monthly']:,}/month")
    print(f"   Gap: ₹{brief['family_progress']['total_gap']:,}/month")

    print(f"\n⚡ CRITICAL PATH THIS WEEK:")
    print(f"   {brief['critical_path']['this_week_action']}")

    print(f"\n👤 EACH MEMBER:")
    for name, member_brief in brief["each_member"].items():
        print(f"\n   {member_brief['name'].upper()} ({member_brief['role']})")
        print(f"   Goal: {member_brief['goal'][:60]}...")
        if member_brief["target"]:
            print(f"   Target: ₹{member_brief['target']:,}/month")
            print(f"   Current: ₹{member_brief['current']:,}/month")
            print(f"   Gap: ₹{member_brief['gap']:,}/month")
        print(f"   Success rate: {int(member_brief['success_rate'] * 100)}%")
        if member_brief["blocker"]:
            print(f"   Blocker: {member_brief['blocker']}")

    print("\n" + "=" * 80)
    return brief


def psychology_analysis():
    """Psychological analysis (rejection aversion, decision patterns)."""
    api = JarvisAPI()
    outcomes_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"

    # Load outcomes
    outcomes = []
    if outcomes_path.exists():
        with open(outcomes_path) as f:
            for line in f:
                if line.strip():
                    outcomes.append(json.loads(line))

    print("\n" + "=" * 80)
    print("🧠 PSYCHOLOGICAL ANALYSIS")
    print("=" * 80)

    # Rejection aversion diagnosis
    diagnosis = PsychologicalModel.diagnose_rejection_aversion(outcomes)
    print(f"\n📋 REJECTION AVERSION:")
    print(f"   Building actions: {diagnosis['building_actions']}")
    print(f"   Asking actions: {diagnosis['asking_actions']}")
    print(f"   Build-to-ask ratio: {diagnosis['build_to_ask_ratio']:.1f}:1")
    print(f"   Diagnosis: {diagnosis['diagnosis']}")
    print(f"   Recommendation: {diagnosis['recommendation']}")

    # Best approach
    print(f"\n💡 BEST APPROACH FOR YOU:")
    approaches = [
        PsychologicalModel.best_approach_for_person("early_morning"),
        PsychologicalModel.best_approach_for_person("broker_intro"),
        PsychologicalModel.best_approach_for_person("personal_relationship"),
    ]

    for approach in approaches:
        print(f"\n   {approach['description']}")
        print(f"   Success rate: {int(approach['success_rate'] * 100)}%")
        print(f"   Why: {approach['why']}")

    print("\n" + "=" * 80)
    return diagnosis


def world_knowledge(asset_class: str = "crude_oil"):
    """World knowledge about markets, deals, trades."""
    print("\n" + "=" * 80)
    print(f"🌍 WORLD KNOWLEDGE — {asset_class.upper()}")
    print("=" * 80)

    market = WorldKnowledge.market_insight(asset_class)
    print(f"\n📊 Market snapshot:")
    for key, value in market.items():
        print(f"   {key}: {value}")

    # Deal playbook
    print(f"\n📖 DEAL ACCELERATION PLAYBOOK:")
    for blocker, advice in WorldKnowledge.DEAL_PLAYBOOK.items():
        print(f"\n   {blocker.upper().replace('_', ' ')}:")
        print(f"   Typical duration: {advice['typical_duration']}")
        print(f"   Bottleneck: {advice['bottleneck']}")
        print(f"   Acceleration: {advice['acceleration_tactic']}")

    print("\n" + "=" * 80)
    return market


def ai_analysis():
    """AI reasoning over your outcomes."""
    api = JarvisAPI()
    outcomes_path = Path(__file__).parent.parent / "data" / "outcomes.jsonl"

    # Load outcomes
    outcomes = []
    if outcomes_path.exists():
        with open(outcomes_path) as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if "outcome" in entry:
                        outcomes.append(entry)

    print("\n" + "=" * 80)
    print("🤖 AI REASONING ENGINE")
    print("=" * 80)

    if not outcomes:
        print("\nNo outcomes to analyze yet. Take action and report back!")
        return

    # Pattern analysis
    patterns = ReasoningEngine.pattern_from_outcomes(outcomes)
    print(f"\n📊 PATTERN ANALYSIS ({patterns['total_outcomes']} outcomes):")
    print(f"   Success rate: {int(patterns['success_count'] / patterns['total_outcomes'] * 100)}%")

    print(f"\n📈 By method:")
    for method, stats in patterns["methods"].items():
        rate = int(stats["success_rate"] * 100)
        print(f"   {method}: {rate}% success ({stats['total']} attempts)")

    print(f"\n   Best method: {patterns['best_method']}")

    # Recommendation
    print(f"\n💡 NEXT ACTION RECOMMENDATION:")
    rec = ReasoningEngine.next_action_recommendation(
        blocker="₹100Cr deal papers",
        outcomes_history=outcomes,
    )
    print(f"   Blocker: {rec['blocker']}")
    print(f"   Suggested method: {rec['suggested_method']}")
    print(f"   Success probability: {int(rec['success_probability'] * 100)}%")
    print(f"   Why: {rec['why']}")
    print(f"   Tactic: {rec['acceleration_tactic']}")
    print(f"   Urgency: {rec['urgency']}")

    print("\n" + "=" * 80)
    return patterns


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        family_briefing()
    elif sys.argv[1] == "family":
        family_briefing()
    elif sys.argv[1] == "psychology":
        psychology_analysis()
    elif sys.argv[1] == "knowledge":
        asset = sys.argv[2] if len(sys.argv) > 2 else "crude_oil"
        world_knowledge(asset)
    elif sys.argv[1] == "ai":
        ai_analysis()
    else:
        print("Usage:")
        print("  python -m jarvis_consciousness.cli_enhanced family")
        print("  python -m jarvis_consciousness.cli_enhanced psychology")
        print("  python -m jarvis_consciousness.cli_enhanced knowledge [asset_class]")
        print("  python -m jarvis_consciousness.cli_enhanced ai")
