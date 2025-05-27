""" Import the required modules """
from modules.base.repository import BaseRepository

# Import the schema and model classes
from modules.core.schemas import OrganizationSchema


class OrganizationRepository(BaseRepository[OrganizationSchema]):
    """
    OrganizationRepository class to handle organization related database operations.
    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model = OrganizationSchema):
        self.model = model
        super().__init__(model)
