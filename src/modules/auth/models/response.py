from typing import Generic, TypeVar
from pydantic import BaseModel
from fastapi import status

from modules.base.models.base import GenericSuccessResponse

class AuthResponse(BaseModel):
    message: str = "Success"
    success: bool = False
    error: bool = False
    data: dict = {}

class AuthSuccessResponse(GenericSuccessResponse[BaseModel]):
    pass
    