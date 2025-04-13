import json
from typing import List
from fastapi import Request

# Include the project controllers
from modules.base.controller.base import BaseController

# Include the project services
from ..services.service import AuthService

# Include the project models
from ..models.base import Auth
from ..models.request import LoginRequest
from ..models.response import AuthSuccessResponse


class AuthController(BaseController[Auth]):
    def __init__(self):
        super().__init__(model=Auth)
        self.service = AuthService()


    async def authenticate(self, credentials: LoginRequest, request: Request):
        ip_address = request.client.host

        data: dict[str, any] = await self.service.authenticate(credentials, ip_address)

        # Get data from the service
        return AuthSuccessResponse(
            message="Login successful",
            data=data
        )


    async def logout(self, access_token: str, is_forced: bool = False) -> bool:
        data: dict[str, any] = await self.service.logout(
            token=access_token,
            is_forced=is_forced
        )

        # Get data from the service
        return AuthSuccessResponse(
            message="Logout successful"
        )
    