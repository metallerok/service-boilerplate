import uuid
from typing import List, Type
import sqlalchemy as sa
from message_bus.repositories.outbox import OutBoxRepoABC
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.modules.core.models.outbox import OutBox


class SAOutboxRepo(OutBoxRepoABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

        super().__init__()

    def get_model(self) -> Type:
        return OutBox

    def _add(self, outbox_message: OutBox):
        self._db_session.add(outbox_message)

    async def get(self, id: uuid.UUID) -> OutBox:
        query = sa.select(
            OutBox
        ).filter(
            OutBox.id == id,
        )

        result = await self._db_session.scalars(query)

        return result.one_or_none()

    async def list_unprocessed(self) -> List:
        query = sa.select(
            OutBox
        ).filter(
            OutBox.processed.is_(None),
        ).with_for_update()

        result = await self._db_session.execute(query)

        return list(result.scalars().all())

    async def save(self):
        await self._db_session.commit()
