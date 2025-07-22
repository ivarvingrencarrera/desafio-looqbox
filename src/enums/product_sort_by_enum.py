from enum import StrEnum


class ProductSortByEnum(StrEnum):
    PRICE = 'price'
    NAME = 'name'


class ProductSortOrderEnum(StrEnum):
    ASC = 'asc'
    DESC = 'desc'
