from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Date, Integer, Numeric

from src.settings.database.sqlalchemy import Base


class ProductSaleModel(Base):
    __tablename__ = 'data_product_sales'

    STORE_CODE: Mapped[int] = mapped_column(
        ForeignKey('data_store_cad.STORE_CODE'), primary_key=True
    )
    PRODUCT_CODE: Mapped[int] = mapped_column(
        ForeignKey('data_product_cad.PRODUCT_CODE'), primary_key=True
    )
    DATE: Mapped[date] = mapped_column(Date, primary_key=True, nullable=False)
    SALES_VALUE: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    SALES_QTY: Mapped[int] = mapped_column(Integer)
