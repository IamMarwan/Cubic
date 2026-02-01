import logging
import uuid
import time


def setup_logger() -> logging.Logger:
    """
    Configure and return a structured logger.
    """
    logger = logging.getLogger("week4_api")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_request(
    logger: logging.Logger,
    endpoint: str,
    start_time: float,
    status: str,
    retrieval_count: int = 0
):
    """
    Log request metadata without sensitive data.
    """
    duration_ms = int((time.time() - start_time) * 1000)

    log_data = {
        "request_id": str(uuid.uuid4()),
        "endpoint": endpoint,
        "status": status,
        "duration_ms": duration_ms,
        "retrieval_count": retrieval_count
    }

    logger.info(log_data)