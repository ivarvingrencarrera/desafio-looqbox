from typing import Annotated

from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter
from starlette import status

from src.schemas import SectionDepartmentOutputSchema, SectionOutputSchema
from src.use_cases import SectionUseCase, section_usecase

router = APIRouter(prefix='/sections', tags=['Section'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_sections(
    usecase: Annotated[SectionUseCase, Depends(section_usecase)],
) -> list[SectionOutputSchema]:
    return await usecase.find_sections()


@router.get('/{section_id}', status_code=status.HTTP_200_OK)
async def get_section(
    section_id: int,
    usecase: Annotated[SectionUseCase, Depends(section_usecase)],
) -> SectionOutputSchema:
    return await usecase.find_section(section_id)


@router.get('/departments', status_code=status.HTTP_200_OK)
async def get_sections_by_departments(
    usecase: Annotated[SectionUseCase, Depends(section_usecase)],
    department_names: list[str] = Query(..., alias='department_names'),
) -> list[SectionDepartmentOutputSchema]:
    return await usecase.find_section_by_department(department_names)
