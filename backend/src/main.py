from fastapi import FastAPI

from src.task.api.rest import router as task_router
from src.core.logging_setup import setup_fastapi_logging
import src.core.logging_setup

app = FastAPI(title="Music Remover API")
setup_fastapi_logging(app)

app.include_router(task_router, tags=["Task"], prefix="/api/task")
