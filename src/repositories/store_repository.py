from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.sql.functions import func

from src.entities import Store
from src.models import StoreModel, StoreSaleModel
from src.value_objects import Sale


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

    async def find_store_sales(self, store_id: int, start_date: str, end_date: str) -> list[Sale]:
        query = (
            select(
                StoreSaleModel.DATE,
                func.sum(StoreSaleModel.SALES_VALUE).label('total_value'),
                func.sum(StoreSaleModel.SALES_QTY).label('total_quantity'),
            )
            .where(
                store_id == StoreSaleModel.STORE_CODE,  # type: ignore[arg-type]
                StoreSaleModel.DATE.between(start_date, end_date),
            )
            .group_by(StoreSaleModel.DATE)
            .order_by(StoreSaleModel.DATE)
        )
        result = await self.session.execute(query)
        store_sales = result.all()
        return [
            Sale(
                value=store_sale.total_value,
                quantity=store_sale.total_quantity,
                date=store_sale.DATE,
            )
            for store_sale in store_sales
        ]
