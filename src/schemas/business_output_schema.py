from __future__ import annotations

from pydantic import BaseModel, Field

from src.entities import Business


class BusinessOutputBaseSchema(BaseModel):
    id: int = Field(examples=[1])
    name: str = Field(examples=['Varejo'])


class BusinessOutputSchema(BusinessOutputBaseSchema):
    @staticmethod
    def from_entity(business: Business) -> BusinessOutputSchema:
        return BusinessOutputSchema(id=business.id, name=business.name)


class BusinessTotalSalesOutputSchema(BusinessOutputBaseSchema):
    total_sales: float = Field(examples=[123456.78])

    @staticmethod
    def from_entity(business: Business) -> BusinessTotalSalesOutputSchema:
        return BusinessTotalSalesOutputSchema(
            id=business.id,
            name=business.name,
            total_sales=business.total_sales,
        )
