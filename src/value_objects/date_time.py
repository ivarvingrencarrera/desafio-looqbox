from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime


@dataclass
class DateTime:
    value: datetime | date

    def __post_init__(self) -> None:
        if isinstance(self.value, date):
            self.value = datetime.combine(self.value, datetime.min.time(), tzinfo=UTC)
        elif isinstance(self.value, str):
            self.value = datetime.fromisoformat(self.value)

    @staticmethod
    def now() -> DateTime:
        return DateTime(datetime.now(tz=UTC))

    def to_year(self) -> str:
        return self.value.strftime('%Y')

    def to_month(self) -> str:
        return self.value.strftime('%Y-%m')

    def to_week(self) -> str:
        iso_year, iso_week, _ = self.value.isocalendar()
        return f'{iso_year}-W{iso_week:02}'

    def to_day(self) -> str:
        return self.value.strftime('%Y-%m-%d')
