import datetime as dt
import pytest
from dataclasses import dataclass
from src.modules.core.repositories.outbox import SAOutboxRepo
from message_bus.outbox_handlers.base import OutboxHandlerABC
from message_bus.core import AsyncMessageBus
from message_bus.commands import Command


class MockOutBoxHandler(OutboxHandlerABC):
    async def handle(self, outbox_message, context: dict, *args, **kwargs):
        super().handle(outbox_message, context, *args, **kwargs)

    def _before_handle(self, context: dict):
        pass

    def _handle(self, outbox_message, context: dict, *args, **kwargs):
        outbox_message.processed = dt.datetime.utcnow()

    def _after_handle(self, context: dict):
        pass


@dataclass
class ProcessOrder(Command):
    id: int


@pytest.mark.asyncio
async def test_outbox_processing(async_db_session_fx):
    async with async_db_session_fx() as db_session:
        outbox_repo = SAOutboxRepo(db_session)

        message_bus = AsyncMessageBus()
        message_bus.set_outbox_handlers(handlers=[MockOutBoxHandler()])

        outbox_message = message_bus.register_outbox_message(outbox_repo, message=ProcessOrder(id=1))

        assert outbox_message

        await db_session.commit()

        outbox_messages = await outbox_repo.list_unprocessed()

        assert len(outbox_messages) == 1
        assert outbox_messages[0] == outbox_message
        assert outbox_message.processed is None

        await message_bus.process_outbox(outbox_repo)

        outbox_message = await outbox_repo.get(outbox_message.id)
        assert outbox_message.processed is not None
