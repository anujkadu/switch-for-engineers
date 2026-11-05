# ruff: noqa: E501
import logging
import os
import sys
import uuid
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer

from efs.config import Settings
from efs.db import create_engine_for, create_session_factory
from efs.mcp.errors import error_response
from efs.mcp.serialization import decision, definition, session
from efs.missions.registry import MissionRegistry
from efs.missions.sample import SAMPLE_MISSION
from efs.services.mission_service import MissionService


def build_server(profile: Literal["orchestrator", "specialist"] = "orchestrator") -> MCPServer:
    if profile not in {"orchestrator", "specialist"}:
        raise ValueError("EFS_MCP_PROFILE must be orchestrator or specialist")
    settings = Settings()
    registry = MissionRegistry([SAMPLE_MISSION])
    service = MissionService(create_session_factory(create_engine_for(settings)), registry)
    server = MCPServer(name=f"efs-backend-{profile}", version="0.3.0")

    def safe(fn):
        try:
            return fn()
        except Exception as exc:
            return error_response(exc)

    @server.tool(name="get_mission", description="Return an exact-version mission definition.")
    def get_mission(mission_id: str, mission_version: str) -> dict[str, Any]:
        return safe(lambda: {"ok": True, "mission": definition(registry.get(mission_id, mission_version))})

    @server.tool(name="get_mission_progress", description="Return owned authoritative mission progress.")
    def get_mission_progress(learner_id: str, session_id: str) -> dict[str, Any]:
        return safe(lambda: {"ok": True, "session": session(service.get_progress(uuid.UUID(session_id), learner_id))})

    @server.tool(name="get_decision_history", description="Return owned append-only decision history.")
    def get_decision_history(learner_id: str, session_id: str) -> dict[str, Any]:
        return safe(lambda: {"ok": True, "decisions": [decision(x) for x in service.get_decision_history(uuid.UUID(session_id), learner_id)]})

    if profile == "orchestrator":
        @server.tool(name="start_mission", description="Start or resume a mission.")
        def start_mission(learner_id: str, mission_id: str, mission_version: str) -> dict[str, Any]:
            return safe(lambda: {"ok": True, "session": session(service.start_mission(learner_id, mission_id, mission_version))})

        @server.tool(name="submit_learner_decision", description="Persist the learner's explicit decision.")
        def submit_learner_decision(learner_id: str, session_id: str, content: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
            return safe(lambda: {"ok": True, "decision": decision(service.submit_decision(uuid.UUID(session_id), learner_id, content, idempotency_key))})

        @server.tool(name="advance_mission_stage", description="Advance only when the backend rule is satisfied.")
        def advance_mission_stage(learner_id: str, session_id: str) -> dict[str, Any]:
            return safe(lambda: {"ok": True, "session": session(service.advance_stage(uuid.UUID(session_id), learner_id))})

        @server.tool(name="complete_mission", description="Complete a satisfied final stage.")
        def complete_mission(learner_id: str, session_id: str) -> dict[str, Any]:
            return safe(lambda: {"ok": True, "session": session(service.complete_mission(uuid.UUID(session_id), learner_id))})

        @server.tool(name="abandon_mission", description="Abandon an active mission.")
        def abandon_mission(learner_id: str, session_id: str) -> dict[str, Any]:
            return safe(lambda: {"ok": True, "session": session(service.abandon_mission(uuid.UUID(session_id), learner_id))})
    return server


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=os.getenv("EFS_LOG_LEVEL", "INFO"))
    build_server(os.getenv("EFS_MCP_PROFILE", "orchestrator")).run("stdio")


if __name__ == "__main__":
    main()
