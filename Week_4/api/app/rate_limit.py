import time
from fastapi import Header
from fastapi.exceptions import HTTPException

# Simple in-memory store: {api_key: [timestamps]}
REQUEST_LOG = {}

# Rate limit settings
MAX_REQUESTS = 60       # requests
WINDOW_SECONDS = 60     # per minute


def rate_limiter(x_api_key: str = Header(default=None)):
    """
    Basic rate limiter per API key.
    """
    if x_api_key is None:
        # Auth layer should catch this first, but keep it safe
        raise HTTPException(
            status_code=401,
            detail="Missing API key"
        )

    current_time = time.time()
    window_start = current_time - WINDOW_SECONDS

    # Initialize if key not seen before
    if x_api_key not in REQUEST_LOG:
        REQUEST_LOG[x_api_key] = []

    # Remove old requests outside the window
    REQUEST_LOG[x_api_key] = [
        t for t in REQUEST_LOG[x_api_key] if t > window_start
    ]

    # Check limit
    if len(REQUEST_LOG[x_api_key]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    # Record this request
    REQUEST_LOG[x_api_key].append(current_time)

    return True