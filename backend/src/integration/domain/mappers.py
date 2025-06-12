from src.task.domain.entities import TaskRun
from src.integration.domain.schemas import LalalaiSplitRequest


class TaskRunToRequestMapper:
    def map_one(self, task_run: TaskRun, file_id: str) -> LalalaiSplitRequest:
        return LalalaiSplitRequest(
            params=[
                LalalaiSplitRequest.Params(
                    id=file_id,
                    splitter=task_run.splitter,
                    stem=task_run.stem,
                    enhanced_processing_enabled=task_run.enhanced_processing,
                    noise_cancelling_level=task_run.noise_cancelling
                )
            ]
        )
