""" Import the required modules """
import base64
import hashlib
import hmac
import boto3
from botocore.exceptions import ClientError
from modules.base.config import config

logger = config.get_logger(__name__)

client = boto3.client(
    "cognito-idp", 
    region_name=config.AWS_COGNITO_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)


class CognitoService():
    """
    Memcached cache backend implementation using AWS ElastiCache.

    This class implements the ICache interface and provides methods to 
    interact with a Memcached cache.
    It uses the AWS SDK for Python (Boto3) to interact with AWS ElastiCache.
    """
    def __init__(self):
        self.client = client
        self.user_pool_id = config.AWS_COGNITO_USER_POOL_ID
        self.client_id = config.AWS_COGNITO_CLIENT_ID
        self.client_secret = config.AWS_COGNITO_CLIENT_SECRET



    async def authenticate(self, user_name, password):
        """
        Starts the sign-in process for a user by using administrator credentials.
        This method of signing in is appropriate for code running on a secure server.

        If the user pool is configured to require MFA and this is the first sign-in
        for the user, Amazon Cognito returns a challenge response to set up an
        MFA application. When this occurs, this function gets an MFA secret from
        Amazon Cognito and returns it to the caller.

        :param user_name: The name of the user to sign in.
        :param password: The user's password.
        :return: The result of the sign-in attempt. When sign-in is successful, this
                 returns an access token that can be used to get AWS credentials. Otherwise,
                 Amazon Cognito returns a challenge to set up an MFA application,
                 or a challenge to enter an MFA code from a registered MFA application.
        """
        try:
            payload: dict[str, str] = {
                "UserPoolId": self.user_pool_id,
                "ClientId": self.client_id,
                "AuthFlow": "ADMIN_USER_PASSWORD_AUTH",
                "AuthParameters": {
                    "USERNAME": user_name,
                    "PASSWORD": password
                },
            }

            if self.client_secret is not None:
                payload["AuthParameters"]["SECRET_HASH"] = self._secret_hash(user_name)

            # Log the payload for debugging purposes
            logger.debug("Payload: %s", payload)

            # Start the sign-in process
            response = self.client.admin_initiate_auth(**payload)

            # Handle the response
            if "ChallengeName" in response:
                challenge_name = response.get("ChallengeName", None)

                if challenge_name == "NEW_PASSWORD_REQUIRED":
                    # The user is required to set a new password
                    raise RuntimeError(
                        "The user is required to set a new password. "
                        "Please use the AdminSetUserPassword API to set a new password."
                    )
                elif challenge_name == "MFA_SETUP":
                    if (
                        "SOFTWARE_TOKEN_MFA"
                        in response["ChallengeParameters"]["MFAS_CAN_SETUP"]
                    ):
                        response.update(self.get_mfa_secret(response["Session"]))
                    else:
                        raise RuntimeError(
                            "The user pool requires MFA setup, but the user pool is not "
                            "configured for TOTP MFA. This example requires TOTP MFA."
                        )
                elif challenge_name == "SOFTWARE_TOKEN_MFA":
                    # The user is required to enter an MFA code from 
                    # a registered MFA application
                    raise RuntimeError(
                        "The user is required to enter an MFA code" \
                        "from a registered MFA application."
                    )

            response.pop("ResponseMetadata", None)
            return response
        except ClientError as err:
            logger.error(
                "Couldn't start sign in for %s. Here's why: %s: %s",
                user_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise


    def _secret_hash(self, user_name: str) -> str:
        """
        Returns the secret hash for the user.

        :param user_name: The name of the user.
        :return: The secret hash for the user.
        """
        if self.client_secret is None:
            return None
        message = f"{user_name}{self.client_id}"
        dig = hmac.new(
            self.client_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
        )
        return base64.b64encode(dig.digest()).decode()

    def get_mfa_secret(self, session: str) -> dict[str, str]:
        """
        Returns the MFA secret for the user.

        :param session: The session ID.
        :return: The MFA secret for the user.
        """
        try:
            response = self.client.admin_respond_to_auth_challenge(
                UserPoolId=self.user_pool_id,
                ClientId=self.client_id,
                ChallengeName="SOFTWARE_TOKEN_MFA",
                Session=session,
                ChallengeResponses={
                    "SOFTWARE_TOKEN_MFA_CODE": "123456",
                    "SECRET_HASH": self._secret_hash("user_name"),
                },
            )
            return response
        except ClientError as err:
            logger.error(
                "Couldn't get MFA secret. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    async def logout(self, access_token: str) -> None:
        """
        Logs out the user from the user pool.

        :param access_token: The access token of the user.
        :return: None
        """
        try:
            self.client.global_sign_out(AccessToken=access_token)
        except ClientError as err:
            logger.error(
                "Couldn't log out user. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
