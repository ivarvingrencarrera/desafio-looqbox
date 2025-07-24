from unittest.mock import AsyncMock

import pytest

from src.entities import Business
from src.enums import CalculationType, GroupByPeriodEnum
from src.exceptions import BusinessNotFoundError
from src.repositories import BusinessRepository
from src.schemas import (
    BusinessesSalesInputSchema,
    BusinessesSalesOutputSchema,
    BusinessOutputSchema,
    BusinessSalesOutputSchema,
)
from src.use_cases import BusinessUseCase


async def test_find_business(
    business: Business, business_use_case: BusinessUseCase, business_repository: BusinessRepository
) -> None:
    business_repository.find = AsyncMock(return_value=business)
    output = await business_use_case.find_business(business_id=business.id)
    assert output == BusinessOutputSchema.from_entity(business)


async def test_find_business_not_found(
    business_use_case: BusinessUseCase, business_repository: BusinessRepository
) -> None:
    business_repository.find = AsyncMock(return_value=None)
    with pytest.raises(BusinessNotFoundError) as error:
        await business_use_case.find_business(business_id=999)
    assert str(error.value) == BusinessNotFoundError.message


async def test_find_businesses(
    business: Business, business_use_case: BusinessUseCase, business_repository: BusinessRepository
) -> None:
    business_repository.find_all = AsyncMock(return_value=[business])
    output = await business_use_case.find_businesses()
    assert output == [BusinessOutputSchema.from_entity(business)]


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
async def test_find_businesses_sales_total(
    business: Business,
    business_use_case: BusinessUseCase,
    business_repository: BusinessRepository,
    group_by: GroupByPeriodEnum,
) -> None:
    business_repository.find_all = AsyncMock(return_value=[business])
    sales = {business.id: business.sales}
    business_repository.find_sales = AsyncMock(return_value=sales)
    calculation = CalculationType.TOTAL
    input_data = BusinessesSalesInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        calculation=calculation,
        group_by=group_by,
    )
    output = await business_use_case.find_businesses_sales(input_data=input_data)
    assert output == BusinessesSalesOutputSchema(
        calculation=calculation,
        group_by=input_data.group_by,
        start_date=input_data.start_date,
        end_date=input_data.end_date,
        businesses=[BusinessSalesOutputSchema.from_entity(business, group_by)],
    )


async def test_find_businesses_sales_no_businesses(
    business_use_case: BusinessUseCase,
    business_repository: BusinessRepository,
) -> None:
    business_repository.find_all = AsyncMock(return_value=[])
    input_data = BusinessesSalesInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        calculation=CalculationType.TOTAL,
    )
    output = await business_use_case.find_businesses_sales(input_data=input_data)
    assert output == BusinessesSalesOutputSchema(
        calculation=input_data.calculation,
        group_by=input_data.group_by,
        start_date=input_data.start_date,
        end_date=input_data.end_date,
        businesses=[],
    )
