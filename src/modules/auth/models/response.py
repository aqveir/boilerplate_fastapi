from pydantic import BaseModel
from fastapi import status

class AuthResponse(BaseModel):
    message: str = "Success"
    success: bool = False
    error: bool = False
    data: dict = {}

class AuthSuccessResponse(BaseModel):
    message: str = "Success"
    success: bool = True
    error: bool = False
    status_code: int = status.HTTP_200_OK
    data: dict = {}
    