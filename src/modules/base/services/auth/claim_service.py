import typing

from pydantic import BaseModel

from ...helpers.token import TokenHelper
from .token_service import TokenService

from ...models.auth.token import Token
from ...models.auth.claim import AuthClaim


from ...exceptions.base import *

#Load data from config file
from modules.base.config import config
from ..aws.dynamodb import DynamoDBService

class ClaimService:
    def __init__(self):
        self.token_service = TokenService()

        match config.CLAIM_STORAGE:
            case "dynamodb":
                # Initialize the DynamoDB service with the table name
                self.storage_service = DynamoDBService(table_name=config.CLAIM_TABLE_NAME)
            case _:
                raise NotImplementedError("Claim storage not implemented")


    """ Create a new claim
    Create a new claim with the given payload. The payload is usually
    the user data that will be included in the token. The claim is
    stored using the storage service.

    The claim is created using the TokenHelper class, which generates
    a JWT token with the given payload and expiration period.
    """
    def create(self, payload: dict, user: typing.Any) -> AuthClaim:
        # Generate a token
        token: Token = TokenHelper.encode(payload, expire_period=config.JWT_EXPIRES)
        if not token:
            raise InvalidTokenException(error_msg_code="error_code_token_generation")

        if isinstance(user, BaseModel):
            user = user.model_dump(mode='json')
        
        # Create a claim with the token and user data
        claim: AuthClaim = AuthClaim(token=token, user=user)
        if not claim:
            raise InvalidTokenException(error_msg_code="error_code_claim_generation")

        # Store the claim in storage
        self.store(claim)

        return claim


    def delete(self, value: str) -> bool:
        return self.storage_service.delete_data(value=value, key=config.CLAIM_TABLE_KEY)


    """ Get the claim from storage
    Get the claim from storage using the given value/identifier

    The value is usually the claim token. If the claim is found, it 
    returns the claim. If the claim is not found, it raises an exception.
    """
    def get(self, value: str) -> AuthClaim:
        return self.storage_service.get_data(value=value, key=config.CLAIM_TABLE_KEY)
    

    """ Store the claim in storage
    Save the claim in storage using the given claim object.

    The claim is includes JWT token or a session token along with the 
    user data.
    """
    def store(self, claim: AuthClaim) -> bool:
        response = self.storage_service.set_data(claim.model_dump())
        if not response:
            raise InvalidTokenException()
        else:
            return True

