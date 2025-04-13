#from modules.core.repository.base import BaseRepository
from modules.user.models.user import User

class UserRepository():
    def __init__(self):
        #super().__init__(User)
        pass

    async def index(self):
        return 'UserRepository index'

    async def show(self, hash: str):
        return f'UserRepository show {hash}'

    async def create(self):
        return 'UserRepository create'

    async def update(self, hash: str):
        return f'UserRepository update {hash}'

    async def delete(self, hash: str):
        return f'UserRepository delete {hash}'