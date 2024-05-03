from typing import Type

from message_bus.core import MessageBusABC
from config import Config
from message_bus import MessageBus, AsyncMessageBus
from src.modules.core.models.meta import session_factory, async_session_factory

from src.modules.sync_api_module.mb_events.events import events_handlers as sync_api_module_events_handlers
from src.modules.async_api_module.mb_events.events import events_handlers as async_api_module_events_handlers


def make_message_bus(config: Type[Config]) -> MessageBusABC:
    message_bus = MessageBus(
        event_handlers={
            **sync_api_module_events_handlers,
        }
    )

    message_bus.context["db_session"] = session_factory(config)()
    message_bus.context["config"] = config

    return message_bus


def make_async_message_bus(config: Type[Config]) -> MessageBusABC:
    message_bus = AsyncMessageBus(
        event_handlers={
            **async_api_module_events_handlers,
        }
    )

    message_bus.context["db_session_maker"] = async_session_factory(config)
    message_bus.context["config"] = config

    return message_bus
