from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, Numeric, String

from src.entities import Department, Product, Section
from src.settings.database.sqlalchemy import Base


class ProductModel(Base):
    __tablename__ = 'data_product'

    PRODUCT_COD: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    PRODUCT_NAME: Mapped[str] = mapped_column(String(150))
    PRODUCT_VAL: Mapped[float] = mapped_column(Numeric(8, 2))
    DEP_NAME: Mapped[str] = mapped_column(String(255))
    DEP_COD: Mapped[int] = mapped_column(Integer)
    SECTION_NAME: Mapped[str] = mapped_column(String(255))
    SECTION_COD: Mapped[int] = mapped_column(Integer)

    def to_entity(self) -> Product:
        return Product(
            product_id=self.PRODUCT_COD,
            product_name=self.PRODUCT_NAME,
            product_price=self.PRODUCT_VAL,
            product_department=Department(
                department_id=self.DEP_COD, department_name=self.DEP_NAME
            ),
            product_section=Section(section_id=self.SECTION_COD, section_name=self.SECTION_NAME),
        )
