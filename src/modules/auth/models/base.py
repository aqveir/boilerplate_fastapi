from pydantic import BaseModel


class Auth(BaseModel):
    """Base model for authentication module."""


    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def __str__(self):
        return f'User: {self.id} - {self.name} - {self.email}'