from fastapi import FastAPI
from rag_pipeline import run_rag
from metrics import metrics
from logger import logger
import time

app = FastAPI(title="Cubic RAG System")

@app.post("/query")
def query_rag(query: str):
    start_time = time.time()

    try:
        answer, sources, latency, tokens_in, tokens_out = run_rag(query)

        metrics.log_request(
            latency=latency,
            tokens_in=tokens_in,
            tokens_out=tokens_out
        )

        logger.info(f"Query processed in {latency:.4f}s")

        return {
            "query": query,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        metrics.log_request(latency=0, error=True)
        logger.error(str(e))
        return {"error": "Internal server error"}

@app.get("/metrics")
def get_metrics():
    return metrics.report()