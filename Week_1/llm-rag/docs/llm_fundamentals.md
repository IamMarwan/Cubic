# LLM Fundamentals – Week 1 Summary

## 1. Tokens and tokenization

Large Language Models (LLMs) do not work directly with words and sentences like humans do. Inside the model, text is converted into smaller pieces called tokens. A token can be a whole word, part of a word, punctuation, or even spaces. For English, a rough rule of thumb is that 1 token is about 4 characters or roughly three quarters of a word.

Before I send any text to an LLM, it is passed through a tokenizer. The tokenizer splits the text into tokens using rules designed during model training. OpenAI’s models use a tokenizer implementation called `tiktoken`, which is based on a method called Byte Pair Encoding (BPE). BPE breaks text into common sub-word units so that the model can handle many languages and unexpected words efficiently.

Tokens matter for two reasons:

1. **Limits** – every model has a maximum number of tokens it can handle in one request (the context window).
2. **Cost** – when using the API, I am billed based on how many tokens I send and how many tokens the model generates.

Because of this, it is useful to count tokens in my own code (for example, with `tiktoken` in Python) before sending requests.

---

## 2. Context windows

The **context window** is the maximum number of tokens the model can see at once. This includes:

- The current user prompt,
- Any previous messages or conversation history that I include,
- Any extra documents or text I add for the model to read,
- The tokens produced by the model as a response.

If the total number of tokens is larger than the context window, the request will fail or some part of the text must be removed or summarized. Modern models like GPT‑4.1 mini can handle very large context windows (up to around one million tokens), which is enough for long conversations or multiple documents, but it is still a fixed limit.

Context windows are important in practice because they control:

- How much chat history I can keep,
- How many and how large documents I can pass into the model at once,
- Whether I need to summarise long documents before sending them.

---

## 3. Embeddings

Embeddings are a way to represent text as vectors (lists of numbers) in a high‑dimensional space. The key idea is that texts with similar meaning should have embeddings that are close together, while texts that are unrelated should be far apart. The model learns this structure during training.

Embeddings are especially useful for:

- **Semantic search**: finding documents that are relevant to a question, even if they do not share the same exact words.
- **Clustering**: grouping similar texts together.
- **Recommendations**: suggesting items similar to things the user has seen before.
- **Classification and anomaly detection**: using the distances between vectors to detect unusual or out‑of‑distribution examples.

A typical pattern for using embeddings with LLMs is:

1. Split documents into smaller chunks.
2. Compute an embedding vector for each chunk and store the vectors in a database that supports vector similarity search.
3. When a user asks a question, compute an embedding for the question.
4. Find the document chunks whose embeddings are closest to the question embedding.
5. Pass those chunks, along with the question, into the LLM to generate an answer.

This pattern is the foundation of **Retrieval‑Augmented Generation (RAG)**.

---

## 4. Fine‑tuning vs Retrieval‑Augmented Generation (RAG)

Fine‑tuning and RAG are two different ways to adapt a general‑purpose LLM to a specific use case.

### 4.1. Fine‑tuning

Fine‑tuning means taking a base model and continuing its training on my own dataset. I provide many examples of inputs together with desired outputs. During fine‑tuning, the model’s internal weights are updated so that it learns to imitate these examples more closely.

Fine‑tuning is particularly useful when:

- I want the model to follow a specific tone and style,
- I need the model to consistently output a particular format or template,
- I have a narrow, repetitive task with many labelled examples.

Fine‑tuning is not the best option for storing large and frequently changing knowledge, because every time the knowledge changes, I would need to retrain the model.

### 4.2. Retrieval‑Augmented Generation (RAG)

In a RAG system, the base model is kept frozen. Instead of trying to store all knowledge inside the model, I keep my documents in an external store and retrieve the most relevant pieces at query time.

The typical RAG workflow is:

1. Ingest documents (for example, PDFs, manuals, procedures) and split them into chunks.
2. Compute embeddings for each chunk and store them in a vector database.
3. For each user question, compute an embedding of the question.
4. Retrieve the document chunks that are most similar to the question embedding.
5. Build a prompt that includes the user question and the retrieved chunks.
6. Ask the LLM to answer the question using this context.

RAG is ideal when I need to answer questions based on specific, possibly changing documents, such as engineering standards, project specifications, or internal company procedures.

### 4.3. Choosing between them

A simple way to decide is:

- If the main challenge is **knowledge** (lots of documents, need up‑to‑date facts) → use **RAG**.
- If the main challenge is **behaviour or style** (how the model writes, formats, or structures its answers) → consider **fine‑tuning**.

In real projects, it is common to start with RAG for knowledge and then optionally add fine‑tuning later to refine the model’s tone and reliability.

---

## 5. Why this is important for my training

In my training at Cubic Engineering Consultancy, these concepts form the foundation for any LLM‑based tools I build. Engineering projects involve large amounts of text: drawings, specifications, codes, emails, and reports. By understanding tokens, context windows, embeddings, fine‑tuning, and RAG, I can design systems that search, summarise and present this information in a way that is accurate, efficient, and aligned with how the company works.
