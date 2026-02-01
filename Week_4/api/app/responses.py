from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(data: Any, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "data": data,
            "error": None
        }
    )


def error_response(
    code: str,
    message: str,
    status_code: int = 400
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "data": None,
            "error": {
                "code": code,
                "message": message
            }
        }
    )