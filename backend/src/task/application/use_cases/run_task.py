import asyncio
from io import BytesIO
from uuid import UUID

from loguru import logger

from src.task.domain.dtos import TaskCreateDTO, TaskResultDTO
from src.task.domain.mappers import IntegrationResponseToDomainMapper
from src.task.domain.entities import TaskRun, TaskStatus, TaskUpdate
from src.integration.domain.exceptions import IntegrationRequestException
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.application.interfaces.task_runner import ITaskRunner, TResponseData


class RunTaskUseCase:
    TIMEOUT_SECONDS = 5 * 60

    def __init__(self, uow: ITaskUnitOfWork, runner: ITaskRunner) -> None:
        self.uow = uow
        self.runner = runner

    async def execute(self, task_id: UUID, dto: TaskCreateDTO, file: BytesIO) -> None:
        """Run it in background"""
        command = TaskRun(**dto.model_dump(), file=file)
        logger.info(f"Running task {task_id}")
        logger.debug(f"Task {task_id} params: {command}")
        result = await self._run(command)

        if isinstance(result, str):  # If error occured
            await self._set_task_status(task_id, status=TaskStatus.failed, error=result)
            return

        logger.info(f"Task {task_id} result: {result}")
        result_domain = IntegrationResponseToDomainMapper().map_one(result)
        await self._store_result(task_id, result_domain)

    async def _store_result(self, task_id: UUID, result: TaskResultDTO):
        async with self.uow:
            await self.uow.tasks.update_by_pk(
                task_id, TaskUpdate(status=result.status, error=result.error, result=result.result)
            )
            await self.uow.commit()

    async def _set_task_status(self, task_id: UUID, status: TaskStatus, error: str | None = None):
        async with self.uow:
            await self.uow.tasks.update_by_pk(task_id, TaskUpdate(status=status, error=error))
            await self.uow.commit()

    async def _run(self, command: TaskRun) -> TResponseData | str:
        try:
            result = await asyncio.wait_for(self.runner.start(command), timeout=self.TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            return "Generation run error: Timeout"
        except IntegrationRequestException as e:
            return "Request error: " + str(e)
        except Exception as e:
            logger.exception(e)
            return "Internal exception"
        return result
