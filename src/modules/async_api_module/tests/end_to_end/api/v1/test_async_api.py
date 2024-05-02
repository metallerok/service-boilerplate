from src.lib.api_resource import url
from tests.helpers.message_bus_test import AsyncDryRunMessageBus


def test_async_api(api_factory_async_fx):
    message_bus = AsyncDryRunMessageBus(
        event_handlers={}
    )
    api_async = api_factory_async_fx(message_bus=message_bus)
    result = api_async.simulate_get(url('/async-api'))
    assert result.status_code == 200
