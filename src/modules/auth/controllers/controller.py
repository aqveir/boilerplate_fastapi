""" Import the required modules """
from fastapi import Request
from pydantic import BaseModel

# Include the project modules
from modules.base.models.response import JsonSuccessResponse
from modules.base.controller.base import BaseController

# Include the project services
from ..services.service import AuthService

# Include the project models
from ..models.request import (
    LoginRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    ChangePasswordRequest,
    ResetPasswordRequest
)


class AuthController(BaseController):
    """
    AuthController class to handle authentication related requests.
    """

    def __init__(self):
        super().__init__()
        self.service = AuthService()


    async def authenticate(
            self,
            credentials: LoginRequest,
            request: Request) -> JsonSuccessResponse:
        """
        Authenticate a user with the given credentials.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.authenticate(
                credentials, ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Authentication successful"
            )
        except Exception as e:
            raise e


    async def logout(
            self,
            access_token: str,
            is_forced: bool = False) -> JsonSuccessResponse:
        """
        Logout a user with the given access token.
        """
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


    async def register(
            self,
            payload: RegisterRequest,
            request: Request) -> JsonSuccessResponse:
        """
        Register a new user with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.register(
                payload=payload,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Registration successful"
            )
        except Exception as e:
            raise e


    async def forgot_password(
            self,
            payload: ForgotPasswordRequest,
            request: Request) -> JsonSuccessResponse:
        """
        Send a forgot password request with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.forgot_password(
                payload=payload,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                message="Forgot password successful",
                content=response
            )
        except Exception as e:
            raise e


    async def change_password(
            self,
            payload: ChangePasswordRequest,
            request: Request) -> JsonSuccessResponse:
        """
        Change the password with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.change_password(
                payload=payload,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                message="Change password successful",
                content=response
            )
        except Exception as e:
            raise e


    async def reset_password(
            self,
            payload: ResetPasswordRequest,
            request: Request) -> JsonSuccessResponse:
        """
        Reset the password with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.reset_password(
                payload=payload,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                message="Reset password successful",
                content=response
            )
        except Exception as e:
            raise e


    async def refresh_token(
            self,
            access_token: str,
            request: Request) -> JsonSuccessResponse:
        """
        Refresh the access token using the refresh token.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.refresh_token(
                token=access_token,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                message="Refresh token successful",
                content=response
            )
        except Exception as e:
            raise e
