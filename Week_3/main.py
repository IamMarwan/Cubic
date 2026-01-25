# Week 3 – Incremental Indexing System
# GitHub Repository: https://github.com/IamMarwan/Cubic

from utils import load_documents
from indexer import init_db, incremental_index

if __name__ == "__main__":
    init_db()
    docs = load_documents("corpus")
    incremental_index(docs, version="v1")
