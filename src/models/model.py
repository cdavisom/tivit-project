import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    role: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
