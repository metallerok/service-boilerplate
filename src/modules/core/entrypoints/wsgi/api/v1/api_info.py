import json
from src.modules.core.entrypoints.wsgi.api.v1 import api_resource


@api_resource("/api-info")
class APIInfo:
    @classmethod
    def on_get(cls, req, resp):
        config = req.context["config"]

        resp.text = json.dumps({
            "name": config.app_name,
        })
