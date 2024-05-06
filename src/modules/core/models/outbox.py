import uuid
import datetime as dt
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from src.modules.core.models.meta import Base
from src.modules.core.models.primitives.events import (
    SAMessage,
)
from message_bus.types import Message


class OutBox(Base):
    __tablename__ = "outbox"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))

    type: Mapped[str] = mapped_column(nullable=False)
    message_type: Mapped[str] = mapped_column(nullable=False)
    message: Mapped['Message'] = mapped_column(type_=SAMessage, nullable=False)

    datetime: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)
    processed: Mapped[Optional[dt.datetime]] = mapped_column(default=None)
