from datetime import date
from decimal import Decimal

import pytest

from src.entities import Business, Department, Product, Section, Store
from src.repositories import (
    BusinessRepository,
    DepartmentRepository,
    ProductRepository,
    SectionRepository,
    StoreRepository,
)
from src.use_cases import (
    BusinessUseCase,
    DepartmentUseCase,
    ProductUseCase,
    SectionUseCase,
    StoreUseCase,
)
from src.value_objects import DateTime, Sale


@pytest.fixture
def business_repository() -> BusinessRepository:
    return BusinessRepository  # type: ignore[return-value]


@pytest.fixture
def product_repository() -> ProductRepository:
    return ProductRepository  # type: ignore[return-value]


@pytest.fixture
def store_repository() -> StoreRepository:
    return StoreRepository  # type: ignore[return-value]


@pytest.fixture
def department_repository() -> DepartmentRepository:
    return DepartmentRepository  # type: ignore[return-value]


@pytest.fixture
def section_repository() -> SectionRepository:
    return SectionRepository  # type: ignore[return-value]


@pytest.fixture
def business_use_case(business_repository: BusinessRepository) -> BusinessUseCase:
    return BusinessUseCase(business_repository)


@pytest.fixture
def store_use_case(store_repository: StoreRepository) -> StoreUseCase:
    return StoreUseCase(store_repository)


@pytest.fixture
def department_use_case(department_repository: DepartmentRepository) -> DepartmentUseCase:
    return DepartmentUseCase(department_repository)


@pytest.fixture
def section_use_case(
    section_repository: SectionRepository, department_repository: DepartmentRepository
) -> SectionUseCase:
    return SectionUseCase(section_repository, department_repository)


@pytest.fixture
def product_use_case(
    product_repository: ProductRepository, store_repository: StoreRepository
) -> ProductUseCase:
    return ProductUseCase(product_repository, store_repository)


@pytest.fixture
def sales() -> list[Sale]:
    return [
        Sale(date=DateTime(date(2023, 1, 1)), quantity=10, value=Decimal('5.99')),
        Sale(date=DateTime(date(2023, 1, 2)), quantity=5, value=Decimal('5.99')),
    ]


@pytest.fixture
def business() -> Business:
    return Business(id=1, name='Varejo', total_sales=123456.78)


@pytest.fixture
def store(business: Business, sales: list[Sale]) -> Store:
    return Store(id=1, name='Sao Paulo', business=business, sales=sales)


@pytest.fixture
def department() -> Department:
    return Department(department_id=2, department_name='Bebidas')


@pytest.fixture
def section(department: Department) -> Section:
    return Section(section_id=4, section_name='Bebidas', department=department)


@pytest.fixture
def product(section: Section, department: Department, sales: list[Sale]) -> Product:
    return Product(
        id=10,
        name='Cerveja',
        price=5.99,
        department=department,
        section=section,
        sales=sales,
    )
