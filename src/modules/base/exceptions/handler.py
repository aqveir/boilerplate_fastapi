import logging
from typing import Callable
from fastapi import Request

# Include the Error Response model
from ..models.response import JsonErrorResponse

# Import the project models
from .base import GenericBaseException

# Set Error logger
logger = logging.getLogger("error")

def custom_exception_handler() -> Callable[
    [Request, GenericBaseException], JsonErrorResponse]:
    """ Custom exception handler for the application.
    This function is used to handle exceptions raised in the application.
    It takes a request and an exception as input and returns a JSON response
    with the error details.
    """
    async def exception_handler(_: Request, exception: GenericBaseException) -> JsonErrorResponse:

        # Log the exception if needed
        logger.error(exception)

        return JsonErrorResponse(
            content=exception
        )

    return exception_handler
