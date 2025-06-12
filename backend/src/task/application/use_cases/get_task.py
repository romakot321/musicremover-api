from uuid import UUID

from fastapi import HTTPException

from src.db.exceptions import DBModelNotFoundException
from src.task.domain.dtos import TaskReadDTO
from src.task.application.interfaces.task_uow import ITaskUnitOfWork


class GetTaskUseCase:
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def execute(self, task_id: UUID) -> TaskReadDTO:
        async with self.uow:
            try:
                task = await self.uow.tasks.get_by_pk(task_id)
            except DBModelNotFoundException:
                raise HTTPException(404)
        return TaskReadDTO(**task.model_dump())
