from starlette import status
from starlette.exceptions import HTTPException


class FeatureNotAvailableError(HTTPException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = 'This feature is currently not available. Please contact support.'

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
