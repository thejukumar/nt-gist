"""HTTP routes for the comparison API.

Functional in the scaffold: /health, /session/start, GET /session/{id}, /demo/run.
Stubbed until later branches: /chat/turn (needs agents), /report/{id} (needs reporting).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..pruning.retention_policy import RetentionPolicy
from ..scenarios import load_scenario
from ..session_manager import SessionManager
from .dependencies import get_session_manager
from .schemas import (
    ChatTurnRequest,
    ChatTurnResponse,
    DemoRunRequest,
    DemoRunResponse,
    SessionStartRequest,
    SessionStartResponse,
)

router = APIRouter(prefix="/api", tags=["comparison"])


@router.post("/session/start", response_model=SessionStartResponse)
def start_session(
    body: SessionStartRequest,
    sessions: SessionManager = Depends(get_session_manager),
) -> SessionStartResponse:
    """Create a new comparison session with default or custom retention policy."""
    policy = (
        RetentionPolicy(**body.retention_policy.model_dump())
        if body.retention_policy
        else RetentionPolicy()
    )
    session = sessions.create(
        retention_policy=policy,
        prune_every=body.prune_every,
        recent_turns_to_keep=body.recent_turns_to_keep,
    )
    return SessionStartResponse(session_id=session.session_id)


@router.get("/session/{session_id}")
def get_session(
    session_id: str,
    sessions: SessionManager = Depends(get_session_manager),
) -> dict:
    """Return session state (turns/metrics fill in once agents are wired)."""
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session.session_id,
        "prune_every": session.prune_every,
        "recent_turns_to_keep": session.recent_turns_to_keep,
        "turns": session.turns,
    }


@router.post("/demo/run", response_model=DemoRunResponse)
def run_demo(body: DemoRunRequest) -> DemoRunResponse:
    """Return the scenario prompts; the frontend calls /chat/turn sequentially."""
    try:
        scenario = load_scenario(body.scenario)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None
    return DemoRunResponse(
        scenario=scenario.name,
        description=scenario.description,
        prompts=scenario.turns,
    )


@router.post("/chat/turn", response_model=ChatTurnResponse)
def chat_turn(
    body: ChatTurnRequest,
    sessions: SessionManager = Depends(get_session_manager),
) -> dict:
    """Run one prompt through both agents; return baseline + pruned + comparison."""
    session = sessions.get(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions.run_turn(session, body.message)


@router.get("/report/{session_id}")
def get_report(
    session_id: str,
    sessions: SessionManager = Depends(get_session_manager),
) -> dict:
    """Write JSON + Markdown reports for the session; return their paths."""
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    from ..reporting.json_logger import write_session_log
    from ..reporting.markdown_report import write_markdown_report

    json_path = write_session_log(session)
    md_path = write_markdown_report(session)
    return {
        "json_log_path": f"logs/{json_path.name}",
        "markdown_report_path": f"reports/{md_path.name}",
    }
