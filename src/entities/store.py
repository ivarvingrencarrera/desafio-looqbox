from src.exceptions import ValueNotDefined
from src.value_objects import Sale

from .business import Business


class Store:
    def __init__(
        self,
        id: int,
        name: str,
        business: Business,
        sales: list[Sale] | None = None,
    ) -> None:
        self._id = id
        self._name = name
        self._business = business
        self._sales = sales

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def business_id(self) -> int:
        return self._business.id

    @property
    def business_name(self) -> str:
        return self._business.name

    @property
    def sales(self) -> list[Sale]:
        if self._sales is None:
            raise ValueNotDefined(value='sales', entity='Store')
        return self._sales

    @sales.setter
    def sales(self, sales: list[Sale]) -> None:
        self._sales = sales

    def __repr__(self) -> str:
        return f'Store(id={self.id}, name={self.name})'
