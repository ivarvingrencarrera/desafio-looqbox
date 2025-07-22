from __future__ import annotations

from pydantic import BaseModel, Field

from src.entities import Product

from .department_output_schema import DepartmentOutputBaseSchema
from .section_output_schema import SectionOutputBaseSchema


class ProductOutputBaseSchema(BaseModel):
    id: int = Field(examples=[301409])
    name: str = Field(examples=['Whisky Escoces THE MACALLAN Ruby Garrafa 700ml com Caixa'])
    price: float = Field(examples=[741.99])


class ProductOutputSchema(ProductOutputBaseSchema):
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
