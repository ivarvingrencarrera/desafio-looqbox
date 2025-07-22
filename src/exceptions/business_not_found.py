from starlette import status
from starlette.exceptions import HTTPException


class BusinessNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'The business you specified does not exist.'

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.message)

    def __str__(self) -> str:
        return self.message
