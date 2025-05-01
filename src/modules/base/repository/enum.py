""" Import the required modules """
from pydantic import BaseModel


class SynchronizeSessionEnum(BaseModel):
    """ Synchronize session enum class """
    FETCH: str = "fetch"
    EVALUATE: str = "evaluate"
    FALSE: bool = False
