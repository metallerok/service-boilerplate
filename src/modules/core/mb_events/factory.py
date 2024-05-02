from typing import Type
from config import Config
from message_bus import MessageBus
from src.modules.sync_api_module.mb_events.events import events as sync_api_module_events
from src.modules.core.models.meta import session_factory


def make_message_bus(config: Type[Config]) -> MessageBus:
    message_bus = MessageBus(
        event_handlers={
            **sync_api_module_events,
        }
    )

    message_bus.context["db_session"] = session_factory(config)()
    message_bus.context["config"] = config

    return message_bus
