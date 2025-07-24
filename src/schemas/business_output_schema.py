from __future__ import annotations

from typing import cast

from pydantic import BaseModel, Field

from src.entities import Business
from src.enums import CalculationType, GroupByPeriodEnum
from src.value_objects import DateTime


class BusinessOutputBaseSchema(BaseModel):
    id: int = Field(examples=[1])
    name: str = Field(examples=['Varejo'])


class BusinessOutputSchema(BusinessOutputBaseSchema):
    @staticmethod
    def from_entity(business: Business) -> BusinessOutputSchema:
        return BusinessOutputSchema(id=business.id, name=business.name)


class BusinessSalesOutputSchema(BusinessOutputBaseSchema):
    sales: dict | list[dict] = Field()

    @staticmethod
    def from_entity(business: Business, group_by: GroupByPeriodEnum) -> BusinessSalesOutputSchema:
        if group_by == GroupByPeriodEnum.DAILY:
            sales = [
                {'day': cast(DateTime, sale.date).to_day(), 'value': sale.average}
                for sale in business.sales
            ]
        elif group_by == GroupByPeriodEnum.WEEKLY:
            sales = [
                {'week': cast(DateTime, sale.date).to_week(), 'value': sale.average}
                for sale in business.sales
            ]
        elif group_by == GroupByPeriodEnum.MONTHLY:
            sales = [
                {'month': cast(DateTime, sale.date).to_month(), 'value': sale.average}
                for sale in business.sales
            ]
        elif group_by == GroupByPeriodEnum.YEARLY:
            sales = [
                {'year': cast(DateTime, sale.date).to_year(), 'value': sale.average}
                for sale in business.sales
            ]
        elif group_by == GroupByPeriodEnum.TOTAL:
            sales = [{'value': sale.average} for sale in business.sales]
        return BusinessSalesOutputSchema(
            id=business.id,
            name=business.name,
            sales=sales,
        )


class BusinessesSalesOutputSchema(BaseModel):
    calculation: CalculationType = Field(examples=[CalculationType.TOTAL])
    group_by: GroupByPeriodEnum = Field(examples=[GroupByPeriodEnum.DAILY])
    start_date: str = Field(examples=['2024-01-01'])
    end_date: str = Field(examples=['2024-01-31'])
    businesses: list[BusinessSalesOutputSchema]
