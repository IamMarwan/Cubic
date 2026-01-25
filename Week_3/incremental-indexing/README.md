# Week 3 – Incremental Indexing System

GitHub Repository:
https://github.com/IamMarwan/Cubic

## Overview
This project implements an incremental document indexing system using Python.
It is designed to avoid full re-indexing by detecting document-level changes.

## Features
- Incremental indexing (no full rebuild)
- Document add / update / remove detection
- MD5 checksum-based change tracking
- Index versioning (v1, v2)
- Metadata tracking using SQLite
- No external services or databases

## How It Works
1. Documents are stored in the `corpus/` folder
2. Each document is assigned a document ID (filename)
3. A checksum is computed for each document
4. Only changed documents are re-indexed
5. Deleted documents are removed from the index
6. Index versions are stored as JSON files

## Demo Steps
1. Add a `.txt` file → system detects `[NEW]`
2. Modify a file → system detects `[UPDATED]`
3. Delete a file → system detects `[DELETED]`
4. Change index version → new index file is created

## Folder Structure
Week_3/
├── corpus/
├── index/
├── main.py
├── indexer.py
├── utils.py
├── metadata.db
└── README.md


## Notes
This implementation focuses on correctness, clarity, and scalability
and prepares the system for future vector database integration.