import json
from typing import List
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Include the project controllers
from modules.base.controller.base import BaseController

# Include the project services
from ..services.service import AuthService

# Include the project models
from ..models.base import Auth
from ..models.request import *
from modules.base.models.response import JsonSuccessResponse


class AuthController(BaseController[Auth]):
    def __init__(self):
        super().__init__(model=Auth)
        self.service = AuthService()


    async def authenticate(self, credentials: LoginRequest, request: Request) -> JsonSuccessResponse:
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.authenticate(credentials, ip_address)

            # Send data from the service
            return JsonSuccessResponse(
                content=response, 
                message="Authentication successful"
            )
        except Exception as e:
            raise e


    async def logout(self, access_token: str, is_forced: bool = False) -> JsonSuccessResponse:
        try:
            response: BaseModel = await self.service.logout(
                token=access_token,
                is_forced=is_forced
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response, 
                message="Logout successful"
            )
        except Exception as e:
            raise e
    

    async def register(self, payload: RegisterRequest, request: Request) -> JsonSuccessResponse:
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.register(
                payload=payload,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(content=response, message="Registration successful")
        except Exception as e:
            raise e

 
    async def forgot_password(self, payload: ForgotPasswordRequest, request: Request) -> JsonSuccessResponse:
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            # Send data from the service
            return JsonSuccessResponse(
                message="Forgot password successful",
                content=payload
            )
        except Exception as e:
            raise e


    async def change_password(self, payload: ChangePasswordRequest, request: Request) -> JsonSuccessResponse:
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            # Send data from the service
            return JsonSuccessResponse(
                message="Change password successful",
                content=payload
            )
        except Exception as e:
            raise e






    async def reset_password(self, token: str, password: str) -> JsonSuccessResponse:
        data: dict[str, any] = await self.service.reset_password(
            token=token,
            password=password
        )

        # Get data from the service
        return JsonSuccessResponse(
            message="Reset password successful",
            data=data
        )


    async def refresh_token(self, refresh_token: str) -> JsonSuccessResponse:
        data: dict[str, any] = await self.service.refresh_token(
            token=refresh_token
        )

        # Send data from the service
        return JsonSuccessResponse(
            message="Refresh token successful",
            content=data
        )
   