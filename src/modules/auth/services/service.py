""" Import the required modules """
import json
from typing import List
from pydantic import TypeAdapter

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
    """ AuthService class to handle authentication related operations. """
    def __init__(self):
        self.repository = AuthRepository()
        self.claim_service = ClaimService()


    async def authenticate(self, credentials: LoginRequest, ip_address: str) -> AuthClaim:
        """ Authenticare the user

        Authenticate the user with the given credentials and IP address.
        This method validates the credentials and generates a token for the user.
        If the authentication is successful, it returns the claim.

        If the authentication fails, it raises an exception.
        """
        try :
            # Validate the credentials
            authenticated_user: User = await self.repository.authenticate_user(
                credentials, ip_address
            )
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


    async def logout(self, token: str, is_forced: bool = False) -> bool:
        """ Logout the user

        Logout the user with the given access token.
        This method deletes the claim from storage.
        If the logout is successful, it returns True.
        If the logout fails, it raises an exception.
        """
        try:
            # Get the claim from storage
            claim = self.claim_service.get(value=token)
            if not claim:
                raise InvalidTokenException()

            if (is_forced is True) and (claim.token is not None):
                refresh_token = claim.token.refresh_token
                if refresh_token:
                    # Get all the claims for the user from refresh token
                    claims: List[AuthClaim] = self.claim_service.get_all(
                        {
                            refresh_token: refresh_token
                        }
                    )
                    if claims:
                        # Delete all the claims for the user
                        for claim in claims:
                            self.claim_service.delete(value=claim.token)
            else:
                # Delete the claim from storage
                self.claim_service.delete(value=token)

            # Raise event for successful logout

            return True
        except Exception as e:
            raise e


    async def register(self, payload: RegisterRequest, ip_address: str) -> dict:
        """ Register the user

        Register the user with the given payload and IP address.
        This method validates the payload and creates a new user.
        If the registration is successful, it returns the payload.
        If the registration fails, it raises an exception.
        """
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


    async def forgot_password(
            self,
            payload: ForgotPasswordRequest,
            ip_address: str
        ) -> dict:
        """ Send a forgot password request

        Send a forgot password request with the given payload.
        This method validates the payload and sends a reset password email.
        If the request is successful, it returns the confirmation.
        If the request fails, it raises an exception.
        """
        try:
            # Validate the payload
            # user: User = await self.repository.forgot_password(payload)

            return payload
        except Exception as e:
            raise e


    async def change_password(
            self,
            payload: ChangePasswordRequest,
            ip_address: str
        ) -> dict:
        """ Send a chnage password request

        Send a change password request with the given payload.
        This method validates the payload and updates the password.
        If the request is successful, it returns the confirmation.
        If the request fails, it raises an exception.
        """
        try:
            # Validate the payload
            # user: User = await self.repository.change_password(payload)

            return payload
        except Exception as e:
            raise e


    async def reset_password(
            self,
            payload: ChangePasswordRequest,
            ip_address: str
        ) -> dict:
        """ Send a chnage password request

        Send a change password request with the given payload.
        This method validates the payload and updates the password.
        If the request is successful, it returns the confirmation.
        If the request fails, it raises an exception.
        """
        try:
            # Validate the payload
            # user: User = await self.repository.change_password(payload)

            return payload
        except Exception as e:
            raise e


    async def refresh_token(
            self,
            token: str,
            ip_address: str
        ) -> AuthClaim:
        """ Refresh the access token

        Refresh the access token using the refresh token.
        This method validates the refresh token and generates a new 
        access token.
        """
        try:
            # Get the claim from storage
            claim = self.claim_service.get(value=token)
            if not claim:
                raise InvalidTokenException()
            
            print(f"Claim: {claim}")

            authenticated_user: User = TypeAdapter(User).validate_python(claim.user, experimental_allow_partial=True)
            if not authenticated_user:
                raise InvalidTokenException()

            # Create and store the claim
            claim: AuthClaim = self.claim_service.create(
                payload={
                    "user_id": authenticated_user.id
                },
                user=authenticated_user
            )

            # Delete the old claim from storage
            self.claim_service.delete(value=token)

            return claim
        except Exception as e:
            raise e
