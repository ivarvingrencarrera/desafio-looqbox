from __future__ import annotations

from pydantic import BaseModel, Field

from src.enums import ProductSortByEnum, ProductSortOrderEnum


class ProductInputSchema(BaseModel):
    sort_by: ProductSortByEnum = Field(default=ProductSortByEnum.NAME)
    sort_order: ProductSortOrderEnum = Field(default=ProductSortOrderEnum.ASC)
    limit: int = Field(default=10, gt=0, le=100)


class ProductSalesInputSchema(BaseModel):
    start_date: str = Field(examples=['2023-01-01'])
    end_date: str = Field(examples=['2023-12-31'])
    store_id: int | None = Field(default=None, examples=[1])
