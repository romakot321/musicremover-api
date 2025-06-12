import datetime as dt
from uuid import UUID

from sqlalchemy import MetaData, text
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


class BaseMixin:
    id: Mapped[UUID] = mapped_column(server_default=text("gen_random_uuid()"), primary_key=True, index=True)
    created_at: Mapped[dt.datetime] = mapped_column(server_default=text("now()"), default=dt.datetime.now)
    updated_at: Mapped[dt.datetime | None] = mapped_column(nullable=True, onupdate=text("now()"))

