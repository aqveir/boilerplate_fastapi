""" Import the required modules """
from fastapi import Request
from pydantic import BaseModel

# Include the project modules
from modules.base.models.response import JsonSuccessResponse
from modules.base.controller.base import BaseController

# Include the project services
from ..services.organization_service import OrganizationService as LookupService

# Include the project models
# from ..models.base import Auth
# from ..models.request import (
#     LoginRequest,
#     RegisterRequest,
#     ForgotPasswordRequest,
#     ChangePasswordRequest,
#     ResetPasswordRequest
# )


class LookupController(BaseController):
    """
    LookupController class to handle lookup related requests.
    This class inherits from the BaseController class and uses the 
    LookupService
    """

    def __init__(self):
        super().__init__()
        self.service = LookupService()


    async def index(
            self,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get all the lookup.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.index(ip_address)

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def show(
            self,
            uid: str,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get the lookup with the given uid.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.show(
                uid=uid,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def create(
            self,
            payload: BaseModel,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Create a new lookup with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.create(
                payload, ip_address, current_user
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def update(
            self,
            uid: str,
            payload: BaseModel,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Update the lookup with the given uid and payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.update(
                uid=uid,
                payload=payload,
                ip_address=ip_address,
                current_user=current_user
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def delete(
            self,
            uid: str,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Delete the lookup data with the given uid.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.delete(
                uid=uid,
                ip_address=ip_address
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e
