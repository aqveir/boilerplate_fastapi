from typing import Callable, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .base import GenericBaseException


"""Generic Error Response Model

This model is used to represent the error response for all the endpoints.
It contains the following fields:
- status_code: The HTTP status code of the response.
- error_code: The error code of the response.
- error_msg_code: The error message code of the response.
- message: The error message of the response.
- context: The context of the error.
- success: A boolean indicating whether the request was successful or not.
"""
class ErrorResponseModel(BaseModel):
    """
    Base model for all error response models.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "error_code_generic"
    error_msg_code: str = "error_code_generic"
    message: str = "error_message"
    context: str = "exception"
    success: bool = False

    errors: Optional[dict] = None
    data: Optional[dict] = None
    metadata: Optional[dict] = None


def custom_exception_handler() -> Callable[[Request, GenericBaseException], JSONResponse]:
    async def exception_handler(_: Request, exception: GenericBaseException) -> JSONResponse:
        # Create an instance of the error model
        error_model = ErrorResponseModel()

        if exception.status_code:
            error_model.status_code = exception.status_code
        if exception.error_code:
            error_model.error_code = exception.error_code
        if exception.error_msg_code:
            error_model.error_msg_code = exception.error_msg_code
        if exception.message:
            error_model.message = exception.message
        if exception.__class__:
            error_model.context = exception.__class__.__name__

        # Log the exception if needed
        #logger.error(exc)
        
        return JSONResponse(
            error_model.model_dump(mode="json", exclude_none=True, exclude_defaults=False),
            status_code=error_model.status_code
        )

    return exception_handler