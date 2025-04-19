from typing import Callable
from fastapi import Request

# Include the Error Response model
from ..models.response import JsonErrorResponse

# Import the project models
from .base import GenericBaseException


def custom_exception_handler() -> Callable[[Request, GenericBaseException], JsonErrorResponse]:
    async def exception_handler(_: Request, exception: GenericBaseException) -> JsonErrorResponse:

        # Log the exception if needed
        #logger.error(exc)
        
        return JsonErrorResponse(
            content=exception
        )

    return exception_handler