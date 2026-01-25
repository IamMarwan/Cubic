import json
import os
import sqlite3
import numpy as np
from datetime import datetime
from utils import compute_checksum

DB_NAME = "metadata.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            checksum TEXT,
            is_deleted INTEGER,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def fake_embedding(text: str):
    np.random.seed(abs(hash(text)) % (10**8))
    return np.random.rand(5).tolist()

def load_index(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_index(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def incremental_index(documents: dict, version: str):
    index_path = f"index/index_{version}.json"
    index_data = load_index(index_path)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT doc_id, checksum FROM documents WHERE is_deleted = 0")
    existing = {row[0]: row[1] for row in c.fetchall()}

    # ADD / UPDATE
    for doc_id, content in documents.items():
        checksum = compute_checksum(content)

        if doc_id not in existing:
            print(f"[NEW] {doc_id}")
        elif existing[doc_id] != checksum:
            print(f"[UPDATED] {doc_id}")
        else:
            continue

        index_data[doc_id] = {
            "embedding": fake_embedding(content),
            "content": content,
            "updated_at": datetime.utcnow().isoformat()
        }

        c.execute("""
            INSERT OR REPLACE INTO documents
            VALUES (?, ?, 0, ?)
        """, (doc_id, checksum, datetime.utcnow().isoformat()))

    # DELETE
    current_ids = set(documents.keys())
    deleted = set(existing.keys()) - current_ids

    for doc_id in deleted:
        print(f"[DELETED] {doc_id}")
        index_data.pop(doc_id, None)
        c.execute("UPDATE documents SET is_deleted = 1 WHERE doc_id = ?", (doc_id,))

    conn.commit()
    conn.close()
    save_index(index_path, index_data)