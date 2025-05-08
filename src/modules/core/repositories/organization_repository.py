""" Import the required modules """
from modules.base.repository.base import BaseRepository

# Import the schema and model classes
from modules.core.schemas.organization import OrganizationSchema


class OrganizationRepository(BaseRepository[OrganizationSchema]):
    """
    OrganizationRepository class to handle organization related database operations.
    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model = OrganizationSchema):
        self.model = model
        super().__init__(model, model.db_session)


    async def get_by_uid(self, uid: str, join_: set[str] | None = None) -> OrganizationSchema:
        """
        Returns the model instance matching the id.

        :param id_: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """

        db_obj = await self.get_by(
            field="hash", value=uid, join_=join_, unique=True
        )
        # if not db_obj:
        #     raise NotFoundException(
        #         f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
        #     )

        return db_obj
