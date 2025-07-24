from src.exceptions import ValueNotDefined
from src.value_objects import Sale


class Business:
    def __init__(
        self,
        id: int,
        name: str,
    ) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def sales(self) -> list[Sale]:
        if self._sales is None:
            raise ValueNotDefined(value='sales', entity='Store')
        return self._sales

    @sales.setter
    def sales(self, sales: list[Sale]) -> None:
        self._sales = sales

    def __repr__(self) -> str:
        return f'Business(id={self.id}, name={self.name})'
