from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import (
    BusinessRepository,
    DepartmentRepository,
    ProductRepository,
    SectionRepository,
    StoreRepository,
)
from src.settings.database.sqlalchemy import get_session

from .business_use_case import BusinessUseCase
from .department_use_case import DepartmentUseCase
from .product_use_case import ProductUseCase
from .section_use_case import SectionUseCase
from .store_use_case import StoreUseCase


def product_usecase(session: AsyncSession = Depends(get_session)) -> ProductUseCase:
    product_repository = ProductRepository(session)
    return ProductUseCase(product_repository)


def section_usecase(session: AsyncSession = Depends(get_session)) -> SectionUseCase:
    section_repository = SectionRepository(session)
    department_repository = DepartmentRepository(session)
    return SectionUseCase(section_repository, department_repository)


def department_usecase(session: AsyncSession = Depends(get_session)) -> DepartmentUseCase:
    department_repository = DepartmentRepository(session)
    return DepartmentUseCase(department_repository)


def store_usecase(session: AsyncSession = Depends(get_session)) -> StoreUseCase:
    store_repository = StoreRepository(session)
    return StoreUseCase(store_repository)


def business_usecase(session: AsyncSession = Depends(get_session)) -> BusinessUseCase:
    business_repository = BusinessRepository(session)
    return BusinessUseCase(business_repository)
