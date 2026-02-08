# End-to-End Demo Steps

1. Build the Docker image for the RAG system.
2. Run the container locally.
3. Send a query request to the API.
4. Verify the generated answer and returned sources.
5. Check the `/metrics` endpoint for latency, errors, and token usage.

This demo shows the full pipeline:
ingestion → retrieval → generation → observability.