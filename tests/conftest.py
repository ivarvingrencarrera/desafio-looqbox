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
def product_use_case(product_repository: ProductRepository) -> ProductUseCase:
    return ProductUseCase(product_repository)


@pytest.fixture
def business() -> Business:
    return Business(business_id=1, business_name='Varejo', business_total_sales=123456.78)


@pytest.fixture
def store(business: Business) -> Store:
    return Store(store_id=1, store_name='Sao Paulo', store_business=business)


@pytest.fixture
def department() -> Department:
    return Department(department_id=2, department_name='Bebidas')


@pytest.fixture
def section(department: Department) -> Section:
    return Section(section_id=4, section_name='Bebidas', department=department)


@pytest.fixture
def product(section: Section, department: Department) -> Product:
    return Product(
        product_id=10,
        product_name='Cerveja',
        product_price=5.99,
        product_department=department,
        product_section=section,
    )
