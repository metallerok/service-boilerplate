from src.lib.api_resource import url
from tests.helpers.message_bus_test import AsyncDryRunMessageBus
from src.modules.async_api_module.mb_events import events


def test_async_api(api_factory_async_fx):
    message_bus = AsyncDryRunMessageBus(
        event_handlers={
            events.AsyncRequestProcessed: []
        }
    )

    api_async = api_factory_async_fx(message_bus=message_bus)
    result = api_async.simulate_get(url('/async-api'))

    assert result.status_code == 200

    events_types = [type(m["message"]) for m in message_bus.messages]
    assert events.AsyncRequestProcessed in events_types
