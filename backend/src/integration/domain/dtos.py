from enum import Enum
from typing import Literal

from pydantic import BaseModel


class LalalaiTrackStem(str, Enum):
    vocals = 'vocals'
    voice = 'voice'
    drum = 'drum'
    piano = 'piano'
    bass = 'bass'
    electric_guitar = 'electric_guitar'
    acoustic_guitar = 'acoustic_guitar'
    synthesizer = 'synthesizer'
    strings = 'strings'
    wind = 'wind'


class IntegrationTaskRunParamsDTO(BaseModel):
    stem: LalalaiTrackStem
    splitter: Literal['perseus', 'phoenix', 'orion'] | None = None
    enhanced_processing: bool = False
    noise_cancelling: Literal[0, 1, 2] = 1


class IntegrationTaskResultDTO(BaseModel):
    status: Literal["success", "error", "progress", "cancelled"]
    external_task_id: str | None = None
    stem_track: str | None = None
    back_track: str | None = None
    error: str | None = None
