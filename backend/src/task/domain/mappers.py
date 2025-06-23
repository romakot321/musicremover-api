from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskSource, TaskStatus
from src.task.application.interfaces.task_runner import TResponseData


class IntegrationResponseToDomainMapper:
    def __init__(self, source: TaskSource | None = None) -> None:
        self.source = source

    def map_one(self, data: TResponseData) -> TaskResultDTO:
        self.source = self._define_source(data)

        if self.source == TaskSource.playht:
            return PlayHTResponseToDomainMapper().map_one(data)
        elif self.source == TaskSource.topmediai:
            return TopMediaiResponseToDomainMapper().map_one(data)

        raise ValueError("Failed to map integration response: Unknown data source")

    def _define_source(self, data: TResponseData) -> TaskSource | None:
        if self.source:
            return self.source
        if hasattr(data, "status") and hasattr(data, "output"):
            return TaskSource.playht
        elif hasattr(data, "status") and hasattr(data, "data"):
            return TaskSource.topmediai
