from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterable, List, Optional
from app.models import AuditEvent, Document, WorkflowState

DB_PATH = Path(__file__).resolve().parents[1] / "document_control.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                document_number TEXT NOT NULL UNIQUE,
                revision TEXT NOT NULL,
                discipline TEXT NOT NULL,
                document_type TEXT NOT NULL,
                status TEXT NOT NULL,
                content TEXT NOT NULL,
                owner TEXT NOT NULL,
                project TEXT NOT NULL,
                ai_confidence REAL NOT NULL,
                risk_score REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                due_date TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                from_state TEXT,
                to_state TEXT,
                comment TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
            """
        )
        conn.commit()


def reset_db(db_path: Path = DB_PATH) -> None:
    if db_path.exists():
        db_path.unlink()
    init_db(db_path)


def _row_to_document(row: sqlite3.Row) -> Document:
    return Document(
        id=row["id"], title=row["title"], document_number=row["document_number"],
        revision=row["revision"], discipline=row["discipline"], document_type=row["document_type"],
        status=WorkflowState(row["status"]), content=row["content"], owner=row["owner"], project=row["project"],
        ai_confidence=row["ai_confidence"], risk_score=row["risk_score"],
        created_at=row["created_at"], updated_at=row["updated_at"], due_date=row["due_date"]
    )


def insert_document(doc: Document, db_path: Path = DB_PATH) -> Document:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO documents (title, document_number, revision, discipline, document_type, status, content,
            owner, project, ai_confidence, risk_score, created_at, updated_at, due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (doc.title, doc.document_number, doc.revision, doc.discipline, doc.document_type, doc.status.value,
             doc.content, doc.owner, doc.project, doc.ai_confidence, doc.risk_score, doc.created_at, doc.updated_at,
             doc.due_date),
        )
        conn.commit()
        doc.id = cur.lastrowid
        return doc


def list_documents(db_path: Path = DB_PATH) -> List[Document]:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM documents ORDER BY updated_at DESC").fetchall()
    return [_row_to_document(row) for row in rows]


def get_document(document_id: int, db_path: Path = DB_PATH) -> Optional[Document]:
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
    return _row_to_document(row) if row else None


def update_document_status(document_id: int, status: WorkflowState, updated_at: str, db_path: Path = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute("UPDATE documents SET status = ?, updated_at = ? WHERE id = ?", (status.value, updated_at, document_id))
        conn.commit()


def insert_audit_event(event: AuditEvent, db_path: Path = DB_PATH) -> AuditEvent:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO audit_events (document_id, actor, action, from_state, to_state, comment, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (event.document_id, event.actor, event.action, event.from_state, event.to_state, event.comment, event.created_at),
        )
        conn.commit()
        event.id = cur.lastrowid
        return event


def list_audit_events(document_id: Optional[int] = None, db_path: Path = DB_PATH) -> List[AuditEvent]:
    with get_connection(db_path) as conn:
        if document_id is None:
            rows = conn.execute("SELECT * FROM audit_events ORDER BY created_at DESC").fetchall()
        else:
            rows = conn.execute("SELECT * FROM audit_events WHERE document_id = ? ORDER BY created_at DESC", (document_id,)).fetchall()
    return [AuditEvent(**dict(row)) for row in rows]
