""" Import the required modules """
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Include the project models
from ...models.auth.claim import AuthClaim
from modules.user.models.user import User

# Include the project services
from modules.base.services.auth.claim_service import ClaimService

# Include the project exceptions
from modules.base.exceptions import (
    InvalidTokenException,
    AuthenticationException
)


class AuthGaurd:
    access_token: str | None = None

    def __init__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))],
        claim_service: ClaimService = Depends(ClaimService)
    ):
        """ Initialize the AuthGaurd with the provided token and claim service.
        This class is used to validate the access token and retrieve the user
        associated with the token. If the token is not provided or invalid,
        an InvalidTokenException is raised.
        Args:
            token (HTTPAuthorizationCredentials): The access token provided in the request.
            claim_service (ClaimService): The service to handle claims and user retrieval.
        """
        try :
            if not token:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found"
                )
            self.access_token = token.credentials
            self.claim_service = claim_service
        except Exception as e:
            raise e


    def access_token(self) -> str:
        return self.access_token


    def valid_token(self)-> str:
        """
        Validate the access token and return it if valid.
        Raise an exception if invalid.
        """
        try:
            # This could be JWT validation.
            claim: AuthClaim = self.claim_service.get(value=self.access_token)
            if claim is None:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found1"
                )

            return self.access_token
        except (InvalidTokenException, Exception) as e:
            raise e


    def get_user(self) -> User:
        try:
            # This could be JWT validation.
            claim: AuthClaim = self.claim_service.get(value=self.access_token)
            if claim == None:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found2"
                )
            
            user = claim.user

            return user
        except (InvalidTokenException, Exception) as e:
            raise e

    
    # async def valid_token(self, token: str) -> str:
    #     try:
    #         # This could be JWT validation, looking up a session token in the DB, etc.
    #         return token
    #     except Exception as e:
    #         raise InvalidTokenException(message=str(e)) from e
  

    # async def get_user_for_token(token: str):
    #     return await User(1, "Amit", "amit@gmail.com")


    # async def validate_user(self):
        # try:
        #     user = await self.get_user_for_token(self.access_token)
        #     if user == None:
        #         raise HTTPException(status_code=401, detail="Unauthorized")
        #     return user
        # except:
        #     raise HTTPException(status_code=401, detail="Unauthorized")
    
# class TokenGuard_ValidUser(TokenGaurd_ValidToken):

#     async def __call__(self, request: Request = Depends(Request)):
#         user = await self.validate_user(request)
#         return user
    
# class TokenGuard_ValidPermissions(TokenGaurd_ValidToken):

#     async def __call__(self, request: Request = Depends(Request)):
#         user = await self.validate_permissions(request)
#         return user
    

auth = AuthGaurd