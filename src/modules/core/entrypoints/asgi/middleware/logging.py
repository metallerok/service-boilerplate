import copy
from typing import Type
import datetime as dt
from pathlib import Path
from uuid import uuid4

import falcon

from config import Config


def save_log(path, filename, message):
    dir_path = Path(path)
    file_path = str(dir_path) + "/" + filename
    print(file_path)
    try:
        dir_path.mkdir()
        with open(file_path, "a+") as log:
            log.write(message)
    except FileExistsError:
        with open(file_path, "a+") as log:
            log.write(message)


class LoggingMiddleware:
    def __init__(self, config: Type[Config]):
        self._config = config

    async def process_request(self, req, _):
        request_id = str(uuid4())
        req.context.request_id = request_id
        req.context.dt_start = dt.datetime.utcnow()

    async def process_response(self, req: 'falcon.Request', resp: 'falcon.Response', resource, is_success):
        request_id = req.context.get("request_id")
        dt_start = req.context.get("dt_start")
        if dt_start:
            total_time = (dt.datetime.utcnow() - dt_start)
        else:
            total_time = None

        resp.set_header("X-Request-Id", request_id)

        if not self._config.enable_logging:
            return

        req_body = copy.deepcopy(req.text) if hasattr(req, "text") else {}
        if type(req_body) == dict:
            _mask_secrets(req_body)

        resp_body = copy.deepcopy(resp.data) if not is_success and hasattr(resp, "data") else {}
        if type(resp_body) == dict:
            _mask_secrets(resp_body)

        req_headers = copy.deepcopy(req.headers)

        if "AUTHORIZATION" in req_headers:
            req_headers["AUTHORIZATION"] = "**********"

        if "SERVICE-TOKEN" in req_headers:
            req_headers["SERVICE-TOKEN"] = "***********"

        if "COOKIE" in req_headers:
            cookies = req_headers["COOKIE"].split('; ')
            for cookie_index in range(len(cookies)):
                if cookies[cookie_index].startswith("qvik.session.refresh_token"):
                    cookies[cookie_index] = "qvik.session.refresh_token=***********"
            req_headers["COOKIE"] = "; ".join(cookies)

        response = f"[{dt_start}]: request_id={request_id} status={resp.status} " \
            f"method={req.method} path={req.relative_uri} remote_addr={req.remote_addr} " \
            f"access_route={req.access_route} forwarded_host={req.forwarded_host} " \
            f"host={req.host} params={req.params} body={req_body} " \
            f"headers={req_headers} " \
            f"success={is_success} error_message={resp_body} total_time={total_time}\n"

        # save file
        save_log(self._config.web_logging_dir, "requests_log.txt", response)


def _mask_secrets(data: dict):
    if "password" in data:
        data["password"] = "***********"

    if "refresh_token" in data:
        data["refresh_token"] = "***********"

    if "access_token" in data:
        data["access_token"] = "***********"
