from src.exceptions import BusinessNotFoundError
from src.repositories import BusinessRepository
from src.schemas import (
    BusinessesSalesInputSchema,
    BusinessesSalesOutputSchema,
    BusinessOutputSchema,
    BusinessSalesOutputSchema,
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

    async def find_businesses_sales(
        self, input_data: BusinessesSalesInputSchema
    ) -> BusinessesSalesOutputSchema:
        businesses = await self.business_repository.find_all(business_ids=input_data.business_ids)
        if not businesses:
            businesses_sales = []
        else:
            sales = await self.business_repository.find_sales(
                business_ids=[business.id for business in businesses],
                start_date=input_data.start_date,
                end_date=input_data.end_date,
                group_by=input_data.group_by,
            )
            for business in businesses:
                business.sales = sales.get(business.id, [])
            businesses_sales = [
                BusinessSalesOutputSchema.from_entity(
                    business=business,
                    group_by=input_data.group_by,
                )
                for business in businesses
            ]
        return BusinessesSalesOutputSchema(
            calculation=input_data.calculation,
            group_by=input_data.group_by,
            start_date=input_data.start_date,
            end_date=input_data.end_date,
            businesses=businesses_sales,
        )
