from ...models.auth.token import Token as AuthToken
import jwt

#Load data from config file
from modules.base.config import config

class TokenService:
    auth_token: AuthToken

    def __init__(self):
        pass

    def create(self, expires_at: int, hash: str) -> AuthToken:
        token = jwt.encode(
            {
                "hash": hash, 
                "exp": expires_at
            }, 
            key=config.JWT_SECRET_KEY, 
            algorithm=[config.JWT_ALGORITHM]
        )
        self.auth_token(token)
        return token

    def get(self) -> AuthToken:
        return self.auth_token

    def decode(self, token: AuthToken) -> dict:
        return jwt.decode(token, 
            key=config.JWT_SECRET_KEY, 
            algorithm=[config.JWT_ALGORITHM]
        )