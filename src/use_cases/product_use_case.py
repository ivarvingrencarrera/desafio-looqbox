from src.exceptions import ProductNotFoundError
from src.repositories import ProductRepository
from src.schemas import ProductInputSchema, ProductOutputSchema


class ProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

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
