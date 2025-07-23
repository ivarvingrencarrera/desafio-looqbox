from src.exceptions import ProductNotFoundError, StoreNotFoundError
from src.repositories import ProductRepository, StoreRepository
from src.schemas import (
    ProductInputSchema,
    ProductOutputSchema,
    ProductSalesByStoreInputSchema,
    ProductSalesOutputSchema,
)


class ProductUseCase:
    def __init__(
        self, product_repository: ProductRepository, store_repository: StoreRepository
    ) -> None:
        self.product_repository = product_repository
        self.store_repository = store_repository

    async def find_product(self, product_id: int) -> ProductOutputSchema:
        product = await self.product_repository.find(product_id=product_id)
        if not product:
            raise ProductNotFoundError
        return ProductOutputSchema.from_entity(product)

    async def find_products(self, input_data: ProductInputSchema) -> list[ProductOutputSchema]:
        products = await self.product_repository.find_all(
            sort_by=input_data.sort_by, sort_order=input_data.sort_order, limit=input_data.limit
        )
        return [ProductOutputSchema.from_entity(product) for product in products]

    async def find_product_sales(
        self, product_id: int, input_data: ProductSalesByStoreInputSchema
    ) -> ProductSalesOutputSchema:
        product = await self.product_repository.find(product_id=product_id)
        if not product:
            raise ProductNotFoundError
        if input_data.store_id is not None:
            store = await self.store_repository.find(store_id=input_data.store_id)
            if not store:
                raise StoreNotFoundError
        product.sales = await self.product_repository.find_product_sales(
            product_id=product_id,
            start_date=input_data.start_date,
            end_date=input_data.end_date,
            store_id=input_data.store_id,
        )
        return ProductSalesOutputSchema.from_entity(product)
