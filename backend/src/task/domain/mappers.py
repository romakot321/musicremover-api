from typing import Literal

from src.integration.domain.dtos import IntegrationTaskResultDTO
from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskSource, TaskStatus
from src.task.application.interfaces.task_runner import TResponseData


class IntegrationResponseToDomainMapper:
    def __init__(self, source: TaskSource | None = None) -> None:
        self.source = source

    def map_one(self, data: IntegrationTaskResultDTO) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_status(data.status),
            result=data.stem_track,
            error=data.error
        )

    def _map_status(self, status: Literal["success", "error", "progress", "cancelled"]) -> TaskStatus:
        if status == "success":
            return TaskStatus.finished
        elif status == "error":
            return TaskStatus.failed
        elif status == "progress":
            return TaskStatus.queued
        elif status == "cancelled":
            return TaskStatus.failed
        raise ValueError("Failed to map integration response: Unknown status {}".format(status))
