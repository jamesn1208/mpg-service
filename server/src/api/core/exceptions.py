from starlette import status


class FuelAPIBase(Exception):
    pass


class UsernameTaken(FuelAPIBase):
    pass


class UnknownAccount(FuelAPIBase):
    pass


class NoAuth(FuelAPIBase):
    pass


class Unauthenticated(FuelAPIBase):
    pass


class NoAction(FuelAPIBase):
    pass


class MissingData(FuelAPIBase):
    status_code: int

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.status_code = status_code


class ActionError(FuelAPIBase):
    status_code: int

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
