from src.exceptions import ValueNotDefined


class Business:
    def __init__(
        self, business_id: int, business_name: str, business_total_sales: float | None = None
    ) -> None:
        self._business_id = business_id
        self._business_name = business_name
        self._business_total_sales = business_total_sales

    @property
    def id(self) -> int:
        return self._business_id

    @property
    def name(self) -> str:
        return self._business_name

    @property
    def total_sales(self) -> float:
        if self._business_total_sales is None:
            raise ValueNotDefined(value='total_sales', entity='business')
        return self._business_total_sales

    def __repr__(self) -> str:
        return f'Business(id={self.id}, name={self.name})'
