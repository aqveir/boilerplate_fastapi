""" Import the required modules """
from pydantic_settings import BaseSettings


class CoreConfig(BaseSettings):
    """
    CoreConfig class to handle core related configurations.
    """
    # Define your configuration variables here
    # For example:
    # DATABASE_URL: str = "sqlite:///./test.db"
