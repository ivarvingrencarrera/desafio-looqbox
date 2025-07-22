from unittest.mock import AsyncMock

import pytest

from src.entities import Business
from src.exceptions import BusinessNotFoundError
from src.repositories import BusinessRepository
from src.schemas import (
    BusinessOutputSchema,
    BusinessTotalSalesInputSchema,
    BusinessTotalSalesOutputSchema,
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


async def test_find_businesses_total_sales(
    business: Business, business_use_case: BusinessUseCase, business_repository: BusinessRepository
) -> None:
    business_repository.find_total_sales = AsyncMock(return_value=[business])
    input_data = BusinessTotalSalesInputSchema(start_date='2023-01-01', end_date='2023-12-31')
    output = await business_use_case.find_businesses_total_sales(input_data)
    assert output == [BusinessTotalSalesOutputSchema.from_entity(business)]
