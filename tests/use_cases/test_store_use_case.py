from unittest.mock import AsyncMock

import pytest

from src.entities import Store
from src.enums import CalculationType, GroupByPeriodEnum
from src.exceptions import StoreNotFoundError
from src.repositories import StoreRepository
from src.schemas import (
    StoreOutputSchema,
    StoreSalesOutputSchema,
    StoresSalesInputSchema,
    StoresSalesOutputSchema,
)
from src.use_cases import StoreUseCase


async def test_find_store(
    store: Store,
    store_use_case: StoreUseCase,
    store_repository: StoreRepository,
) -> None:
    store_repository.find = AsyncMock(return_value=store)
    output = await store_use_case.find_store(store_id=store.id)
    assert output == StoreOutputSchema.from_entity(store)


async def test_find_store_not_found(
    store_use_case: StoreUseCase, store_repository: StoreRepository
) -> None:
    store_repository.find = AsyncMock(return_value=None)
    with pytest.raises(StoreNotFoundError) as error:
        await store_use_case.find_store(store_id=999)
    assert str(error.value) == StoreNotFoundError.message


async def test_find_stores(
    store: Store,
    store_use_case: StoreUseCase,
    store_repository: StoreRepository,
) -> None:
    store_repository.find_all = AsyncMock(return_value=[store])
    output = await store_use_case.find_stores()
    assert output == [StoreOutputSchema.from_entity(store)]


@pytest.mark.parametrize(
    'group_by',
    [
        GroupByPeriodEnum.DAILY,
        GroupByPeriodEnum.WEEKLY,
        GroupByPeriodEnum.MONTHLY,
        GroupByPeriodEnum.YEARLY,
        GroupByPeriodEnum.TOTAL,
    ],
)
async def test_find_stores_sales_average(
    store: Store,
    store_use_case: StoreUseCase,
    store_repository: StoreRepository,
    group_by: GroupByPeriodEnum,
) -> None:
    store_repository.find_all = AsyncMock(return_value=[store])
    sales = {store.id: store.sales}
    store_repository.find_sales = AsyncMock(return_value=sales)
    calculation = CalculationType.AVERAGE
    input_data = StoresSalesInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        calculation=calculation,
        group_by=group_by,
    )
    output = await store_use_case.find_stores_sales(input_data=input_data)
    assert output == StoresSalesOutputSchema(
        calculation=calculation,
        group_by=input_data.group_by,
        start_date=input_data.start_date,
        end_date=input_data.end_date,
        stores=[StoreSalesOutputSchema.from_entity(store, calculation, group_by)],
    )


async def test_find_stores_sales_no_stores(
    store_use_case: StoreUseCase,
    store_repository: StoreRepository,
) -> None:
    store_repository.find_all = AsyncMock(return_value=[])
    input_data = StoresSalesInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        calculation=CalculationType.TOTAL,
    )
    output = await store_use_case.find_stores_sales(input_data=input_data)
    assert output == StoresSalesOutputSchema(
        calculation=input_data.calculation,
        group_by=input_data.group_by,
        start_date=input_data.start_date,
        end_date=input_data.end_date,
        stores=[],
    )
