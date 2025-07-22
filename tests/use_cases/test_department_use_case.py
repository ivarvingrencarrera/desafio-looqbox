from unittest.mock import AsyncMock

import pytest

from src.entities import Department
from src.exceptions import DepartmentNotFoundError
from src.repositories import DepartmentRepository
from src.schemas import DepartmentOutputSchema
from src.use_cases import DepartmentUseCase


async def test_find_department(
    department: Department,
    department_use_case: DepartmentUseCase,
    department_repository: DepartmentRepository,
) -> None:
    department_repository.find = AsyncMock(return_value=department)
    output = await department_use_case.find_department(department_id=department.id)
    assert output == DepartmentOutputSchema.from_entity(department)


async def test_find_department_not_found(
    department_use_case: DepartmentUseCase, department_repository: DepartmentRepository
) -> None:
    department_repository.find = AsyncMock(return_value=None)
    with pytest.raises(DepartmentNotFoundError) as error:
        await department_use_case.find_department(department_id=999)
    assert str(error.value) == DepartmentNotFoundError.message


async def test_find_departments(
    department: Department,
    department_use_case: DepartmentUseCase,
    department_repository: DepartmentRepository,
) -> None:
    department_repository.find_all = AsyncMock(return_value=[department])
    output = await department_use_case.find_departments()
    assert output == [DepartmentOutputSchema.from_entity(department)]
