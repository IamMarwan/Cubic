import hashlib
import os

def compute_checksum(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_documents(folder: str) -> dict:
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs