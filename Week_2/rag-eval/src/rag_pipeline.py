from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any

import math
import os

from dotenv import load_dotenv
from openai import OpenAI

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
LOGS_DIR = BASE_DIR / "logs"

# Load API key from .env in rag-eval root
load_dotenv()

client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4.1-mini"


@dataclass
class RetrievedChunk:
    doc_id: str
    text: str
    score: float


def _ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_event(message: str) -> None:
    """Append a simple log line to logs/rag_log.txt."""
    _ensure_logs_dir()
    logfile = LOGS_DIR / "rag_log.txt"
    with logfile.open("a", encoding="utf-8") as f:
        f.write(message.rstrip() + "\n")


def read_knowledge_documents() -> Dict[str, str]:
    """
    Load all markdown files from the knowledge directory.

    Returns
    -------
    dict
        Mapping of doc_id -> text content.
    """
    docs: Dict[str, str] = {}
    for path in KNOWLEDGE_DIR.glob("*.md"):
        doc_id = path.stem  # e.g. "cec_overview"
        text = path.read_text(encoding="utf-8")
        docs[doc_id] = text
    return docs


def compute_embedding(text: str) -> List[float]:
    """Compute an embedding vector for the given text."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def retrieve_relevant_chunks(
    question: str,
    docs: Dict[str, str],
    top_k: int = 3,
) -> List[RetrievedChunk]:
    """
    Retrieve the top_k most relevant documents for the question.
    Each document is treated as a single chunk in this simple prototype.
    """
    q_emb = compute_embedding(question)
    results: List[RetrievedChunk] = []

    for doc_id, text in docs.items():
        doc_emb = compute_embedding(text)
        score = cosine_similarity(q_emb, doc_emb)
        results.append(RetrievedChunk(doc_id=doc_id, text=text, score=score))

    results.sort(key=lambda c: c.score, reverse=True)
    return results[:top_k]


def answer_question(
    question: str,
    min_relevance: float = 0.25,
    max_output_tokens: int = 350,
) -> Dict[str, Any]:
    """
    Main RAG entry point with basic guardrails.

    Returns a dict like:
    {
        "ok": bool,
        "reason": str,
        "answer": str,
        "sources": List[str],
        "retrieved": List[dict],
        "usage": {...}  # when ok=True
    }
    """
    cleaned = (question or "").strip()

    # Guardrail 1: empty query
    if not cleaned:
        msg = "Query is empty. Please provide a question related to the knowledge base."
        log_event("EMPTY_QUERY")
        return {
            "ok": False,
            "reason": "empty_query",
            "answer": msg,
            "sources": [],
            "retrieved": [],
        }

    # Guardrail 2: overly long query
    if len(cleaned) > 500:
        msg = "Query is too long. Please shorten it to a single clear question."
        log_event("LONG_QUERY")
        return {
            "ok": False,
            "reason": "query_too_long",
            "answer": msg,
            "sources": [],
            "retrieved": [],
        }

    docs = read_knowledge_documents()

    if not docs:
        msg = "Knowledge base is empty. Please add documents before querying."
        log_event("EMPTY_KB")
        return {
            "ok": False,
            "reason": "empty_knowledge_base",
            "answer": msg,
            "sources": [],
            "retrieved": [],
        }

    retrieved = retrieve_relevant_chunks(cleaned, docs)
    retrieved_dicts = [c.__dict__ for c in retrieved]
    best_score = retrieved[0].score if retrieved else 0.0

    # Filter chunks by minimum relevance
    relevant_chunks = [c for c in retrieved if c.score >= min_relevance]

    # Guardrail 3: no relevant context
    if not relevant_chunks:
        msg = (
            "I’m not able to answer this question based on the available documents. "
            "Please consult a human engineer or update the knowledge base."
        )
        log_event(f"NO_MATCH\t{cleaned}")
        return {
            "ok": False,
            "reason": "no_relevant_context",
            "answer": msg,
            "sources": [],
            "retrieved": retrieved_dicts,
        }

    # Build context from relevant chunks
    context_parts: List[str] = []
    source_ids: List[str] = []
    for chunk in relevant_chunks:
        context_parts.append(f"[{chunk.doc_id}]\n{chunk.text}")
        source_ids.append(chunk.doc_id)

    context = "\n\n".join(context_parts)

    # Prompt that strongly limits the model to the context
    prompt = (
        "You are an assistant for Cubic Engineering Consultancy. "
        "You must answer ONLY using the information in the context below. "
        "If the context does not contain the answer, you MUST say you do not know "
        "and suggest checking with a human engineer. Do not guess or invent any details.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {cleaned}\n\n"
        "Answer in a short, clear paragraph. "
        "At the end, add a line starting with 'Sources:' followed by the IDs of the documents you used, "
        "for example: Sources: [cec_overview], [rag_overview]."
    )

    response = client.responses.create(
        model=GENERATION_MODEL,
        input=prompt,
        max_output_tokens=max_output_tokens,
    )

    answer_text = response.output_text

    # Guardrail 4: enforce Sources line if the model forgot it
    if "Sources:" not in answer_text:
        sources_str = ", ".join(f"[{sid}]" for sid in source_ids)
        answer_text = answer_text.rstrip() + f"\n\nSources: {sources_str}"

    log_event(
        f"ANSWER\t{cleaned}\tbest_score={best_score:.3f}\tsources={','.join(source_ids)}"
    )

    return {
        "ok": True,
        "reason": "answered",
        "answer": answer_text,
        "sources": source_ids,
        "retrieved": retrieved_dicts,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }