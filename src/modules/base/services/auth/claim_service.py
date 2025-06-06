""" Import the required modules """
import typing
from typing import List

from pydantic import BaseModel, TypeAdapter

from modules.base.models.auth.token import Token
from modules.base.models.auth.claim import AuthClaim

# Exception classes
from modules.base.exceptions import (
    InvalidTokenException
)

# Load data from config file
from modules.base.config import config
from modules.base.services.aws.dynamodb import DynamoDBService

from modules.base.helpers.token import TokenHelper
from .token_service import TokenService


class ClaimService:
    """ ClaimService class to handle claims related operations.

    This class is responsible for creating, deleting and retrieving claims.
    It uses the TokenService to generate tokens and the storage service
    to store the claims.
    """

    def __init__(self):
        self.token_service = TokenService()

        match config.CLAIM_STORAGE:
            case "dynamodb":
                # Initialize the DynamoDB service with the table name
                self.storage_service = DynamoDBService(table_name=config.CLAIM_TABLE_NAME)
            case _:
                raise NotImplementedError("Claim storage not implemented")


    def create(self, payload: dict, user: typing.Any) -> AuthClaim:
        """ Create a new claim
        Create a new claim with the given payload. The payload is usually
        the user data that will be included in the token. The claim is
        stored using the storage service.

        The claim is created using the TokenHelper class, which generates
        a JWT token with the given payload and expiration period.
        """

        try:
            # Validate the payload
            if not isinstance(payload, dict):
                raise InvalidTokenException(
                    error_msg_code="error_code_invalid_payload",
                    message="Payload must be a dictionary"
                )

            # Generate a token
            token: Token = TokenHelper.encode(payload, expire_period=config.JWT_EXPIRES)
            if not token:
                raise InvalidTokenException(
                    error_msg_code="error_code_token_generation",
                    message="Failed to generate token from payload"
                )

            if isinstance(user, BaseModel):
                user = user.model_dump(mode='json', exclude_none=True)

            # Create a claim with the token and user data
            claim: AuthClaim = AuthClaim(token=token, user=user)
            if not claim:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_generation",
                    message="Failed to generate claim from token"
                )

            # Store the claim in storage
            self.store(claim)

            return claim
        except (InvalidTokenException, Exception) as e:
            raise e


    def delete(self, value: str) -> bool:
        """ Delete the claim from storage
        Delete the claim from storage using the given value/identifier.
        The value is usually the claim token. If the claim is found, it
        deletes the claim and returns True. If the claim is not found, it
        raises an exception.
        """
        return self.storage_service.delete_data(
            value=value,
            key=config.CLAIM_TABLE_KEY
        )


    def get(self, value: str) -> AuthClaim:
        """ Get the claim from storage
        Get the claim from storage using the given value/identifier

        The value is usually the claim token. If the claim is found, it 
        returns the claim. If the claim is not found, it raises an exception.
        """
        try:
            # Get the claim from storage
            claim = self.storage_service.get_data(
                value=value,
                key=config.CLAIM_TABLE_KEY
            )
            if not claim:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found",
                    message="Claim not found for the given value"
                )

            # Validate the claim using TypeAdapter
            ta: TypeAdapter = TypeAdapter(AuthClaim)
            return ta.validate_python(claim)
        except (InvalidTokenException, Exception):
            raise


    def get_all(self, query: dict) -> List[AuthClaim]:
        """ Get all the claims from storage
        Get the claims from storage using the given query/identifier

        The values are usually the claim tokens. If the claims are found, it 
        returns the list of the claims. If the claim is not found, it 
        raises an exception.
        """
        try:
            # Get the claim from storage
            claims = self.storage_service.query_data(
                query=query
            )
            if not claims:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found",
                    message="Claims not found in the storage"
                )
            
            # Validate the claim using TypeAdapter
            ta: TypeAdapter = TypeAdapter(List[AuthClaim])
            return ta.validate_python(claims)
        except (InvalidTokenException, Exception) as e:
            raise e


    def store(self, claim: AuthClaim) -> bool:
        """ Store the claim in storage
        Save the claim in storage using the given claim object.

        The claim is includes JWT token or a session token along with the 
        user data.
        """
        try:
            response = self.storage_service.set_data(
                claim.model_dump(mode='python', exclude_none=True),
            )
            if not response:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_storage_failed",
                    message="Failed to store claim in the storage"
                )

            return True
        except (InvalidTokenException, Exception) as e:
            raise e
