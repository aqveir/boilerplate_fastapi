import typing
import json
from typing import Generic, Optional
from fastapi import status, Response
from pydantic import SerializeAsAny, BaseModel
from starlette.background import BackgroundTask

# Include the project models
from .base import GenericResponse as GenericResponseModel, T
from ..exceptions.base import GenericBaseException


""" Generic Success Response Model

This is the pydantic model for the success response.

It contains the following fields:
- status_code: The HTTP status code of the response.
- message: The success message of the response.
- success: A boolean indicating whether the request was successful or not.
- data: The data of the response.
- errors: The errors of the response.
- metadata: The metadata of the response.
"""
class SuccessModel(GenericResponseModel, Generic[T]):
    """
    Base model for all success response models.
    """
    status_code: int = status.HTTP_200_OK
    message: str = "success"
    success: bool = True


""" Generic Error Response Model

This model is used to represent the error response for all the endpoints.
It contains the following fields:
- status_code: The HTTP status code of the response.
- error_code: The error code of the response.
- error_msg_code: The error message code of the response.
- message: The error message of the response.
- context: The context of the error.
- success: A boolean indicating whether the request was successful or not.
"""
class ErrorModel(GenericResponseModel, Generic[T]):
    """
    Base model for all error response models.
    """
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "error"
    success: bool = False


class BaseResponse(Response):
    """
    Base class for all response models.
    """
    media_type: str = "application/json"


class JsonErrorResponse(BaseResponse):
    media_type: str = "application/json"

    def __init__(
        self,
        content: typing.Any,
        message: str = "error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        # check content is a class of pydantic model
        if isinstance(content, GenericBaseException):
            exception: GenericBaseException = content

            # Create an instance of the error model
            error_model = ErrorModel()
            error_model.errors = {}

            if exception.status_code:
                error_model.status_code = exception.status_code
                status_code = exception.status_code
            if exception.error_code:
                error_model.errors['code'] = exception.error_code
            if exception.error_msg_code:
                error_model.errors['msg_code'] = exception.error_msg_code
            if exception.message:
                error_model.message = exception.message
            if exception.__class__:
                error_model.errors['context'] = exception.__class__.__name__

            content = error_model.model_dump(mode="json")

        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


""" JSON Success Response

This response class is used to represent the JSON success response for 
all the endpoints.
"""
class JsonSuccessResponse(BaseResponse):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any,
        message: str = "success",
        status_code: int = status.HTTP_200_OK,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        # check content is a class of pydantic model
        if isinstance(content, BaseModel):
            model = SuccessModel[BaseModel](
                status_code=status_code,
                message=message,
                data=content
            )
            content = model.model_dump(mode="json")

        # check content is a boolean
        if isinstance(content, bool):
            model = SuccessModel[bool](
                status_code=status_code,
                message=message,
                data=content
            )
            content = model.model_dump(mode="json")


        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
    