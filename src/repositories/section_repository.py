from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.entities import Department, Section
from src.models import ProductModel


class SectionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, section_id: int) -> Section | None:
        query = (
            select(ProductModel.SECTION_COD, ProductModel.SECTION_NAME)
            .distinct()
            .where(section_id == ProductModel.SECTION_COD)  # type: ignore[arg-type]
            .order_by(ProductModel.SECTION_COD)
        )
        try:
            result = await self.session.execute(query)
            section = result.one()
            return Section(section_id=section[0], section_name=section[1])
        except NoResultFound:
            return None

    async def find_all(self, department_ids: list[int] | None = None) -> list[Section]:
        query = (
            select(
                ProductModel.SECTION_COD,
                ProductModel.SECTION_NAME,
                ProductModel.DEP_COD,
                ProductModel.DEP_NAME,
            )
            .distinct()
            .order_by(ProductModel.SECTION_COD)
        )
        if department_ids:
            query = query.where(ProductModel.DEP_COD.in_(department_ids))
        result = await self.session.execute(query)
        sections = result.all()
        return [
            Section(
                section_id=cod,
                section_name=name,
                department=Department(department_id=dep_cod, department_name=dep_name),
            )
            for cod, name, dep_cod, dep_name in sections
        ]
