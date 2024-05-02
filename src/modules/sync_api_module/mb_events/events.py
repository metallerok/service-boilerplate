from message_bus.events import Event
from dataclasses import dataclass


@dataclass
class SyncRequestProcessed(Event):
    id: str
    text: str


events = {
    SyncRequestProcessed: []
}
