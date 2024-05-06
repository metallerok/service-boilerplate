import uuid
import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column
from typing import Type, TYPE_CHECKING
from src.modules.core.models.primitives.events import (
    SAEvent,
    SAEventType,
)
from src.modules.core.models.meta import Base

from message_bus.events import Event


class EventLog(Base):
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
    datetime: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)
