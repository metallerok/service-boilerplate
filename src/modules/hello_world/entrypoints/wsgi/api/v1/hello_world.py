import json
from src.modules.core.entrypoints.wsgi.api.v1 import api_resource


@api_resource("/hello-world")
class HelloWorldWebController:
    @classmethod
    def on_get(cls, req, resp):
        resp.text = json.dumps({
            "message": "Hello World!",
        })
