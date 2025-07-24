from __future__ import annotations

from datetime import date
from typing import cast

from pydantic import BaseModel, Field

from src.entities import Store
from src.enums import CalculationType, GroupByPeriodEnum
from src.value_objects import DateTime

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


class StoreSalesOutputSchema(StoreOutputBaseSchema):
    sales: dict | list[dict] = Field()

    @staticmethod
    def from_entity(
        store: Store, calculation: CalculationType, group_by: GroupByPeriodEnum
    ) -> StoreSalesOutputSchema:
        if calculation == CalculationType.AVERAGE:
            if group_by == GroupByPeriodEnum.DAILY:
                sales = [
                    {'day': cast(DateTime, sale.date).to_day(), 'value': sale.average}
                    for sale in store.sales
                ]
            elif group_by == GroupByPeriodEnum.WEEKLY:
                sales = [
                    {'week': cast(DateTime, sale.date).to_week(), 'value': sale.average}
                    for sale in store.sales
                ]
            elif group_by == GroupByPeriodEnum.MONTHLY:
                sales = [
                    {'month': cast(DateTime, sale.date).to_month(), 'value': sale.average}
                    for sale in store.sales
                ]
            elif group_by == GroupByPeriodEnum.YEARLY:
                sales = [
                    {'year': cast(DateTime, sale.date).to_year(), 'value': sale.average}
                    for sale in store.sales
                ]
            elif group_by == GroupByPeriodEnum.TOTAL:
                sales = [{'value': sale.average} for sale in store.sales]
        else:
            sales = [
                {
                    'value': sale.value,
                    'quantity': sale.quantity,
                    'date': cast(date, sale.date).isoformat(),
                }
                for sale in store.sales
            ]
        return StoreSalesOutputSchema(
            id=store.id,
            name=store.name,
            sales=sales,
        )


class StoresSalesOutputSchema(BaseModel):
    calculation: CalculationType = Field(examples=[CalculationType.AVERAGE])
    group_by: GroupByPeriodEnum = Field(examples=[GroupByPeriodEnum.DAILY])
    start_date: str = Field(examples=['2024-01-01'])
    end_date: str = Field(examples=['2024-01-31'])
    stores: list[StoreSalesOutputSchema]
