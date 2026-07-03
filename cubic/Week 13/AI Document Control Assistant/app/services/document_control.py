from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from app.database import get_document, insert_audit_event, insert_document, list_audit_events, list_documents, update_document_status
from app.models import AuditEvent, Document, WorkflowState, now_iso, validate_transition
from app.services.ai_engine import extract_metadata


def create_document_from_text(content: str, filename: str, owner: str, project: str, due_date: Optional[str] = None) -> Document:
    ai = extract_metadata(content, filename)
    timestamp = now_iso()
    doc = Document(
        id=None,
        title=ai.title,
        document_number=ai.document_number,
        revision=ai.revision,
        discipline=ai.discipline,
        document_type=ai.document_type,
        status=WorkflowState.DRAFT,
        content=content,
        owner=owner,
        project=project,
        ai_confidence=ai.confidence,
        risk_score=ai.risk_score,
        created_at=timestamp,
        updated_at=timestamp,
        due_date=due_date,
    )
    saved = insert_document(doc)
    insert_audit_event(AuditEvent(None, saved.id, owner, "Created", None, WorkflowState.DRAFT.value, "Document created and classified by AI assistant.", timestamp))
    return saved


def transition_document(document_id: int, target_state: WorkflowState, actor: str, comment: str) -> Document:
    doc = get_document(document_id)
    if not doc:
        raise LookupError(f"Document {document_id} was not found.")
    validate_transition(doc.status, target_state)
    timestamp = now_iso()
    update_document_status(document_id, target_state, timestamp)
    insert_audit_event(AuditEvent(None, document_id, actor, "State Transition", doc.status.value, target_state.value, comment, timestamp))
    updated = get_document(document_id)
    assert updated is not None
    return updated


def get_register() -> List[Document]:
    return list_documents()


def get_audit_trail(document_id: Optional[int] = None) -> list[AuditEvent]:
    return list_audit_events(document_id)
