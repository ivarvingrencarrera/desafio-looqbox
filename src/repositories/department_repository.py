from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.entities import Department
from src.models import ProductModel


class DepartmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, department_id: int) -> Department | None:
        query = (
            select(ProductModel.DEP_COD, ProductModel.DEP_NAME)
            .distinct()
            .where(department_id == ProductModel.DEP_COD)  # type: ignore[arg-type]
            .order_by(ProductModel.DEP_COD)
        )
        try:
            result = await self.session.execute(query)
            department = result.one()
            return Department(department_id=department[0], department_name=department[1])
        except NoResultFound:
            return None

    async def find_all(self, department_names: list[str] | None = None) -> list[Department]:
        query = (
            select(ProductModel.DEP_COD, ProductModel.DEP_NAME)
            .distinct()
            .order_by(ProductModel.DEP_COD)
        )
        if department_names:
            query = query.where(ProductModel.DEP_NAME.in_(department_names))
        result = await self.session.execute(query)
        departments = result.all()
        return [Department(department_id=cod, department_name=name) for cod, name in departments]
