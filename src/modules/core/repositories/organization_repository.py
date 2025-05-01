""" Import the required modules """

from modules.base.repository.base import BaseRepository

from ..models.organization.organization import Organization


class OrganizationRepository(BaseRepository[Organization]):
    """
    OrganizationRepository class to handle organization related database operations.
    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model: Organization):
        self.model = model
        self.session = None
        super().__init__(model)
