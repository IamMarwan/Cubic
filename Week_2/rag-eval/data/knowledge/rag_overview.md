# Internal RAG System – Overview

The internal Retrieval-Augmented Generation (RAG) system at Cubic Engineering Consultancy is designed to help engineers quickly access information from a curated knowledge base. The system works in three main steps:

1. Documents are stored as text files and converted into vector embeddings using an OpenAI embedding model.
2. For each user question, the system computes an embedding and retrieves the most similar documents based on cosine similarity.
3. The retrieved documents are passed to a language model which generates an answer strictly using the provided context.

The default configuration retrieves the top 3 most relevant documents. If none of the documents reach a minimum similarity threshold, the system should not answer the question and must instead return a safe fallback message.

The current RAG prototype uses the `text-embedding-3-small` model for embeddings and `gpt-4.1-mini` for answer generation. It is intended as an internal assistant and not as a final decision-making tool.