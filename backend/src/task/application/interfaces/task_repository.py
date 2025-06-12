import abc
from uuid import UUID

from src.task.domain.entities import Task, TaskCreate, TaskUpdate


class ITaskRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: TaskCreate) -> Task: ...

    @abc.abstractmethod
    async def get_by_pk(self, pk: UUID) -> Task: ...

    @abc.abstractmethod
    async def update_by_pk(self, pk: UUID, data: TaskUpdate) -> Task: ...
