from src.exceptions import DepartmentNotFoundError
from src.repositories import DepartmentRepository
from src.schemas import DepartmentOutputSchema


class DepartmentUseCase:
    def __init__(self, department_repository: DepartmentRepository) -> None:
        self.department_repository = department_repository

    async def find_department(self, department_id: int) -> DepartmentOutputSchema:
        department = await self.department_repository.find(department_id=department_id)
        if not department:
            raise DepartmentNotFoundError
        return DepartmentOutputSchema.from_entity(department)

    async def find_departments(self) -> list[DepartmentOutputSchema]:
        departments = await self.department_repository.find_all()
        return [DepartmentOutputSchema.from_entity(department) for department in departments]
