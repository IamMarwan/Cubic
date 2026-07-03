from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

DISCIPLINE_KEYWORDS = {
    "Civil": ["concrete", "foundation", "road", "earthwork", "structure", "rebar"],
    "Mechanical": ["pump", "valve", "hvac", "duct", "pipe", "compressor"],
    "Electrical": ["cable", "switchgear", "lighting", "transformer", "panel", "earthing"],
    "Architectural": ["finish", "facade", "flooring", "ceiling", "door", "partition"],
    "HSE": ["safety", "risk", "permit", "incident", "hazard", "method statement"],
    "QA/QC": ["inspection", "test", "quality", "nonconformance", "itr", "checklist"],
}

TYPE_KEYWORDS = {
    "Drawing": ["drawing", "layout", "plan", "section", "elevation"],
    "Method Statement": ["method statement", "procedure", "sequence", "work steps"],
    "Inspection Report": ["inspection", "test report", "itr", "checklist"],
    "Material Submittal": ["material", "datasheet", "supplier", "submittal"],
    "Specification": ["specification", "requirements", "standard", "criteria"],
}

RISK_TERMS = ["critical", "urgent", "nonconformance", "safety", "hazard", "delay", "rework", "rejected", "overdue"]

@dataclass
class AIResult:
    title: str
    document_number: str
    revision: str
    discipline: str
    document_type: str
    confidence: float
    risk_score: float


def _score_keywords(text: str, keyword_map: Dict[str, List[str]]) -> Tuple[str, float]:
    normalized = text.lower()
    scores = {}
    for label, keywords in keyword_map.items():
        scores[label] = sum(1 for keyword in keywords if keyword in normalized)
    best_label, best_score = max(scores.items(), key=lambda item: item[1])
    total_hits = sum(scores.values())
    if best_score == 0:
        return "General", 0.45
    confidence = min(0.98, 0.55 + (best_score / max(1, total_hits)) * 0.40)
    return best_label, round(confidence, 2)


def extract_metadata(content: str, fallback_name: str = "Untitled Document") -> AIResult:
    title_match = re.search(r"(?:title|subject)\s*:\s*(.+)", content, re.IGNORECASE)
    number_match = re.search(r"(?:document number|doc no|number)\s*:\s*([A-Z0-9\-_/]+)", content, re.IGNORECASE)
    revision_match = re.search(r"(?:revision|rev)\s*:\s*([A-Z0-9.]+)", content, re.IGNORECASE)

    title = title_match.group(1).strip() if title_match else fallback_name.replace("_", " ").replace(".txt", "")
    document_number = number_match.group(1).strip() if number_match else "AUTO-" + re.sub(r"[^A-Z0-9]", "", fallback_name.upper())[:12]
    revision = revision_match.group(1).strip() if revision_match else "A"

    discipline, discipline_conf = _score_keywords(content, DISCIPLINE_KEYWORDS)
    document_type, type_conf = _score_keywords(content, TYPE_KEYWORDS)
    risk_score = calculate_risk_score(content)
    confidence = round((discipline_conf + type_conf) / 2, 2)

    return AIResult(title, document_number, revision, discipline, document_type, confidence, risk_score)


def calculate_risk_score(content: str) -> float:
    normalized = content.lower()
    hits = sum(normalized.count(term) for term in RISK_TERMS)
    length_factor = min(1.0, len(content) / 3000)
    score = min(1.0, hits * 0.12 + length_factor * 0.15)
    return round(score, 2)


def classify_text(content: str) -> dict:
    result = extract_metadata(content)
    return {
        "discipline": result.discipline,
        "document_type": result.document_type,
        "confidence": result.confidence,
        "risk_score": result.risk_score,
    }
