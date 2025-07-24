from __future__ import annotations

from pydantic import BaseModel, Field

from src.enums import CalculationType, GroupByPeriodEnum


class BusinessesSalesInputSchema(BaseModel):
    business_ids: list[int] = Field(default=[], examples=[[1, 2, 3]])
    start_date: str = Field(examples=['2019-01-01'])
    end_date: str = Field(examples=['2019-01-31'])
    group_by: GroupByPeriodEnum = Field(
        default=GroupByPeriodEnum.DAILY, examples=[GroupByPeriodEnum.TOTAL]
    )
    calculation: CalculationType = Field(
        default=CalculationType.TOTAL, examples=[CalculationType.TOTAL]
    )
