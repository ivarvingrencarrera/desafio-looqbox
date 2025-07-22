from src.exceptions import StoreNotFoundError
from src.repositories import StoreRepository
from src.schemas import StoreOutputSchema


class StoreUseCase:
    def __init__(self, store_repository: StoreRepository) -> None:
        self.store_repository = store_repository

    async def find_store(self, store_id: int) -> StoreOutputSchema:
        store = await self.store_repository.find(store_id=store_id)
        if not store:
            raise StoreNotFoundError
        return StoreOutputSchema.from_entity(store)

    async def find_stores(self) -> list[StoreOutputSchema]:
        stores = await self.store_repository.find_all()
        return [StoreOutputSchema.from_entity(store) for store in stores]
