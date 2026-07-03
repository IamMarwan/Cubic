from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, List
from app.models import Document


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def build_summary(documents: List[Document]) -> Dict:
    total = len(documents)
    by_status = Counter(doc.status.value for doc in documents)
    by_discipline = Counter(doc.discipline for doc in documents)
    by_type = Counter(doc.document_type for doc in documents)
    avg_confidence = round(sum(doc.ai_confidence for doc in documents) / total, 2) if total else 0
    avg_risk = round(sum(doc.risk_score for doc in documents) / total, 2) if total else 0
    high_risk = sum(1 for doc in documents if doc.risk_score >= 0.5)
    now = datetime.now(timezone.utc)
    overdue = 0
    for doc in documents:
        due = _parse_date(doc.due_date)
        if due and due < now and doc.status.value not in {"Approved", "Issued", "Archived"}:
            overdue += 1
    return {
        "total_documents": total,
        "by_status": dict(by_status),
        "by_discipline": dict(by_discipline),
        "by_type": dict(by_type),
        "average_ai_confidence": avg_confidence,
        "average_risk_score": avg_risk,
        "high_risk_documents": high_risk,
        "overdue_reviews": overdue,
    }


def reporting_rows(documents: List[Document]) -> list[dict]:
    return [doc.to_dict() for doc in documents]
