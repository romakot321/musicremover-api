import json
from io import BytesIO

from src.core.config import settings
from src.core.http.client import IHttpClient
from src.task.domain.entities import TaskRun
from src.integration.domain.dtos import IntegrationTaskResultDTO
from src.integration.domain.mappers import TaskRunToRequestMapper
from src.integration.domain.schemas import LalalaiCheckResponse, LalalaiSplitResponse, LalalaiUploadResponse
from src.integration.domain.exceptions import IntegrationRequestException
from src.task.application.interfaces.task_runner import ITaskRunner
from src.integration.infrastructure.http_api_client import HttpApiClient


class LalalaiTaskRunner(HttpApiClient, ITaskRunner[IntegrationTaskResultDTO]):
    token: str = settings.LALALAI_API_TOKEN
    api_url: str = "https://www.lalal.ai"

    def __init__(self, client: IHttpClient) -> None:
        super().__init__(client=client, source_url=self.api_url)

    async def _upload_file(self, file: BytesIO) -> LalalaiUploadResponse:
        response = await self.request(
            "POST", "/api/upload", data=file.read(), headers={"Content-Disposition": "attachment; filename=result.mp3"}
        )
        result = self.validate_response(response.data, LalalaiUploadResponse)
        if result.status == "error":
            raise IntegrationRequestException(result.error)
        return result

    async def start(self, data: TaskRun) -> IntegrationTaskResultDTO:
        uploaded_file = await self._upload_file(data.file)

        request = TaskRunToRequestMapper().map_one(data, uploaded_file.id)
        params = request.params[0].model_dump_json()
        response = await self.request("POST", "/api/split", data=params)

        result = self.validate_response(response.data, LalalaiSplitResponse)
        if result.status == "success":
            return IntegrationTaskResultDTO(status="progress", external_task_id=uploaded_file.id)
        return IntegrationTaskResultDTO(status="error", error=result.error)

    async def get_result(self, external_task_id: str) -> IntegrationTaskResultDTO | None:
        response = await self.request("POST", "/api/check", data=f"id={external_task_id}")

        result = self.validate_response(response.data, LalalaiCheckResponse)
        if result.status == "error":
            raise IntegrationRequestException(result.error)
        task = list(result.result.values())[0]

        if task.status == "error":
            return IntegrationTaskResultDTO(status="error", error=task.error)
        return IntegrationTaskResultDTO(
            status=task.task.state if task.task else "progress",
            external_task_id=external_task_id,
            stem_track=task.split.stem_track if task.split else None,
            back_track=task.split.back_track if task.split else None,
            error=task.task.error if task.task else None,
        )
