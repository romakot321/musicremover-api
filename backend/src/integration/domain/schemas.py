from typing import Literal

from pydantic import BaseModel


class LalalaiSplitRequest(BaseModel):
    class Params(BaseModel):
        id: str  # File id
        splitter: str | None = None
        stem: str | None = "vocals"
        dereverb_enabled: bool | None = None
        enhanced_processing_enabled: bool | None = None
        noise_cancelling_level: int | None = None

    params: list[Params]


class LalalaiSplitResponse(BaseModel):
    status: Literal["success", "error"]
    error: str | None = None
    task_id: list[str]


class LalalaiCheckResponse(BaseModel):
    class Result(BaseModel):
        class Task(BaseModel):
            state: Literal["success", "error", "progress", "cancelled"]
            error: str | None = None
            progress: int | None = None

        class Split(BaseModel):
            stem_track: str
            back_track: str

        status: Literal["success", "error"]
        name: str | None = None
        error: str | None = None
        task: Task | None = None
        split: Split | None = None

    status: Literal["success", "error"]
    result: dict[str, Result]
    error: str | None = None


class LalalaiUploadResponse(BaseModel):
    status: Literal["success", "error"]
    id: str | None = None
    error: str | None = None
