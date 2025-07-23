from src.exceptions import ValueNotDefined
from src.value_objects import Sale

from .department import Department
from .section import Section


class Product:
    def __init__(
        self,
        id: int,
        name: str,
        price: float,
        department: Department,
        section: Section,
        sales: list[Sale] | None = None,
    ) -> None:
        self._id = id
        self._name = name
        self._price = price
        self._department = department
        self._section = section
        self._sales = sales

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def department_id(self) -> int:
        return self._department.id

    @property
    def department_name(self) -> str:
        return self._department.name

    @property
    def section_id(self) -> int:
        return self._section.id

    @property
    def section_name(self) -> str:
        return self._section.name

    @property
    def sales(self) -> list[Sale]:
        if self._sales is None:
            raise ValueNotDefined(value='sales', entity='Product')
        return self._sales

    @sales.setter
    def sales(self, sales: list[Sale]) -> None:
        self._sales = sales

    def __repr__(self) -> str:
        return f'Product(id={self.id}, name={self.name}, price={self.price}'
