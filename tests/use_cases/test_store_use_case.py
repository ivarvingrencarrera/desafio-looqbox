from unittest.mock import AsyncMock

import pytest

from src.entities import Store
from src.exceptions import StoreNotFoundError
from src.repositories import StoreRepository
from src.schemas import StoreOutputSchema
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
