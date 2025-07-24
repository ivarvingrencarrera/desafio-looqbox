from src.exceptions import StoreNotFoundError
from src.repositories import StoreRepository
from src.schemas import (
    StoreOutputSchema,
    StoreSalesOutputSchema,
    StoresSalesInputSchema,
    StoresSalesOutputSchema,
)


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

    async def find_stores_sales(
        self, input_data: StoresSalesInputSchema
    ) -> StoresSalesOutputSchema:
        stores = await self.store_repository.find_all(store_ids=input_data.store_ids)
        if not stores:
            stores_sales = []
        else:
            sales = await self.store_repository.find_sales(
                store_ids=[store.id for store in stores],
                start_date=input_data.start_date,
                end_date=input_data.end_date,
                group_by=input_data.group_by,
            )
            for store in stores:
                store.sales = sales.get(store.id, [])
            stores_sales = [
                StoreSalesOutputSchema.from_entity(
                    store=store, calculation=input_data.calculation, group_by=input_data.group_by
                )
            ]
        return StoresSalesOutputSchema(
            calculation=input_data.calculation,
            group_by=input_data.group_by,
            start_date=input_data.start_date,
            end_date=input_data.end_date,
            stores=stores_sales,
        )
