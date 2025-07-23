from unittest.mock import AsyncMock

import pytest

from src.entities import Product, Store
from src.enums import ProductSortByEnum, ProductSortOrderEnum
from src.exceptions import ProductNotFoundError, StoreNotFoundError
from src.repositories import ProductRepository, StoreRepository
from src.schemas import (
    ProductInputSchema,
    ProductOutputSchema,
    ProductSalesByStoreInputSchema,
    ProductSalesOutputSchema,
)
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


async def test_find_products_sales(
    product: Product,
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
) -> None:
    product_repository.find = AsyncMock(return_value=product)
    product_repository.find_product_sales = AsyncMock(return_value=product.sales)
    input_data = ProductSalesByStoreInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
    )
    output = await product_use_case.find_product_sales(product_id=product.id, input_data=input_data)
    assert output == ProductSalesOutputSchema.from_entity(product)


async def test_find_product_sales_with_store(
    product: Product,
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
    store: Store,
    store_repository: StoreRepository,
) -> None:
    product_repository.find = AsyncMock(return_value=product)
    product_repository.find_product_sales = AsyncMock(return_value=product.sales)
    store_repository.find = AsyncMock(return_value=store)
    input_data = ProductSalesByStoreInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        store_id=store.id,
    )
    output = await product_use_case.find_product_sales(product_id=product.id, input_data=input_data)
    assert output == ProductSalesOutputSchema.from_entity(product)


async def test_find_product_sales_store_not_found(
    product: Product,
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
    store_repository: StoreRepository,
) -> None:
    product_repository.find = AsyncMock(return_value=product)
    store_repository.find = AsyncMock(return_value=None)
    input_data = ProductSalesByStoreInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
        store_id=999,
    )
    with pytest.raises(StoreNotFoundError) as error:
        await product_use_case.find_product_sales(product_id=product.id, input_data=input_data)
    assert str(error.value) == StoreNotFoundError.message


async def test_find_product_sales_product_not_found(
    product_use_case: ProductUseCase,
    product_repository: ProductRepository,
) -> None:
    product_repository.find = AsyncMock(return_value=None)
    input_data = ProductSalesByStoreInputSchema(
        start_date='2023-01-01',
        end_date='2023-01-31',
    )
    with pytest.raises(ProductNotFoundError) as error:
        await product_use_case.find_product_sales(product_id=999, input_data=input_data)
    assert str(error.value) == ProductNotFoundError.message
