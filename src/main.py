from fastapi.routing import APIRouter

from src.routers import (
    business_router,
    department_router,
    product_router,
    section_router,
    store_router,
)
from src.settings.server.fastapi import app

routers: list[APIRouter] = [
    product_router,
    section_router,
    department_router,
    store_router,
    business_router,
]
routers.sort(key=lambda router: router.prefix)


def sort_routes_by_path(router: APIRouter) -> None:
    router.routes.sort(key=lambda route: route.path)  # type: ignore[attr-defined]


for router in routers:
    sort_routes_by_path(router)
    app.include_router(router)
