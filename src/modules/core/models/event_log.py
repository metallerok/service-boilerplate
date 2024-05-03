import uuid
import sqlalchemy as sa
import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column
from typing import Type, TYPE_CHECKING
from sqlalchemy import types
from .meta import Base

from message_bus.events import Event


class SAEventType(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: Event, dialect):
        return str(value.__name__)

    def process_result_value(self, value, dialect):
        return value

    @property
    def python_type(self):
        return Event


class SAEvent(types.TypeDecorator):
    impl = types.JSON

    def process_bind_param(self, value: Event, dialect):
        return value.serialize()

    def process_result_value(self, value, dialect):
        return value

    @property
    def python_type(self):
        return Event


class EventLog(Base):
    __allow_unmapped__ = True
    __tablename__ = "events_log"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[uuid.UUID] = mapped_column(nullable=True, index=True)
    object_id: Mapped[str] = mapped_column(nullable=True, index=True)

    if TYPE_CHECKING:
        type: Mapped[Type["Event"]]
        event: Mapped["Event"]
    else:
        type = mapped_column(type_=SAEventType, nullable=False, index=True)
        event = mapped_column(type_=SAEvent, nullable=False)

    info: Mapped[str] = mapped_column(nullable=True)
    datetime: Mapped[dt.datetime] = mapped_column(default=sa.func.now())
