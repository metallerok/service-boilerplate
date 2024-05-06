import logging
from typing import List, Dict, Union, Callable, Type
from message_bus import MessageBusABC
from message_bus.types import Message
from message_bus import events, commands
from message_bus.event_handlers.base import EventHandlerABC
from message_bus.command_handlers.base import CommandHandlerABC
from message_bus.repositories.outbox import OutBoxRepoABC


logger = logging.getLogger(__name__)


class DryRunMessageBus(MessageBusABC):

    def __init__(
        self,
        event_handlers: Dict[Type[events.Event], List[Union[Callable, EventHandlerABC]]] = None,
        command_handlers: Dict[Type[commands.Command], Union[Callable, CommandHandlerABC]] = None,
    ):
        self.messages = []
        self.called_outbox_handlers = []

        if event_handlers:
            self._event_handlers = event_handlers
        else:
            self._event_handlers = dict()

        if command_handlers:
            self._command_handlers = command_handlers
        else:
            self._command_handlers = dict()

        super().__init__()

    def set_event_handlers(self, event: Type[events.Event], handlers: List[Union[Callable, EventHandlerABC]]):
        self._event_handlers[event] = handlers

    def set_command_handler(self, cmd: Type[commands.Command], handler: Union[Callable, CommandHandlerABC]):
        self._command_handlers[cmd] = handler

    def get_event_handlers(
            self,
            event: Type[events.Event],
    ) -> List[Union[Callable, EventHandlerABC]]:
        return self._event_handlers[event]

    def get_command_handler(
            self,
            command: Type[commands.Command],
    ) -> CommandHandlerABC:
        return self._command_handlers[command]

    def handle(self, message: Message, *args, **kwargs):
        handlers = []
        if isinstance(message, events.Event):
            message_desc = {
                "message": message,
                "args": args,
                "kwargs": kwargs,
            }

            for handler in self._event_handlers[type(message)]:
                handlers.append(handler)

        elif isinstance(message, commands.Command):
            message_desc = {
                "message": message,
                "args": args,
                "kwargs": kwargs,
            }

            for handler in self._command_handlers[type(message)]:
                handlers.append(handler)
        else:
            raise Exception(f"{message} was not an Event or Command type")

        message_desc["handlers"] = handlers
        self.messages.append(message_desc)

    def process_outbox(self, outbox_repo: OutBoxRepoABC):
        if len(self._outbox_handlers) == 0:
            return

        outbox_messages = outbox_repo.list_unprocessed()

        for outbox_message in outbox_messages:
            for handler in self._outbox_handlers:
                self.called_outbox_handlers.append(type(handler))


class AsyncDryRunMessageBus(DryRunMessageBus):
    async def handle(self, message: Message, *args, **kwargs):
        return super().handle(message, *args, **kwargs)

    async def batch_handle(self, messages: List[Message], *args, **kwargs):
        for message in messages:
            await self.handle(message, *kwargs, **kwargs)

    async def process_outbox(self, outbox_repo: OutBoxRepoABC):
        if len(self._outbox_handlers) == 0:
            return

        outbox_messages = await outbox_repo.list_unprocessed()

        for outbox_message in outbox_messages:
            for handler in self._outbox_handlers:
                self.called_outbox_handlers.append(type(handler))
