from collections import defaultdict

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Label, literal, select
from sqlalchemy.sql.functions import func

from src.entities import Business
from src.enums import GroupByPeriodEnum
from src.exceptions import FeatureNotAvailableError
from src.models import ProductSaleModel, StoreModel
from src.value_objects import DateTime, Sale


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

    async def find_all(self, business_ids: list[int] | None = None) -> list[Business]:
        query = (
            select(StoreModel.BUSINESS_CODE, StoreModel.BUSINESS_NAME)
            .distinct()
            .order_by(StoreModel.BUSINESS_CODE)
        )
        if business_ids:
            query = query.where(StoreModel.BUSINESS_CODE.in_(business_ids))
        result = await self.session.execute(query)
        business = result.all()
        return [Business(id=cod, name=name) for cod, name in business]

    async def find_sales(
        self,
        business_ids: list[int],
        start_date: str,
        end_date: str,
        group_by: GroupByPeriodEnum,
    ) -> dict[int, list[Sale]]:
        if group_by == GroupByPeriodEnum.TOTAL:
            query = (
                select(
                    StoreModel.BUSINESS_CODE,
                    func.sum(ProductSaleModel.SALES_VALUE).label('total_value'),
                    func.sum(ProductSaleModel.SALES_QTY).label('total_quantity'),
                )
                .join(StoreModel, ProductSaleModel.STORE_CODE == StoreModel.STORE_CODE)
                .where(
                    StoreModel.BUSINESS_CODE.in_(business_ids),
                    ProductSaleModel.DATE.between(start_date, end_date),
                )
                .group_by(StoreModel.BUSINESS_CODE)
                .order_by(StoreModel.BUSINESS_CODE)
            )
        else:
            period_expr = self.build_period_expr(group_by)
            query = (
                select(
                    StoreModel.BUSINESS_CODE,
                    period_expr,
                    func.sum(ProductSaleModel.SALES_VALUE).label('total_value'),
                    func.sum(ProductSaleModel.SALES_QTY).label('total_quantity'),
                )
                .join(StoreModel, ProductSaleModel.STORE_CODE == StoreModel.STORE_CODE)
                .where(
                    StoreModel.BUSINESS_CODE.in_(business_ids),
                    ProductSaleModel.DATE.between(start_date, end_date),
                )
                .group_by(StoreModel.BUSINESS_CODE, period_expr)
                .order_by(StoreModel.BUSINESS_CODE)
            )
        result = await self.session.execute(query)
        businesses_sales = result.all()
        businesses_sales_dict: dict[int, list[Sale]] = defaultdict(list)
        for row in businesses_sales:
            businesses_sales_dict[row.BUSINESS_CODE].append(
                Sale(
                    value=row.total_value,
                    quantity=int(row.total_quantity),
                    date=DateTime(row.period) if group_by != GroupByPeriodEnum.TOTAL else None,
                )
            )
        return dict(businesses_sales_dict)

    @staticmethod
    def build_period_expr(group_by: GroupByPeriodEnum) -> Label:
        match group_by:
            case GroupByPeriodEnum.DAILY:
                return func.date(ProductSaleModel.DATE).label('period')
            case GroupByPeriodEnum.WEEKLY:
                return func.concat(
                    func.year(ProductSaleModel.DATE),
                    literal('-W'),
                    func.lpad(func.week(ProductSaleModel.DATE, 3), 2, '0'),  # modo 3 = ISO 8601
                ).label('period')
            case GroupByPeriodEnum.MONTHLY:
                return func.date_format(ProductSaleModel.DATE, '%Y-%m-01').label('period')
            case GroupByPeriodEnum.YEARLY:
                return func.date_format(ProductSaleModel.DATE, '%Y-01-01').label('period')
        raise FeatureNotAvailableError
