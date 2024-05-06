from src.modules.core.tests.helpers.message_bus import DryRunMessageBus
from src.lib.api_resource import url

from src.modules.sync_api_module.mb_events import events


def test_sync_api(api_factory_fx):
    message_bus = DryRunMessageBus(
        event_handlers={
            events.SyncRequestProcessed: []
        }
    )

    api = api_factory_fx(message_bus=message_bus)

    URL = url('/sync-api')
    result = api.simulate_get(URL)

    assert result.status_code == 200

    events_types = [type(m["message"]) for m in message_bus.messages]
    assert events.SyncRequestProcessed in events_types
