from src.exceptions import ValueNotDefined


class Business:
    def __init__(self, id: int, name: str, total_sales: float | None = None) -> None:
        self._id = id
        self._name = name
        self._total_sales = total_sales

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def total_sales(self) -> float:
        if self._total_sales is None:
            raise ValueNotDefined(value='total_sales', entity='business')
        return self._total_sales

    def __repr__(self) -> str:
        return f'Business(id={self.id}, name={self.name})'
