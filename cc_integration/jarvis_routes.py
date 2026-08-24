"""Jarvis routes for Command Center."""
from flask import Blueprint, jsonify, request
from .jarvis_client import JarvisClient

jarvis_bp = Blueprint("jarvis", __name__)
jarvis_client = JarvisClient()


@jarvis_bp.route("/briefing", methods=["GET"])
def get_briefing():
    """Shreyas's weekly briefing."""
    income = request.args.get("income", 92000, type=int)
    result = jarvis_client.briefing(income)
    return jsonify(result)


@jarvis_bp.route("/family/briefing", methods=["GET"])
def get_family_briefing():
    """Family-level briefing."""
    result = jarvis_client.family_briefing()
    return jsonify(result)


@jarvis_bp.route("/snapshot", methods=["GET"])
def get_snapshot():
    """Progress snapshot for dashboards."""
    result = jarvis_client.snapshot()
    return jsonify(result)


@jarvis_bp.route("/outcome", methods=["POST"])
def record_outcome():
    """Record an action outcome."""
    data = request.json or {}
    result = jarvis_client.record_outcome(
        action=data.get("action", ""),
        outcome=data.get("outcome", ""),
        person=data.get("person", "shreyas"),
        details=data.get("details"),
    )
    return jsonify(result), 201


@jarvis_bp.route("/member/<name>/briefing", methods=["GET"])
def get_member_briefing(name):
    """Get briefing for one family member."""
    result = jarvis_client.member_briefing(name)
    return jsonify(result)


@jarvis_bp.route("/member/<name>/blocker", methods=["POST"])
def set_member_blocker(name):
    """Update member's blocker."""
    data = request.json or {}
    result = jarvis_client.set_member_blocker(
        name=name,
        blocker=data.get("blocker", ""),
        priority=data.get("priority", "HIGH"),
    )
    return jsonify(result)


@jarvis_bp.route("/member/<name>/income", methods=["POST"])
def set_member_income(name):
    """Update member's current income."""
    data = request.json or {}
    result = jarvis_client.set_member_income(
        name=name,
        monthly_income=data.get("income", 0),
    )
    return jsonify(result)


@jarvis_bp.route("/blockers", methods=["GET"])
def get_blockers():
    """Get all family blockers."""
    result = jarvis_client.blockers()
    return jsonify(result)


@jarvis_bp.route("/decision/<gate_name>", methods=["GET"])
def get_decision(gate_name):
    """Ask Jarvis about a decision."""
    result = jarvis_client.decision(gate_name)
    return jsonify(result)


@jarvis_bp.route("/health", methods=["GET"])
def health():
    """Health check."""
    health_ok = jarvis_client.health()
    return jsonify({"status": "ok" if health_ok else "jarvis_unreachable"}), 200 if health_ok else 503


# To register in your Flask app:
# from cc_integration.jarvis_routes import jarvis_bp
# app.register_blueprint(jarvis_bp, url_prefix="/api/jarvis")
