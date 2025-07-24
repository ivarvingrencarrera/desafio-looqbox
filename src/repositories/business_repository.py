from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.sql.functions import func

from src.entities import Business
from src.models import ProductSaleModel, StoreModel


class BusinessRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, business_id: int) -> Business | None:
        query = (
            select(StoreModel.BUSINESS_CODE, StoreModel.BUSINESS_NAME)
            .distinct()
            .where(business_id == StoreModel.BUSINESS_CODE)  # type: ignore[arg-type]
            .order_by(StoreModel.BUSINESS_CODE)
        )
        try:
            result = await self.session.execute(query)
            business = result.one()
            return Business(id=business[0], name=business[1])
        except NoResultFound:
            return None

    async def find_all(self) -> list[Business]:
        query = (
            select(StoreModel.BUSINESS_CODE, StoreModel.BUSINESS_NAME)
            .distinct()
            .order_by(StoreModel.BUSINESS_CODE)
        )
        result = await self.session.execute(query)
        business = result.all()
        return [Business(id=cod, name=name) for cod, name in business]

    async def find_total_sales(self, start_date: str, end_date: str) -> list[Business]:
        query = (
            select(
                StoreModel.BUSINESS_CODE,
                StoreModel.BUSINESS_NAME,
                func.sum(ProductSaleModel.SALES_VALUE).label('total_sales'),
            )
            .join(StoreModel, ProductSaleModel.STORE_CODE == StoreModel.STORE_CODE)
            .where(ProductSaleModel.DATE.between(start_date, end_date))
            .group_by(StoreModel.BUSINESS_CODE, StoreModel.BUSINESS_NAME)
            .order_by(StoreModel.BUSINESS_CODE)
        )
        result = await self.session.execute(query)
        sales_data = result.all()
        return [
            Business(id=cod, name=name, total_sales=sales_value)
            for cod, name, sales_value in sales_data
        ]
