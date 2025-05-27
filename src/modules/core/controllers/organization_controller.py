""" Import the required modules """
from fastapi import Request
from pydantic import BaseModel

# Include the project modules
from modules.base.models.response import JsonSuccessResponse
from modules.base.controller.base import BaseController

# Include the project services
from ..services.organization_service import OrganizationService


class OrganizationController(BaseController):
    """
    OrganizationController class to handle organization related requests.
    This class inherits from the BaseController class and uses the 
    OrganizationService
    """

    def __init__(self):
        super().__init__()
        self.service = OrganizationService()


    async def index(
            self,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get all the organizations.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.list(
                request=request,
                ip_address=ip_address
            )

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
        Get the organization with the given uid.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.get(
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
        Create a new organization with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.create(
                payload, ip_address, current_user
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Authentication successful"
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
        Update the organization with the given hash and payload.
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
                content=response, 
                message="Logout successful"
            )
        except Exception as e:
            raise e


    async def delete(
            self,
            uid: str,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Delete the organization with the given hash and payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.delete(
                uid=uid,
                ip_address=ip_address,
                current_user=current_user
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e
