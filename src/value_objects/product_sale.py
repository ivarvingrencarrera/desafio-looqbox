from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductSale:
    value: Decimal
    quantity: int
    date: date
