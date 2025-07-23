from starlette import status
from starlette.exceptions import HTTPException


class ValueNotDefined(HTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, value: str, entity: str) -> None:
        self.message = f'The {value} is not defined for the {entity}.'
        super().__init__(status_code=self.status_code, detail=self.message)

    def __str__(self) -> str:
        return self.message
