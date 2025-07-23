from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import asc, desc, select
from sqlalchemy.sql.functions import func

from src.entities import Product
from src.enums import ProductSortByEnum, ProductSortOrderEnum
from src.models import ProductModel, ProductSaleModel
from src.value_objects import Sale


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

    async def find_product_sales(
        self, product_id: int, start_date: str, end_date: str, store_id: int | None = None
    ) -> list[Sale]:
        query = (
            select(
                ProductSaleModel.DATE,
                func.sum(ProductSaleModel.SALES_VALUE).label('total_value'),
                func.sum(ProductSaleModel.SALES_QTY).label('total_quantity'),
            )
            .where(
                product_id == ProductSaleModel.PRODUCT_CODE,  # type: ignore[arg-type]
                store_id == ProductSaleModel.STORE_CODE if store_id is not None else True,  # type: ignore[arg-type]
                ProductSaleModel.DATE.between(start_date, end_date),
            )
            .group_by(ProductSaleModel.DATE)
            .order_by(ProductSaleModel.DATE)
        )
        result = await self.session.execute(query)
        product_sales = result.all()
        return [
            Sale(
                value=product_sale.total_value,
                quantity=product_sale.total_quantity,
                date=product_sale.DATE,
            )
            for product_sale in product_sales
        ]
