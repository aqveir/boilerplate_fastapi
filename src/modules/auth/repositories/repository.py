#from modules.core.repository.base import BaseRepository
from fastapi.responses import JSONResponse

from modules.auth.models.base import Auth
from modules.user.models.user import User
from modules.core.models.organization import Organization

from ..models.request import LoginRequest

class AuthRepository():
    def __init__(self):
        #super().__init__(Auth)
        pass

    async def authenticate_user(self, credentials: LoginRequest) -> User:
        return User(
            id=1,
            username=credentials.username,
            organization=Organization(
                id=1,
                display_name="My Organization",
                legal_name="My Organization Inc"
            )
        )
    
    async def show(self, hash: str):
        return f'UserRepository show {hash}'

    async def create(self):
        return 'UserRepository create'

    async def update(self, hash: str):
        return f'UserRepository update {hash}'

    async def delete(self, hash: str):
        return f'UserRepository delete {hash}'