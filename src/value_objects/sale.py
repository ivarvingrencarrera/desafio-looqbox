from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class Sale:
    value: Decimal
    quantity: int
    date: date
