""" Import the required modules """
from abc import ABC


class BaseService(ABC):
    """Base class for services."""
    def __init__(self, repository=None):
        self.repository = repository
