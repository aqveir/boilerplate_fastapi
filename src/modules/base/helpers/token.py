from datetime import datetime, timedelta, timezone

import jwt

from modules.base.config import config
#from modules.core.exceptions import GenericBaseException

from ..models.auth.token import Token


class DecodeTokenException(Exception):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(Exception):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"


class TokenHelper:
    @staticmethod
    def encode(payload: dict, subject: str=None, expire_period: int = 3600) -> Token:
        # Set the expiration time
        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=expire_period)

        # Set the payload
        token: Token = Token()
        token.access_token = jwt.encode(
            payload={
                **payload,
                "exp": expires_at,                      # expiration time
                "iat": datetime.now(tz=timezone.utc),   # issued at
                "nbf": datetime.now(tz=timezone.utc),   # not before
                "iss": config.JWT_ISSUER,               # issuer
                "aud": config.JWT_AUDIENCE,             # audience
                "sub": subject,                         # subject
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        token.expires_at = int(expires_at.timestamp())
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
