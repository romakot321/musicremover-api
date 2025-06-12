from src.core.http.client import AsyncHttpClient
from src.integration.infrastructure.task_runner import LalalaiTaskRunner
from src.task.application.interfaces.task_runner import ITaskRunner


def get_lalalai_task_runner() -> ITaskRunner:
    return LalalaiTaskRunner(AsyncHttpClient())
