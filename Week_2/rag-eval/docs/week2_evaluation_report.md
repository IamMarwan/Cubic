# Week 2 – RAG Evaluation Report

## 1. Evaluation setup

- Knowledge base: 3 markdown documents (`cec_overview`, `rag_overview`, `llm_policies`)
- Number of evaluation questions: 30
- Embedding model: `text-embedding-3-small`
- Generation model: `gpt-4.1-mini`
- Retrieval method: cosine similarity, top 3 documents
- Minimum relevance threshold: 0.25

## 2. Results (to be filled after running evaluation)

- Total questions: 30
- Correctly grounded answers (expected source included): 17 / 30
- Questions where the system safely refused to answer: 3 / 30
- Questions with retrieval errors or hallucinations: 10 / 30

## 3. Typical failure cases

- **Wrong retrieval / source attribution**:  
  For question Q04 ("How many main steps does the internal RAG pipeline use"),  
  the system produced a correct answer but cited the wrong source.  
  The expected source was `rag_overview`, but similar retrieval issues appeared  
  in other questions where content from `llm_policies` was instead answered  
  using `rag_overview`. This indicates that while the model answers correctly,  
  retrieval ranking and source attribution still need improvement.

- **Wrong retrieval between closely related documents**:  
  For questions Q12 and Q13 (both related to safety and refusal behaviour),  
  the system answered correctly but cited `rag_overview` instead of the expected  
  `llm_policies`. This shows that semantically similar documents can confuse  
  the retriever, leading to incorrect grounding even when hallucinations  
  are avoided.

## 4. Improvements implemented

- Tightened the generation prompt to explicitly forbid using information outside the retrieved context.
- Added a similarity threshold and fallback behaviour:
  - If no document passes the threshold, the system returns a safe refusal message instead of guessing.
- Added input validation:
  - Empty queries return a friendly error message.
  - Very long queries are rejected with a request to shorten the question.
- Ensured that every answer includes a `Sources:` line listing the document IDs used.

## 5. Next steps

- Extend the knowledge base with more project-specific documents.
- Increase the number of evaluation questions with real queries from engineers.
- Add more fine-grained logging and metrics (for example, tracking latency and token usage per query).