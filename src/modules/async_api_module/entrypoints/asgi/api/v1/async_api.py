import json
from src.modules.core.entrypoints.asgi.api.v1 import api_resource
from src.modules.async_api_module.mb_events import events
from message_bus import AsyncMessageBus


@api_resource("/async-api")
class AsyncWebController:
    @classmethod
    async def on_get(cls, req, resp):
        message_bus: AsyncMessageBus = req.context["message_bus"]

        resp.text = json.dumps({
            "message": "Response from async API",
        })

        await message_bus.handle(
            message=events.AsyncRequestProcessed(
                id="1",
                text="test"
            )
        )
