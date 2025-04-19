import json
from typing import List

# Include the project models
from ..models.base import Auth
from ..models.request import *
from modules.user.models.user import User
from modules.base.models.auth.claim import AuthClaim

# include the project services
from modules.base.services.base import BaseService
from modules.base.services.auth.claim_service import ClaimService

# Include the module repositories
from ..repositories.repository import AuthRepository

# Include the module events
from ..events.login_event import LoginEvent

# Include the module exceptions
from modules.base.exceptions.base import *

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()
        self.claim_service = ClaimService()
  

    """ Authenticare the user

    Authenticate the user with the given credentials and IP address.
    This method validates the credentials and generates a token for the user.
    If the authentication is successful, it returns the claim.

    If the authentication fails, it raises an exception.
    """
    async def authenticate(self, credentials: LoginRequest, ip_address: str):
        try :
            # Validate the credentials
            authenticated_user: User = await self.repository.authenticate_user(credentials)
            if not authenticated_user:
                raise AuthenticationException()
            else:
                # Create and store the claim
                claim: AuthClaim = self.claim_service.create(
                    payload={
                        "user_id": authenticated_user.id
                    }, 
                    user=authenticated_user
                )

                # Set update the user status

                # Raise event for successful login
                LoginEvent().raise_event(claim)

            return claim
        except Exception as e:
            raise e


    """ Logout the user

    Logout the user with the given access token.
    This method deletes the claim from storage.
    If the logout is successful, it returns True.
    If the logout fails, it raises an exception.
    """
    async def logout(self, token: str, is_forced: bool = False) -> bool:
        try:
            # Get the claim from storage
            claim = self.claim_service.get(value=token)
            if not claim:
                raise InvalidTokenException()
            else:
                # Delete the claim from storage
                self.claim_service.delete(value=token)

                # Raise event for successful logout

                return True
        except Exception as e:
            raise e


    """ Register the user

    Register the user with the given payload and IP address.
    This method validates the payload and creates a new user.
    If the registration is successful, it returns the payload.
    If the registration fails, it raises an exception.
    """
    async def register(self, payload: RegisterRequest, ip_address: str) -> dict:
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

            return payload
        except Exception as e:
            raise e

    # async def create(self, user: User):
    #     return await self.repository.create()

    # async def update(self, hash: str, user: User):
    #     return await self.repository.update(hash)

    # async def delete(self, hash: str):
    #     return await self.repository.delete(hash)