import json
from src.modules.core.entrypoints.asgi.api.v1 import api_resource


@api_resource("/async-api-info")
class AsyncAPIInfo:
    @classmethod
    async def on_get(cls, req, resp):
        resp.text = json.dumps({
            "name": req.context["config"].app_name,
        })
