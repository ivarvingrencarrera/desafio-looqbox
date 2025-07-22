from .department import Department
from .section import Section


class Product:
    def __init__(
        self,
        product_id: int,
        product_name: str,
        product_price: float,
        product_department: Department,
        product_section: Section,
    ) -> None:
        self._product_id = product_id
        self._product_name = product_name
        self._product_price = product_price
        self._product_department = product_department
        self._product_section = product_section

    @property
    def id(self) -> int:
        return self._product_id

    @property
    def name(self) -> str:
        return self._product_name

    @property
    def price(self) -> float:
        return self._product_price

    @property
    def department_id(self) -> int:
        return self._product_department.id

    @property
    def department_name(self) -> str:
        return self._product_department.name

    @property
    def section_id(self) -> int:
        return self._product_section.id

    @property
    def section_name(self) -> str:
        return self._product_section.name

    def __repr__(self) -> str:
        return f'Product(id={self.id}, name={self.name}, price={self.price}'
