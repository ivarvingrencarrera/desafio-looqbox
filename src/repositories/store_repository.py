from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.entities import Store
from src.models import StoreModel


class StoreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, store_id: int) -> Store | None:
        query = (
            select(StoreModel)
            .where(store_id == StoreModel.STORE_CODE)  # type: ignore[arg-type]
            .order_by(StoreModel.STORE_CODE)
        )
        try:
            result = await self.session.execute(query)
            store_model = result.scalar_one()
            return store_model.to_entity()
        except NoResultFound:
            return None

    async def find_all(self) -> list[Store]:
        query = select(StoreModel).distinct().order_by(StoreModel.STORE_CODE)
        result = await self.session.execute(query)
        store_models = result.scalars().all()
        return [store_model.to_entity() for store_model in store_models]
