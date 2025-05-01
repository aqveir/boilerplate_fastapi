""" Import the required modules """
import json
from typing import List
from pydantic import TypeAdapter, BaseModel

# Include the project models
from modules.core.models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)
from modules.user.models.user import User
from modules.core.models.organization.organization import Organization

# include the project services
from modules.base.services.base import BaseService
from modules.base.services.auth.claim_service import ClaimService

# Include the module repositories
from modules.core.repositories.organization_repository import OrganizationRepository

# Include the module events
from ..events.organization_event import (
    OrganizationCreateEvent,
)

# Include the module exceptions
from modules.base.exceptions.base import *

class OrganizationService:
    """ OrganizationService class to handle organization related operations. """
    def __init__(self):
        self.repository = OrganizationRepository
        self.claim_service = ClaimService()


    async def create(
            self, payload: BaseModel, ip_address: str,
            current_user: BaseModel) -> Organization:
        """ Create a new object """
        try :
            # Validate the credentials
            model: BaseModel = await self.repository.save(
                payload, ip_address
            )
            if not model:
                raise AuthenticationException()
            else:
                # Set update the user status

                # Raise event on successful creation
                OrganizationCreateEvent().raise_event(model)

            return model
        except Exception as e:
            raise e


    async def update(
            self, uid: str, payload: BaseModel,
            ip_address: str, current_user: BaseModel) -> Organization:
        """ Update the model """
        try:
            # Get the claim from storage
            model: BaseModel = await self.repository.update_by_hash(
                uid, payload, ip_address
            )

            # Raise event on successful update

            return model
        except Exception as e:
            raise e


    async def delete(
            self, uid: str, ip_address: str,
            current_user: BaseModel) -> Organization:
        """ Delete the model """
        try:
            # Validate the payload
            # user: User = await self.repository.register_user(payload)

            # Create and store the claim
            # claim: AuthClaim = self.claim_service.create(
            #     payload={
            #         "user_id": user.id
            #     }, 
            #     user=user.model_dump(mode='json')
            # )

            return current_user
        except Exception as e:
            raise e


    async def list(
            self,
            payload: BaseModel,
            ip_address: str
        ) -> List[Organization]:
        """ List all the objects """
        try:
            # Validate the payload
            # user: User = await self.repository.forgot_password(payload)

            return payload
        except Exception as e:
            raise e


    async def get(
            self,
            payload: BaseModel,
            ip_address: str
        ) -> Organization:
        """ Get the object """
        try:
            # Validate the payload
            # user: User = await self.repository.change_password(payload)

            return payload
        except Exception as e:
            raise e
