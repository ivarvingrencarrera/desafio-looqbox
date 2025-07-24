from dataclasses import dataclass, field
from decimal import Decimal

from .date_time import DateTime


@dataclass(frozen=True, slots=True, kw_only=True)
class Sale:
    value: Decimal
    quantity: int
    date: DateTime | None = field(default=None)

    @property
    def average(self) -> Decimal:
        if self.quantity == 0:
            return Decimal('0.00')
        return self.value / self.quantity
