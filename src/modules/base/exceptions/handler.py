from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse

from .base import GenericBaseException


def custom_exception_handler() -> Callable[[Request, GenericBaseException], JSONResponse]:
    detail = {
        "status_code":500,
        "error_msg_code": "error_code_generic",
        "error_code": "error_code_generic",
        "message": "error_message",
        "context": "exception"
    }  # Using a dictionary to hold the detail

    async def exception_handler(_: Request, exception: GenericBaseException) -> JSONResponse:
        if exception.status_code:
            detail["status_code"] = exception.status_code
        if exception.error_code:
            detail["error_code"] = exception.error_code
        if exception.error_msg_code:
            detail["error_msg_code"] = exception.error_msg_code
        if exception.message:
            detail["message"] = exception.message
        if exception.__class__:
            detail["context"] = exception.__class__.__name__

        # Log the exception if needed
        #logger.error(exc)
        
        return JSONResponse(
            detail, 
            status_code=detail["status_code"]
        )

    return exception_handler