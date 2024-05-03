from message_bus.events import Event
from dataclasses import dataclass


@dataclass
class AsyncRequestProcessed(Event):
    id: str
    text: str


events_handlers = {
    AsyncRequestProcessed: []
}
