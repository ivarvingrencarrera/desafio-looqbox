from src.entities import Department
from src.exceptions import ValueNotDefined


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
    def department_id(self) -> int:
        if self._department is None:
            raise ValueNotDefined(value='department', entity='section')
        return self._department.id

    @property
    def department_name(self) -> str:
        if self._department is None:
            raise ValueNotDefined(value='department', entity='section')
        return self._department.name

    def __repr__(self) -> str:
        return f'Section(id={self.id}, name={self.name})'
