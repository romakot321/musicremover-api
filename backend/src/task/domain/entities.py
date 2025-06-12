from io import BytesIO
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.integration.domain.dtos import IntegrationTaskRunParamsDTO


class TaskSource(str, Enum):
    playht = "playht"
    topmediai = "topmediai"


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    failed = "failed"
    finished = "finished"


class Task(BaseModel):
    id: UUID
    user_id: str
    app_bundle: str
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskCreate(BaseModel):
    user_id: str
    app_bundle: str


class TaskResultQuality(str, Enum):
    draft = 'draft'
    low = 'low'
    medium = 'medium'
    high = 'high'
    premium = 'premium'


class TaskRun(IntegrationTaskRunParamsDTO, BaseModel):
    file: BytesIO

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    result: str | None = None
    error: str | None = None

