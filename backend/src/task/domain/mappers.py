from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskSource, TaskStatus
from src.integration.domain.dtos import PlayHTStatus, PlayHTResponseDTO
from src.task.application.interfaces.task_runner import TResponseData
from src.integration.infrastructure.external_api.topmediai.schemas import TopMediaiCoverResponse


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


class TopMediaiResponseToDomainMapper:
    def map_one(self, data: TopMediaiCoverResponse) -> TaskResultDTO:
        status = self._map_status(data.status)
        return TaskResultDTO(
            status=status,
            result=data.data.combine_file,
            error=data.message if status is TaskStatus.failed else None
        )

    @staticmethod
    def _map_status(status: int) -> TaskStatus:
        if status == 200:
            return TaskStatus.finished
        elif status >= 400:
            return TaskStatus.failed
        return TaskStatus.queued


class PlayHTResponseToDomainMapper:
    def map_one(self, data: PlayHTResponseDTO) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_playht_status(data.status),
            result=data.output.url if data.output else None,
            error=data.model_dump_json() if data.status == PlayHTStatus.failed else None
        )

    def _map_playht_status(self, status: PlayHTStatus) -> TaskStatus:
        if status == PlayHTStatus.pending:
            return TaskStatus.queued
        if status == PlayHTStatus.in_progress:
            return TaskStatus.started
        if status == PlayHTStatus.completed:
            return TaskStatus.finished
        if status == PlayHTStatus.failed:
            return TaskStatus.failed
