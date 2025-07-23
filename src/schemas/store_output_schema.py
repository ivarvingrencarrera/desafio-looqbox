from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field

from src.entities import Store

from .business_output_schema import BusinessOutputBaseSchema


class StoreOutputBaseSchema(BaseModel):
    id: int = Field(examples=[1])
    name: str = Field(examples=['Sao Paulo'])


class StoreOutputSchema(StoreOutputBaseSchema):
    business: BusinessOutputBaseSchema

    @staticmethod
    def from_entity(store: Store) -> StoreOutputSchema:
        return StoreOutputSchema(
            id=store.id,
            name=store.name,
            business=BusinessOutputBaseSchema(id=store.business_id, name=store.business_name),
        )


class SalesOutputSchema(BaseModel):
    date: str = Field(examples=['2024-01-01'])
    value: Decimal = Field(examples=[74199.00])
    quantity: int = Field(examples=[100])


class StoreSalesOutputSchema(StoreOutputBaseSchema):
    sales: list[SalesOutputSchema]

    @staticmethod
    def from_entity(store: Store) -> StoreSalesOutputSchema:
        return StoreSalesOutputSchema(
            id=store.id,
            name=store.name,
            sales=[
                SalesOutputSchema(
                    value=sale.value,
                    quantity=sale.quantity,
                    date=sale.date.isoformat(),
                )
                for sale in store.sales
            ],
        )
