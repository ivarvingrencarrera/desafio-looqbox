from __future__ import annotations

from typing import cast

from pydantic import BaseModel, Field

from src.entities import Section

from .department_output_schema import DepartmentOutputBaseSchema


class SectionOutputBaseSchema(BaseModel):
    id: int = Field(examples=[4])
    name: str = Field(examples=['BEBIDAS'])


class SectionOutputSchema(SectionOutputBaseSchema):
    @staticmethod
    def from_entity(section: Section) -> SectionOutputSchema:
        return SectionOutputSchema(id=section.id, name=section.name)


class SectionDepartmentOutputSchema(SectionOutputBaseSchema):
    department: DepartmentOutputBaseSchema

    @staticmethod
    def from_entity(section: Section) -> SectionDepartmentOutputSchema:
        return SectionDepartmentOutputSchema(
            id=section.id,
            name=section.name,
            department=DepartmentOutputBaseSchema(
                id=cast(int, section.department_id), name=cast(str, section.department_name)
            ),
        )
