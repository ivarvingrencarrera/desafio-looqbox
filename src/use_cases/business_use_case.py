from src.exceptions import BusinessNotFoundError
from src.repositories import BusinessRepository
from src.schemas import (
    BusinessOutputSchema,
    BusinessTotalSalesInputSchema,
    BusinessTotalSalesOutputSchema,
)


class BusinessUseCase:
    def __init__(self, business_repository: BusinessRepository) -> None:
        self.business_repository = business_repository

    async def find_business(self, business_id: int) -> BusinessOutputSchema:
        business = await self.business_repository.find(business_id=business_id)
        if not business:
            raise BusinessNotFoundError
        return BusinessOutputSchema.from_entity(business)

    async def find_businesses(self) -> list[BusinessOutputSchema]:
        businesses = await self.business_repository.find_all()
        return [BusinessOutputSchema.from_entity(business) for business in businesses]

    async def find_businesses_total_sales(
        self, input_data: BusinessTotalSalesInputSchema
    ) -> list[BusinessTotalSalesOutputSchema]:
        businesses = await self.business_repository.find_total_sales(
            start_date=input_data.start_date, end_date=input_data.end_date
        )
        return [BusinessTotalSalesOutputSchema.from_entity(business) for business in businesses]
