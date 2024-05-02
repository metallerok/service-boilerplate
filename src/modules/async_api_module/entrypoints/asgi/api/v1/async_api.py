import json
from src.modules.core.entrypoints.asgi.api.v1 import api_resource


@api_resource("/async-api")
class AsyncWebController:
    @classmethod
    async def on_get(cls, req, resp):
        resp.text = json.dumps({
            "message": "Response from async API",
        })
