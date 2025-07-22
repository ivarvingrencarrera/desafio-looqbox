from unittest.mock import AsyncMock

import pytest

from src.entities import Department, Section
from src.exceptions import SectionNotFoundError
from src.repositories import DepartmentRepository, SectionRepository
from src.schemas import SectionDepartmentOutputSchema, SectionOutputSchema
from src.use_cases import SectionUseCase


async def test_find_section(
    section: Section,
    section_use_case: SectionUseCase,
    section_repository: SectionRepository,
) -> None:
    section_repository.find = AsyncMock(return_value=section)
    output = await section_use_case.find_section(section_id=section.id)
    assert output == SectionOutputSchema.from_entity(section)


async def test_find_section_not_found(
    section_use_case: SectionUseCase, section_repository: SectionRepository
) -> None:
    section_repository.find = AsyncMock(return_value=None)
    with pytest.raises(SectionNotFoundError) as error:
        await section_use_case.find_section(section_id=999)
    assert str(error.value) == SectionNotFoundError.message


async def test_find_sections(
    section: Section,
    section_use_case: SectionUseCase,
    section_repository: SectionRepository,
) -> None:
    section_repository.find_all = AsyncMock(return_value=[section])
    output = await section_use_case.find_sections()
    assert output == [SectionOutputSchema.from_entity(section)]


async def test_find_section_by_department(
    section: Section,
    section_use_case: SectionUseCase,
    section_repository: SectionRepository,
    department: Department,
    department_repository: DepartmentRepository,
) -> None:
    section_repository.find_all = AsyncMock(return_value=[section])
    department_repository.find_all = AsyncMock(return_value=[department])
    output = await section_use_case.find_section_by_department(department_names=[department.name])
    assert output == [SectionDepartmentOutputSchema.from_entity(section)]


async def test_find_section_by_department_not_found(
    section_use_case: SectionUseCase,
    section_repository: SectionRepository,
    department_repository: DepartmentRepository,
) -> None:
    section_repository.find_all = AsyncMock(return_value=[])
    department_repository.find_all = AsyncMock(return_value=[])
    output = await section_use_case.find_section_by_department(department_names=['NonExistent'])
    assert output == []
