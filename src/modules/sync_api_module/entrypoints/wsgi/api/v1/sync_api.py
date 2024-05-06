import json
import random
from src.modules.core.entrypoints.wsgi.api.v1 import api_resource
from src.modules.sync_api_module.message_bus import events
from message_bus import MessageBusABC
from src.app_globals import api_cache


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


@api_resource("/sync-cached-resource")
class CachableResourceWebController:
    @classmethod
    @api_cache.cached(timeout=5)
    def on_get(cls, req, resp):
        param_value = req.params.get("value", -1)

        resp.text = json.dumps({
            "value": param_value,
            "payload": random.randint(0, 10000),
        })
