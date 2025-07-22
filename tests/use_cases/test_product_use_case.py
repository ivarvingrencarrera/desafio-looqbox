from unittest.mock import AsyncMock

import pytest

from src.entities import Product
from src.enums import ProductSortByEnum, ProductSortOrderEnum
from src.exceptions import ProductNotFoundError
from src.repositories import ProductRepository
from src.schemas import ProductInputSchema, ProductOutputSchema
from src.use_cases import ProductUseCase


async def test_find_product(
    product: Product,
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
) -> None:
    product_repository.find = AsyncMock(return_value=product)
    output = await product_use_case.find_product(product_id=product.id)
    assert output == ProductOutputSchema.from_entity(product)


async def test_find_product_not_found(
    product_use_case: ProductUseCase, product_repository: ProductRepository
) -> None:
    product_repository.find = AsyncMock(return_value=None)
    with pytest.raises(ProductNotFoundError) as error:
        await product_use_case.find_product(product_id=999)
    assert str(error.value) == ProductNotFoundError.message


async def test_find_products(
    product: Product,
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
) -> None:
    product_repository.find_all = AsyncMock(return_value=[product])
    input_data = ProductInputSchema(
        sort_by=ProductSortByEnum.PRICE, sort_order=ProductSortOrderEnum.DESC, limit=10
    )
    output = await product_use_case.find_products(input_data=input_data)
    assert output == [ProductOutputSchema.from_entity(product)]
