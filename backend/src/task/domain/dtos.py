import inspect
from uuid import UUID
from typing import Type

from fastapi import Form
from pydantic import BaseModel

from src.task.domain.entities import TaskStatus
from src.integration.domain.dtos import IntegrationTaskRunParamsDTO


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.is_required() else Form(model_field.default),
                annotation=model_field.annotation,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    cls.as_form = as_form_func
    return cls


@as_form
class TaskCreateDTO(IntegrationTaskRunParamsDTO, BaseModel):
    user_id: str
    app_bundle: str

    @classmethod
    def as_form(cls): ...


class TaskReadDTO(BaseModel):
    id: UUID
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskResultDTO(BaseModel):
    status: TaskStatus
    result: str | None = None
    error: str | None = None
