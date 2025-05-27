""" Import the required modules """
import logging
from typing import List
from fastapi import Request
from pydantic import TypeAdapter, BaseModel

# Include the project models
from modules.core.models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)
from modules.core.models.organization import Organization

# include the project services
from modules.base.services.base import BaseService
from modules.base.services.auth.claim_service import ClaimService

# Include the module repositories
from modules.core.repositories.organization_repository import OrganizationRepository

# Include the module exceptions
from modules.base.exceptions.base import (
    EntityNotFoundException,
    EntityNotSavedException
)

# Include the module events
from ..events.organization_event import (
    OrganizationCreateEvent,
    OrganizationUpdateEvent,
    OrganizationDeleteEvent
)

# Initialize the logger
logger = logging.getLogger(__name__)

class OrganizationService(BaseService):
    """ OrganizationService class to handle organization related operations. """
    def __init__(self):
        self.repository = OrganizationRepository()
        self.claim_service = ClaimService()
        super().__init__(self.repository)


    async def create(
            self, payload: OrganizationCreateRequest, ip_address: str,
            current_user: BaseModel) -> Organization:
        """ Create a new object """
        try :
            # Validate the credentials
            model: Organization = await self.repository.save(
                payload, ip_address, current_user
            )
            if not model:
                raise EntityNotSavedException(
                    message="Unable to create the organization"
                )

            # Raise event on successful creation
            OrganizationCreateEvent().raise_event(model)

            return model
        except Exception as e:
            raise e


    async def update(
            self, uid: str, payload: OrganizationUpdateRequest,
            ip_address: str, current_user: BaseModel) -> Organization:
        """ Update the model """
        try:
            # Get the claim from storage
            model: Organization = await self.repository.update_by_hash(
                uid, payload, ip_address, current_user
            )
            if not model:
                raise EntityNotSavedException(
                    message="Unable to update the organization"
                )

            # Raise event on successful update
            OrganizationUpdateEvent().raise_event(model)

            return model
        except Exception as e:
            raise e


    async def delete(
            self, uid: str, ip_address: str,
            current_user: BaseModel) -> Organization:
        """ Delete the model """
        try:
            model: Organization = await self.repository.delete_by_hash(
                uid, ip_address, current_user
            )
            if not model:
                raise EntityNotFoundException(
                    message="Unable to delete the organization"
                )

            # Raise event on successful deletion
            OrganizationDeleteEvent().raise_event(model)

            return model
        except Exception as e:
            raise e


    async def list(
            self,
            commons: dict,
            request: Request,
            ip_address: str
        ) -> List[Organization]:
        """ List all the objects """
        try:
            # Validate the payload
            response = await self.repository.get_all(
                skip=commons.get("skip", 0),
                limit=commons.get("limit", 100),
            )
            logger.debug(f"Organization count: {len(response)}")
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the organizations from IP address."
                )
            
            # Validate the response
            models: List[Organization] = TypeAdapter(List[Organization]).validate_python(response)

            return models
        except Exception as e:
            raise e


    async def get(
            self,
            uid: str,
            ip_address: str
        ) -> Organization:
        """ Get the object """
        try:
            # Validate the payload
            response = await self.repository.get_by_hash(uid)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the organization from IP address = " + ip_address
                )

            # Validate the response
            model: Organization = TypeAdapter(Organization).validate_python(response)

            return model
        except Exception as e:
            raise e
