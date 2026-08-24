"""Jarvis Client for Command Center integration."""
import json
import requests
from typing import Any, Optional


class JarvisClient:
    """Talk to Jarvis Consciousness API from Command Center."""

    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    def health(self) -> bool:
        """Check if Jarvis API is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def briefing(self, current_income: int = 92000) -> dict:
        """Get Shreyas's weekly briefing."""
        try:
            response = requests.get(
                f"{self.base_url}/api/briefing",
                params={"income": current_income},
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def family_briefing(self) -> dict:
        """Get family-level briefing."""
        try:
            response = requests.get(
                f"{self.base_url}/api/family/briefing",
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def snapshot(self) -> dict:
        """Get progress snapshot (for dashboards)."""
        try:
            response = requests.get(
                f"{self.base_url}/api/snapshot",
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def record_outcome(
        self,
        action: str,
        outcome: str,
        person: str = "shreyas",
        details: Optional[dict] = None,
    ) -> dict:
        """Record an action outcome."""
        try:
            response = requests.post(
                f"{self.base_url}/api/outcome",
                json={
                    "action": action,
                    "outcome": outcome,
                    "person": person,
                    "details": details or {},
                },
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def member_briefing(self, name: str) -> dict:
        """Get briefing for one family member."""
        try:
            response = requests.get(
                f"{self.base_url}/api/member/{name}/briefing",
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def set_member_blocker(self, name: str, blocker: str, priority: str = "HIGH") -> dict:
        """Update member's blocker."""
        try:
            response = requests.post(
                f"{self.base_url}/api/member/{name}/blocker",
                json={"blocker": blocker, "priority": priority},
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def set_member_income(self, name: str, monthly_income: int) -> dict:
        """Update member's current income."""
        try:
            response = requests.post(
                f"{self.base_url}/api/member/{name}/income",
                json={"income": monthly_income},
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def blockers(self) -> dict:
        """Get all family blockers."""
        try:
            response = requests.get(
                f"{self.base_url}/api/blockers",
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def decision(self, gate_name: str) -> dict:
        """Ask Jarvis about a decision."""
        try:
            response = requests.get(
                f"{self.base_url}/api/decision/{gate_name}",
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def webhook_handler(self, source: str, data: dict) -> dict:
        """Handle webhook from external source."""
        try:
            response = requests.post(
                f"{self.base_url}/api/webhook",
                json={"source": source, "data": data},
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
