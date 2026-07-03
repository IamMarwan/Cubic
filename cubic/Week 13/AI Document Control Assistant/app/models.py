from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class WorkflowState(str, Enum):
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    APPROVED = "Approved"
    ISSUED = "Issued"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"


ALLOWED_TRANSITIONS: Dict[WorkflowState, List[WorkflowState]] = {
    WorkflowState.DRAFT: [WorkflowState.IN_REVIEW, WorkflowState.ARCHIVED],
    WorkflowState.IN_REVIEW: [WorkflowState.APPROVED, WorkflowState.REJECTED, WorkflowState.DRAFT],
    WorkflowState.REJECTED: [WorkflowState.DRAFT, WorkflowState.ARCHIVED],
    WorkflowState.APPROVED: [WorkflowState.ISSUED, WorkflowState.ARCHIVED],
    WorkflowState.ISSUED: [WorkflowState.ARCHIVED],
    WorkflowState.ARCHIVED: [],
}


@dataclass
class Document:
    id: Optional[int]
    title: str
    document_number: str
    revision: str
    discipline: str
    document_type: str
    status: WorkflowState
    content: str
    owner: str
    project: str
    ai_confidence: float
    risk_score: float
    created_at: str
    updated_at: str
    due_date: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value if isinstance(self.status, WorkflowState) else self.status
        return data


@dataclass
class AuditEvent:
    id: Optional[int]
    document_id: int
    actor: str
    action: str
    from_state: Optional[str]
    to_state: Optional[str]
    comment: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def validate_transition(current: WorkflowState, target: WorkflowState) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        allowed = ", ".join(state.value for state in ALLOWED_TRANSITIONS[current]) or "none"
        raise ValueError(f"Invalid workflow transition from {current.value} to {target.value}. Allowed: {allowed}.")
