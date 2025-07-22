from __future__ import annotations

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
