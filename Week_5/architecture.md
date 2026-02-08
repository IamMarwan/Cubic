# System Architecture

The system follows a simple Retrieval-Augmented Generation (RAG) architecture.

## Flow

User  
→ FastAPI Service  
→ Retrieval Component  
→ LLM Generation  
→ Answer with Sources  

## Observability

- Metrics collected at API level
- Latency, errors, and token usage tracked per request
- Metrics exposed through a dedicated endpoint