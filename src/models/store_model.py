from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, Text

from src.entities import Business, Store
from src.settings.database.sqlalchemy import Base


class StoreModel(Base):
    __tablename__ = 'data_store_cad'

    STORE_CODE: Mapped[int] = mapped_column(Integer, primary_key=True)
    STORE_NAME: Mapped[str] = mapped_column(Text)
    START_DATE: Mapped[str] = mapped_column(Text)
    END_DATE: Mapped[str] = mapped_column(Text)
    BUSINESS_NAME: Mapped[str] = mapped_column(Text)
    BUSINESS_CODE: Mapped[int] = mapped_column(Integer)

    def to_entity(self) -> Store:
        return Store(
            store_id=self.STORE_CODE,
            store_name=self.STORE_NAME,
            store_business=Business(
                business_id=self.BUSINESS_CODE,
                business_name=self.BUSINESS_NAME,
            ),
        )
