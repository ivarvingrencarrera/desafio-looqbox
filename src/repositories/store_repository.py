from collections import defaultdict

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Label, literal, select
from sqlalchemy.sql.functions import func

from src.entities import Store
from src.enums import GroupByPeriodEnum
from src.exceptions import FeatureNotAvailableError
from src.models import StoreModel, StoreSaleModel
from src.value_objects import DateTime, Sale


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

    async def find_all(self, store_ids: list[int] | None = None) -> list[Store]:
        query = select(StoreModel).distinct().order_by(StoreModel.STORE_CODE)
        if store_ids:
            query = query.where(StoreModel.STORE_CODE.in_(store_ids))
        result = await self.session.execute(query)
        store_models = result.scalars().all()
        return [store_model.to_entity() for store_model in store_models]

    async def find_sales(
        self,
        store_ids: list[int],
        start_date: str,
        end_date: str,
        group_by: GroupByPeriodEnum,
    ) -> dict[int, list[Sale]]:
        if group_by == GroupByPeriodEnum.TOTAL:
            query = (
                select(
                    StoreSaleModel.STORE_CODE,
                    func.sum(StoreSaleModel.SALES_VALUE).label('total_value'),
                    func.sum(StoreSaleModel.SALES_QTY).label('total_quantity'),
                )
                .where(
                    StoreSaleModel.STORE_CODE.in_(store_ids),
                    StoreSaleModel.DATE.between(start_date, end_date),
                )
                .group_by(StoreSaleModel.STORE_CODE)
                .order_by(StoreSaleModel.STORE_CODE)
            )
        else:
            period_expr = self.build_period_expr(group_by)
            query = (
                select(
                    StoreSaleModel.STORE_CODE,
                    period_expr,
                    func.sum(StoreSaleModel.SALES_VALUE).label('total_value'),
                    func.sum(StoreSaleModel.SALES_QTY).label('total_quantity'),
                )
                .where(
                    StoreSaleModel.STORE_CODE.in_(store_ids),
                    StoreSaleModel.DATE.between(start_date, end_date),
                )
                .group_by(StoreSaleModel.STORE_CODE, period_expr)
                .order_by(StoreSaleModel.STORE_CODE)
            )
        result = await self.session.execute(query)
        store_sales = result.all()
        store_sales_dict: dict[int, list[Sale]] = defaultdict(list)
        for row in store_sales:
            store_sales_dict[row.STORE_CODE].append(
                Sale(
                    value=row.total_value,
                    quantity=int(row.total_quantity),
                    date=DateTime(row.period) if group_by != GroupByPeriodEnum.TOTAL else None,
                )
            )
        return dict(store_sales_dict)

    @staticmethod
    def build_period_expr(group_by: GroupByPeriodEnum) -> Label:
        match group_by:
            case GroupByPeriodEnum.DAILY:
                return func.date(StoreSaleModel.DATE).label('period')
            case GroupByPeriodEnum.WEEKLY:
                return func.concat(
                    func.year(StoreSaleModel.DATE),
                    literal('-W'),
                    func.lpad(func.week(StoreSaleModel.DATE, 3), 2, '0'),  # modo 3 = ISO 8601
                ).label('period')
            case GroupByPeriodEnum.MONTHLY:
                return func.date_format(StoreSaleModel.DATE, '%Y-%m-01').label('period')
            case GroupByPeriodEnum.YEARLY:
                return func.date_format(StoreSaleModel.DATE, '%Y-01-01').label('period')
        raise FeatureNotAvailableError
