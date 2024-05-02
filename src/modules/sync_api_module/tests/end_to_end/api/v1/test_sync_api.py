from tests.helpers.message_bus_test import DryRunMessageBus
from src.lib.api_resource import url


def test_sync_api(api_factory_fx):
    message_bus = DryRunMessageBus(
        event_handlers={}
    )

    api = api_factory_fx(message_bus=message_bus)

    URL = url('/sync-api')
    result = api.simulate_get(URL)

    assert result.status_code == 200
