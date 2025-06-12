from typing import Literal

from pydantic import BaseModel

{
    "status": "success",
    "name": "fbc f af eda-Wooly-combine.mp3",
    "size": 371712,
    "duration": 23,
    "presets": {
        "split": {
            "stem_option": [
                "vocals"
            ],
            "splitter": "orion",
            "dereverb_enabled": false,
            "encoder_format": null,
            "encoder_bitrate": null,
            "task_type": "split",
            "enhanced_processing_enabled": false
        }
    },
    "stem": "vocals",
    "splitter": "orion",
    "preview": null,
    "split": null,
    "player": null,
    "task": {
        "id": [
            "076f8ccc-8c86-432d-ad15-2824e6d9a335",
            "a18d9e2b-351d-4192-a1f4-f44a2560adc2",
            "13ccdc63-cc41-4dc1-b440-f1e13e86557d",
            "5afb22bb-6b8d-452d-9a9f-4151fd4f67d7"
        ],
        "state": "progress",
        "split_id": "13ccdc63-cc41-4dc1-b440-f1e13e86557d",
        "progress": 0
    },
    "task_type": "split"
}


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
