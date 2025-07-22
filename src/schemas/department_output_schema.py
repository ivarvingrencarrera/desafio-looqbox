from __future__ import annotations

from pydantic import BaseModel, Field

from src.entities import Department


class DepartmentOutputBaseSchema(BaseModel):
    id: int = Field(examples=[2])
    name: str = Field(examples=['BEBIDAS'])


class DepartmentOutputSchema(DepartmentOutputBaseSchema):
    @staticmethod
    def from_entity(department: Department) -> DepartmentOutputSchema:
        return DepartmentOutputSchema(id=department.id, name=department.name)
