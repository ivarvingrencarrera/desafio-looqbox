from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field

from src.entities import Product

from .department_output_schema import DepartmentOutputBaseSchema
from .section_output_schema import SectionOutputBaseSchema


class ProductOutputBaseSchema(BaseModel):
    id: int = Field(examples=[301409])
    name: str = Field(examples=['Whisky Escoces THE MACALLAN Ruby Garrafa 700ml com Caixa'])


class ProductOutputSchema(ProductOutputBaseSchema):
    price: float = Field(examples=[741.99])
    department: DepartmentOutputBaseSchema
    section: SectionOutputBaseSchema

    @staticmethod
    def from_entity(product: Product) -> ProductOutputSchema:
        return ProductOutputSchema(
            id=product.id,
            name=product.name,
            price=product.price,
            department=DepartmentOutputBaseSchema(
                id=product.department_id,
                name=product.department_name,
            ),
            section=SectionOutputBaseSchema(
                id=product.section_id,
                name=product.section_name,
            ),
        )


class SalesOutputSchema(BaseModel):
    sales_value: Decimal = Field(examples=[74199.00])
    sales_quantity: int = Field(examples=[100])
    date: str = Field(examples=['2024-01-01'])


class ProductSalesOutputSchema(ProductOutputBaseSchema):
    sales: list[SalesOutputSchema]

    @staticmethod
    def from_entity(product: Product) -> ProductSalesOutputSchema:
        return ProductSalesOutputSchema(
            id=product.id,
            name=product.name,
            sales=[
                SalesOutputSchema(
                    sales_value=sale.value,
                    sales_quantity=sale.quantity,
                    date=sale.date.isoformat(),
                )
                for sale in product.sales
            ],
        )
