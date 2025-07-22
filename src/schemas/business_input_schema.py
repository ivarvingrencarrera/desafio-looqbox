from __future__ import annotations

from pydantic import BaseModel, Field


class BusinessTotalSalesInputSchema(BaseModel):
    start_date: str = Field(examples=['2023-01-01'])
    end_date: str = Field(examples=['2023-12-31'])
