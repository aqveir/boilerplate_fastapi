""" Import the required modules """
from typing import TypeVar, Type, Generic

from sqlalchemy import delete, select, update

from modules.base.db.session import Base, session
from modules.base.repository.enum import SynchronizeSessionEnum

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    BaseRepository class to handle database operations for a given model.
    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model: Type[T]):
        self.model = model

    ### Get all the table data
    async def get_all(self) -> list[T]:
        """
        Get all the table data
        :return: list of all the table data
        """
        ############# Get all the table data #############
        query = select(self.model)
        return await session.execute(query).scalars().all

    ### Get the table data by id
    async def get_by_id(self, id: int) -> T:
        query = select(self.model).where(self.model.id == id)
        return await session.execute(query).scalars().first()

    ### Get the table data by hash
    async def get_by_hash(self, uid: str) -> T:
        query = select(self.model).where(self.model.hash == uid)
        return await session.execute(query).scalars().first()

    ### Update the table data by id
    async def update_by_id(
        self,
        id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum,
    ) -> T:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**params)
            #.execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Update the table data by hash
    async def update_by_hash(
        self,
        uid: str,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum,
    ) -> T:
        """
        Update the table data by hash
        :param uid: hash of the table data
        :param params: parameters to update
        :param synchronize_session: synchronize session
        :return: updated table data
        """
        ############# Update the table data by hash #############
        query = (
            update(self.model)
                .where(self.model.hash == uid)
                .values(**params)
                #.execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Truncate the table
    async def truncate(self) -> None:
        query = delete(self.model)
        await session.execute(query)

    ### Delete the table data
    async def delete(self, model: T) -> T:
        await session.delete(model)

    ### Delete the table data by id
    async def delete_by_id(
        self,
        id: int,
        synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == id)
            #.execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Delete the table data by hash
    async def delete_by_hash(
        self,
        uid: str,
        synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum,
    ) -> T:
        query = (
            delete(self.model)
            .where(self.model.hash == uid)
            #.execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Save the table data
    async def save(self, model: T) -> T:
        saved = await session.add(model)
        return saved
