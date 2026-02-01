import os
from fastapi import Header
from fastapi.exceptions import HTTPException


def verify_api_key(x_api_key: str = Header(default=None)):
    """
    Verifies the internal API key sent by the client.
    Expected header: X-API-Key
    """
    internal_key = os.getenv("INTERNAL_API_KEY")

    if not internal_key:
        raise HTTPException(
            status_code=500,
            detail="Internal API key not configured"
        )

    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Missing API key"
        )

    if x_api_key != internal_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    return True