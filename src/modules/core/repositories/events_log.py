import abc
from typing import Sequence, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.modules.core.models.event_log import EventLog


class EventsLogRepoABC(abc.ABC):
    @abc.abstractmethod
    def add(self, event_log: 'EventLog'):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, *args, **kwargs):
        return cls()

    @abc.abstractmethod
    def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[EventLog]:
        raise NotImplementedError


class SAEventsLogRepo(EventsLogRepoABC):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    @classmethod
    def create(cls, db_session: Session) -> 'SAEventsLogRepo':
        return cls(db_session)

    def add(self, event_log: 'EventLog'):
        self._db_session.add(event_log)

    def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[EventLog]:
        query = self._db_session.query(
            EventLog
        )

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()


class AsyncSAEventsLogRepo(EventsLogRepoABC):

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    @classmethod
    def create(cls, db_session: AsyncSession) -> 'AsyncSAEventsLogRepo':
        return cls(db_session)

    def add(self, event_log: 'EventLog'):
        self._db_session.add(event_log)

    async def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[EventLog]:
        query = sa.select(
            EventLog
        )

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        result = await self._db_session.execute(query)

        return result.scalars().all()
