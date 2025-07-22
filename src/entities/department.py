class Department:
    def __init__(self, department_id: int, department_name: str) -> None:
        self._department_id = department_id
        self._department_name = department_name

    @property
    def id(self) -> int:
        return self._department_id

    @property
    def name(self) -> str:
        return self._department_name

    def __repr__(self) -> str:
        return f'Department(id={self.id}, name={self.name})'
