import loguru
from loguru import logger
from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask

from src.core.config import settings


def add_app_name(record):
    record["extra"]["app_name"] = settings.PROJECT_NAME
    return True


def add_http_info(request, response):
    info = {
        "req": {
            "url": request.url.path,
            "headers": request.headers,
            "method": request.method,
        },
        "res": {
            "status_code": response.status_code,
        },
    }

    def patcher(record) -> None:
        record["extra"]["http"] = info

    return patcher


def setup_fastapi_logging(app: FastAPI):
    fastapi_logger = logger.bind(name="fastapi")
    fastapi_logger = fastapi_logger.patch(add_app_name)
    fastapi_logger.add(
        "/app/logs/fastapi.json",
        format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}",
        serialize=True,
        rotation="30 MB",
    )

    def log(request: Request, response: Response):
        level = "DEBUG"
        if response.status_code >= 400:
            level = "INFO"
        elif response.status_code >= 500:
            level = "ERROR"
        fastapi_logger.patch(add_http_info(request, response)).log(level, request.method + " " + request.url.path)

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        response: Response = await call_next(request)
        response.background = BackgroundTask(log, request, response)
        return response


logger.add(
    "/app/logs/app.json",
    format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}",
    serialize=True,
    rotation="30 MB",
    filter=add_app_name,
)
