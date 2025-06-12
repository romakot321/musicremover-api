class IntegrationRequestException(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
        self.message = message


class IntegrationInvalidResponseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IntegrationUnauthorizedExeception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
