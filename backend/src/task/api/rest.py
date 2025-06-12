from io import BytesIO
from uuid import UUID

from fastapi import File, Depends, APIRouter, UploadFile, BackgroundTasks

from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO
from src.task.api.dependencies import TaskUoWDepend, TaskRunnerDepend
from src.task.application.use_cases.get_task import GetTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.application.use_cases.create_task import CreateTaskUseCase

router = APIRouter()


@router.post("", response_model=TaskReadDTO)
async def create_and_run_task(
    uow: TaskUoWDepend,
    runner: TaskRunnerDepend,
    background_tasks: BackgroundTasks,
    data: TaskCreateDTO = Depends(TaskCreateDTO.as_form),
    file: UploadFile = File(),
):
    task = await CreateTaskUseCase(uow).execute(data)
    if file is not None:
        file_buffer = BytesIO(await file.read())
    background_tasks.add_task(RunTaskUseCase(uow, runner).execute, task.id, data, file_buffer)
    return task


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: UUID, uow: TaskUoWDepend):
    return await GetTaskUseCase(uow).execute(task_id)
