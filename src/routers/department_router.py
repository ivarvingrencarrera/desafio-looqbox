from typing import Annotated

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette import status

from src.schemas import DepartmentOutputSchema
from src.use_cases import DepartmentUseCase, department_usecase

router = APIRouter(prefix='/departments', tags=['Department'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_departments(
    usecase: Annotated[DepartmentUseCase, Depends(department_usecase)],
) -> list[DepartmentOutputSchema]:
    return await usecase.find_departments()


@router.get('/{department_id}', status_code=status.HTTP_200_OK)
async def get_department(
    department_id: int,
    usecase: Annotated[DepartmentUseCase, Depends(department_usecase)],
) -> DepartmentOutputSchema:
    return await usecase.find_department(department_id)
