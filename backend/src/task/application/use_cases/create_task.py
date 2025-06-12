from loguru import logger

from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO
from src.task.domain.entities import TaskCreate
from src.task.application.interfaces.task_uow import ITaskUnitOfWork


class CreateTaskUseCase:
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def execute(self, dto: TaskCreateDTO) -> TaskReadDTO:
        command = TaskCreate(**dto.model_dump())
        async with self.uow:
            task = await self.uow.tasks.create(command)
            await self.uow.commit()
        logger.debug(f"Created {task=}")
        return TaskReadDTO(**task.model_dump())
