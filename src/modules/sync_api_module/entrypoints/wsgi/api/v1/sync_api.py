import json
from src.modules.core.entrypoints.wsgi.api.v1 import api_resource
from src.modules.sync_api_module.mb_events import events
from message_bus import MessageBusABC


@api_resource("/sync-api")
class SyncWebController:
    @classmethod
    def on_get(cls, req, resp):
        message_bus: MessageBusABC = req.context["message_bus"]

        message_bus.handle(
            message=events.SyncRequestProcessed(
                id="1",
                text="processed"
            )
        )

        resp.text = json.dumps({
            "message": "Response from sync API",
        })
