from src.entities import Department


class Section:
    def __init__(
        self, section_id: int, section_name: str, department: Department | None = None
    ) -> None:
        self._section_id = section_id
        self._section_name = section_name
        self._department = department

    @property
    def id(self) -> int:
        return self._section_id

    @property
    def name(self) -> str:
        return self._section_name

    @property
    def department_id(self) -> int | None:
        return self._department.id if self._department else None

    @property
    def department_name(self) -> str | None:
        return self._department.name if self._department else None

    def __repr__(self) -> str:
        return f'Section(id={self.id}, name={self.name})'
