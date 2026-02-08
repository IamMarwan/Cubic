# Monitoring and Metrics

The system tracks basic observability metrics at the API level.

## Collected Metrics

- Total request count
- Error count
- Average request latency
- Prompt tokens (tokens in)
- Generated tokens (tokens out)

## Accessing Metrics

Metrics are available through the `/metrics` endpoint of the FastAPI service.
These metrics help identify performance bottlenecks and estimate LLM usage cost.