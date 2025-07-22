from typing import Annotated

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette import status

from src.schemas import (
    BusinessOutputSchema,
    BusinessTotalSalesInputSchema,
    BusinessTotalSalesOutputSchema,
)
from src.use_cases import BusinessUseCase, business_usecase

router = APIRouter(prefix='/businesses', tags=['Business'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_businesses(
    usecase: Annotated[BusinessUseCase, Depends(business_usecase)],
) -> list[BusinessOutputSchema]:
    return await usecase.find_businesses()


@router.get('/{business_id}', status_code=status.HTTP_200_OK)
async def get_business(
    business_id: int,
    usecase: Annotated[BusinessUseCase, Depends(business_usecase)],
) -> BusinessOutputSchema:
    return await usecase.find_business(business_id)


@router.get('/total-sales', status_code=status.HTTP_200_OK)
async def get_businesses_total_sales(
    usecase: Annotated[BusinessUseCase, Depends(business_usecase)],
    input_data: BusinessTotalSalesInputSchema = Depends(),
) -> list[BusinessTotalSalesOutputSchema]:
    return await usecase.find_businesses_total_sales(input_data)
