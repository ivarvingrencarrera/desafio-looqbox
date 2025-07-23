from src.exceptions import StoreNotFoundError
from src.repositories import StoreRepository
from src.schemas import StoreOutputSchema, StoreSalesInputSchema, StoreSalesOutputSchema


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

    async def find_store_sales(
        self, store_id: int, input_data: StoreSalesInputSchema
    ) -> StoreSalesOutputSchema:
        store = await self.store_repository.find(store_id=store_id)
        if not store:
            raise StoreNotFoundError
        store.sales = await self.store_repository.find_store_sales(
            store_id=store_id, start_date=input_data.start_date, end_date=input_data.end_date
        )
        return StoreSalesOutputSchema.from_entity(store)
