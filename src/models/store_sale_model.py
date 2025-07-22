from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Date, Integer, Numeric

from src.settings.database.sqlalchemy import Base

from .store_model import StoreModel


class StoreSaleModel(Base):
    __tablename__ = 'data_store_sales'

    STORE_CODE: Mapped[int] = mapped_column(
        ForeignKey('data_store_cad.STORE_CODE'), primary_key=True
    )
    DATE: Mapped[date] = mapped_column(Date)
    SALES_VALUE: Mapped[Numeric] = mapped_column(Numeric(255, 2))
    SALES_QTY: Mapped[int] = mapped_column(Integer)

    store: Mapped[StoreModel] = mapped_column(ForeignKey('data_store_cad.STORE_CODE'))
