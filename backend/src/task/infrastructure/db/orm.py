from sqlalchemy.orm import Mapped

from src.db.base import Base, BaseMixin


class TaskDB(BaseMixin, Base):
    __tablename__ = "tasks"

    user_id: Mapped[str]
    app_bundle: Mapped[str]
    status: Mapped[str | None]
    result: Mapped[str | None]
    error: Mapped[str | None]
