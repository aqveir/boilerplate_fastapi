from typing import TypeVar, Type, Generic

from sqlalchemy import delete, select, update

from modules.base.db.session import Base, session
from modules.base.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    ### Get all the table data
    async def get_all(self) -> list[ModelType]:
        query = select(self.model)
        return await session.execute(query).scalars().all

    ### Get the table data by id
    async def get_by_id(self, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        return await session.execute(query).scalars().first()
    
    ### Get the table data by hash
    async def get_by_hash(self, hash: str) -> ModelType | None:
        query = select(self.model).where(self.model.hash == hash)
        return await session.execute(query).scalars().first()

    ### Update the table data by id
    async def update_by_id(
        self,
        id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Update the table data by hash
    async def update_by_hash(
        self,
        hash: str,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.hash == hash)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Truncate the table
    async def truncate(self) -> None:
        query = delete(self.model)
        await session.execute(query)

    ### Delete the table data
    async def delete(self, model: ModelType) -> None:
        await session.delete(model)

    ### Delete the table data by id
    async def delete_by_id(
        self,
        id: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Delete the table data by hash
    async def delete_by_hash(
        self,
        hash: str,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.hash == hash)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    ### Save the table data
    async def save(self, model: ModelType) -> ModelType:
        saved = await session.add(model)
        return saved
