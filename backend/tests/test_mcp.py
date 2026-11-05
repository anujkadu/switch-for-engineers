import asyncio
import uuid

import pytest
from efs.mcp.errors import error_response
from efs.mcp.server import build_server


def test_profiles_expose_exact_capabilities(monkeypatch):
    monkeypatch.setenv("EFS_DATABASE_URL", "postgresql+psycopg://user:pass@localhost/db")

    async def names(profile):
        return {tool.name for tool in await build_server(profile).list_tools()}

    orchestrator = asyncio.run(names("orchestrator"))
    specialist = asyncio.run(names("specialist"))
    assert len(orchestrator) == 8
    assert len(specialist) == 3
    assert specialist <= orchestrator
    assert not specialist & {
        "start_mission", "submit_learner_decision", "advance_mission_stage",
        "complete_mission", "abandon_mission",
    }


def test_invalid_profile_is_rejected(monkeypatch):
    monkeypatch.setenv("EFS_DATABASE_URL", "postgresql+psycopg://user:pass@localhost/db")
    with pytest.raises(ValueError, match="EFS_MCP_PROFILE"):
        build_server("invalid")


@pytest.mark.parametrize(
    ("exception", "code"),
    [
        (ValueError("bad input"), "invalid_input"),
        (RuntimeError("secret password"), "internal_error"),
    ],
)
def test_error_responses_are_stable_and_safe(exception, code):
    response = error_response(exception)
    assert response["ok"] is False
    assert response["error"]["code"] == code
    if code == "internal_error":
        assert "password" not in response["error"]["message"]


def test_uuid_input_is_serializable():
    assert str(uuid.uuid4())
