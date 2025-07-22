from src.exceptions import SectionNotFoundError
from src.repositories import DepartmentRepository, SectionRepository
from src.schemas import SectionDepartmentOutputSchema, SectionOutputSchema


class SectionUseCase:
    def __init__(
        self, section_repository: SectionRepository, department_repository: DepartmentRepository
    ) -> None:
        self.section_repository = section_repository
        self.department_repository = department_repository

    async def find_section(self, section_id: int) -> SectionOutputSchema:
        section = await self.section_repository.find(section_id=section_id)
        if not section:
            raise SectionNotFoundError
        return SectionOutputSchema.from_entity(section)

    async def find_sections(self) -> list[SectionOutputSchema]:
        sections = await self.section_repository.find_all()
        return [SectionOutputSchema.from_entity(section) for section in sections]

    async def find_section_by_department(
        self, department_names: list[str]
    ) -> list[SectionDepartmentOutputSchema]:
        departments = await self.department_repository.find_all(department_names=department_names)
        if not departments:
            return []
        sections = await self.section_repository.find_all(
            department_ids=[department.id for department in departments]
        )
        return [SectionDepartmentOutputSchema.from_entity(section) for section in sections]
