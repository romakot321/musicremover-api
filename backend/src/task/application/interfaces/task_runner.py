import abc
from typing import Generic, TypeVar

from src.task.domain.entities import TaskRun

TResponseData = TypeVar("TResponseData")


class ITaskRunner(abc.ABC, Generic[TResponseData]):
    @abc.abstractmethod
    async def start(self, data: TaskRun) -> TResponseData: ...

    @abc.abstractmethod
    async def get_result(self, external_task_id: str) -> TResponseData | None: ...
