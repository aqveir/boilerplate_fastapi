from typing import List

from ..repositories.repository import UserRepository
from ..models.user import User

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def index(self):
        return await self.repository.index()

    async def show(self, hash: str):
        return await self.repository.show(hash)

    async def create(self, user: User):
        return await self.repository.create()

    async def update(self, hash: str, user: User):
        return await self.repository.update(hash)

    async def delete(self, hash: str):
        return await self.repository.delete(hash)