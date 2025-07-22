from typing import Annotated

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette import status

from src.schemas import StoreOutputSchema
from src.use_cases import StoreUseCase, store_usecase

router = APIRouter(prefix='/stores', tags=['Store'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_stores(
    usecase: Annotated[StoreUseCase, Depends(store_usecase)],
) -> list[StoreOutputSchema]:
    return await usecase.find_stores()


@router.get('/{store_id}', status_code=status.HTTP_200_OK)
async def get_store(
    store_id: int,
    usecase: Annotated[StoreUseCase, Depends(store_usecase)],
) -> StoreOutputSchema:
    return await usecase.find_store(store_id)
