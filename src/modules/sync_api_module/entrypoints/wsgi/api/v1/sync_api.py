import json
from src.modules.core.entrypoints.wsgi.api.v1 import api_resource


@api_resource("/sync-api")
class SyncWebController:
    @classmethod
    def on_get(cls, req, resp):
        resp.text = json.dumps({
            "message": "Response from sync API",
        })
