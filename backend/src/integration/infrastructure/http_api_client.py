from typing import Type, Literal, TypeVar, Callable, Awaitable
from urllib.parse import urljoin

import aiohttp
from loguru import logger
from pydantic import BaseModel, ValidationError

from src.core.http.client import IHttpClient
from src.integration.domain.exceptions import (
    IntegrationRequestException,
    IntegrationUnauthorizedExeception,
    IntegrationInvalidResponseException,
)

T = TypeVar("T", bound=BaseModel)


class AuthMixin:
    token: str | None

    @property
    def auth_headers(self):
        return {"Authorization": f"license {self.token}"}


class ApiResponse(BaseModel):
    cookies: dict
    data: dict
    headers: dict


class HttpApiClient(AuthMixin):
    def __init__(
        self,
        client: IHttpClient,
        source_url: str,
        headers: dict | None = None,
        cookies: dict | None = None,
        token: str | None = None,
    ):
        self.token = token
        self.client = client
        self.source_url = source_url
        self.headers = {**(headers or {}), **self.auth_headers}
        self.cookies = cookies or {}

    def validate_response(self, response: dict, validator: Type[T]) -> T:
        try:
            return validator.model_validate(response)
        except ValidationError as e:
            raise IntegrationInvalidResponseException(e) from e

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        **kwargs,
    ) -> ApiResponse:
        headers = headers or {}
        cookies = cookies or {}
        request_params = {
            "url": urljoin(self.source_url, endpoint),
            "headers": {**self.headers, **headers},
            "json": json,
            "params": params,
            "cookies": {**self.cookies, **cookies},
            **kwargs,
        }

        func: Callable[..., Awaitable[aiohttp.ClientResponse]] = getattr(self.client, method.lower())
        response = await func(**request_params)
        if not response.ok:
            if response.status == 401:
                raise IntegrationUnauthorizedExeception()
            logger.error(str(response))
            raise IntegrationRequestException(message=await response.text())

        try:
            response_data = ApiResponse(
                data=await response.json(), cookies=dict(response.cookies.items()), headers=dict(response.headers.items())
            )
        except aiohttp.client_exceptions.ContentTypeError as e:
            raise IntegrationInvalidResponseException("Empty response") from e

        logger.debug(f"Get api response to {endpoint}: {response_data}")
        return response_data
