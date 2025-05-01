from typing import List

from ..services.service import UserService
from ..models.user import User

from modules.base.controller.base import BaseController

class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = UserService()

    async def index(self):
        return await self.service.index()

    async def show(self, hash: str):
        return await self.service.show(hash)

    async def create(self):
        return await self.service.create(User(1, "Amit", "amit@gmail.com"))

    async def update(self, hash: str):
        return await self.service.update(hash, User(1, "Amit", "amit@gmail.com"))

    async def delete(self, hash: str):
        return await self.service.delete(hash)
    