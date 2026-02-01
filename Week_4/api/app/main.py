import time
import os

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv

from api.app.responses import success_response, error_response
from api.app.validation import QueryRequest
from api.app.auth import verify_api_key
from api.app.rate_limit import rate_limiter
from api.app.logging_config import setup_logger, log_request

# Load environment variables from Week_4/.env
load_dotenv()

app = FastAPI(title="Week 4 Secured API")

logger = setup_logger()


@app.post("/query")
def query_endpoint(
    request: QueryRequest,
    auth_ok: bool = Depends(verify_api_key),
    rate_ok: bool = Depends(rate_limiter)
):
    start_time = time.time()

    try:
        # ---- Core logic (placeholder) ----
        # This is where RAG / OpenAI logic would go later
        result = {
            "answer": f"Received query: {request.query}"
        }
        retrieval_count = 0

        log_request(
            logger=logger,
            endpoint="/query",
            start_time=start_time,
            status="success",
            retrieval_count=retrieval_count
        )

        return success_response(result)

    except HTTPException as e:
        log_request(
            logger=logger,
            endpoint="/query",
            start_time=start_time,
            status="error"
        )
        return error_response(
            code="HTTP_ERROR",
            message=str(e.detail),
            status_code=e.status_code
        )

    except Exception:
        log_request(
            logger=logger,
            endpoint="/query",
            start_time=start_time,
            status="error"
        )
        return error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            status_code=500
        )