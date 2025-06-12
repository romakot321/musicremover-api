import abc

from src.task.application.interfaces.task_repository import ITaskRepository


class ITaskUnitOfWork(abc.ABC):
    tasks: ITaskRepository

    async def commit(self):
        return await self._commit()

    @abc.abstractmethod
    async def _commit(self): ...

    @abc.abstractmethod
    async def _rollback(self): ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._rollback()
