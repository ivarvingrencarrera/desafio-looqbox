from typing import Annotated

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette import status

from src.schemas import ProductInputSchema, ProductOutputSchema
from src.use_cases import ProductUseCase, product_usecase

router = APIRouter(prefix='/products', tags=['Product'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_products(
    usecase: Annotated[ProductUseCase, Depends(product_usecase)],
    input_data: ProductInputSchema = Depends(),
) -> list[ProductOutputSchema]:
    return await usecase.find_products(input_data)


@router.get('/{product_id}', status_code=status.HTTP_200_OK)
async def get_product(
    product_id: int,
    usecase: Annotated[ProductUseCase, Depends(product_usecase)],
) -> ProductOutputSchema:
    return await usecase.find_product(product_id)
