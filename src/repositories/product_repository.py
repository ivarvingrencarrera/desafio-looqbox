from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import asc, desc, select
from sqlalchemy.sql.functions import func

from src.entities import Product
from src.enums import ProductSortByEnum, ProductSortOrderEnum
from src.models import ProductModel


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, product_id: int) -> Product | None:
        query = select(ProductModel).where(product_id == ProductModel.PRODUCT_COD)  # type: ignore[arg-type]
        try:
            result = await self.session.execute(query)
            product_model = result.scalar_one()
            return product_model.to_entity()
        except NoResultFound:
            return None

    async def find_all(
        self, sort_by: ProductSortByEnum, sort_order: ProductSortOrderEnum, limit: int
    ) -> list[Product]:
        sort_column = (
            ProductModel.PRODUCT_VAL
            if sort_by == ProductSortByEnum.PRICE
            else func.ltrim(ProductModel.PRODUCT_NAME)
            if sort_by == ProductSortByEnum.NAME
            else None
        )
        sort_direction = desc if sort_order == ProductSortOrderEnum.DESC else asc
        query = select(ProductModel).order_by(sort_direction(sort_column)).limit(limit)
        result = await self.session.execute(query)
        product_models = result.scalars().all()
        return [product_model.to_entity() for product_model in product_models]
