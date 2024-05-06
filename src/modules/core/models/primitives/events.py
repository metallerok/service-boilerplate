from sqlalchemy import types
from message_bus.events import Event
from message_bus.types import Message


class SAEventType(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: Event, dialect):
        return str(type(value).__name__)

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


class SAMessage(types.TypeDecorator):
    impl = types.JSON

    def process_bind_param(self, value: Message, dialect):
        return value.serialize()

    def process_result_value(self, value, dialect):
        return value

    @property
    def python_type(self):
        return Message
