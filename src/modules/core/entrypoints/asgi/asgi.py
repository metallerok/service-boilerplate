import os
import falcon
import falcon.asgi
import venusian
import logging
import redis

from typing import Type, Optional

from config import Config
from message_bus import MessageBusABC

from src.modules.core.entrypoints.asgi.middleware import (
    DatabaseMiddleware,
    ConfigMiddleware,
    EncodeMiddleware,
    # AuthMiddleware,
    MessageBudsMiddleware,
    LoggingMiddleware,
)
from src.modules.core.entrypoints.wsgi.middleware import (
    CORSMiddleware
)

from src.lib.models_scanner import scan_models
from src.modules.core.models.meta import async_session_factory, Base

from src.modules.core.entrypoints.wsgi.errors.base import (
    async_no_result_found_handler,
    async_validation_error_handler,
    async_base_exception,
)
from src.modules.core.entrypoints.asgi import api as core_api
from src.modules.async_api_module.entrypoints.asgi import api as async_api_module
from src.modules.core.mb_events.factory import make_async_message_bus

from src import app_globals
from falcon_cache.cache import APICache

from sqlalchemy.exc import NoResultFound
from marshmallow import ValidationError


class AppLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = ''
        return True


def make_app(
        config: Type[Config] = Config,
        message_bus: Optional['MessageBusABC'] = None,
) -> falcon.asgi.App:
    _init_environment(config)
    redis_ = _make_redis_conn(config)

    if not message_bus:
        message_bus = make_async_message_bus(config)

    db_sessionmaker, db_engine = async_session_factory(config)
    Base.metadata.bind = db_engine

    app_globals.api_cache = APICache(redis_)

    middlewares = [
        ConfigMiddleware(config),
        DatabaseMiddleware(config, db_engine, db_sessionmaker),
        MessageBudsMiddleware(message_bus),
        # AuthMiddleware(config),
        EncodeMiddleware(),
        LoggingMiddleware(config=config)
    ]

    if config.is_cors_enable:
        middlewares.append(
            CORSMiddleware(allow_origins=config.allow_origins, allow_credentials=config.allow_credentials)
        )

    app = falcon.asgi.App(
        middleware=middlewares,
    )

    app.add_error_handler(ValidationError, async_validation_error_handler)
    app.add_error_handler(NoResultFound, async_no_result_found_handler)
    app.add_error_handler(Exception, async_base_exception)

    venusian.Scanner(api=app).scan(core_api)
    venusian.Scanner(api=app).scan(async_api_module)

    scan_models()

    os.environ['PYTHON_EGG_CACHE'] = os.path.dirname(os.path.abspath(__file__)) + '/.cache'

    # mgr = socketio.AsyncRedisManager(
    #     url=f"redis://{config.redis_host}:{config.redis_port}",
    #     redis_options={
    #         "db": config.redis_db,
    #         "password": config.redis_password,
    #         "socket_connect_timeout": 10,
    #     },
    # )
    #
    # sio = socketio.AsyncServer(
    #     async_mode='asgi',
    #     cors_allowed_origins="*",
    #     client_manager=mgr,
    # )
    #
    # app = socketio.ASGIApp(sio, app)

    return app


def _init_environment(config: Type[Config]):
    root_logger = logging.getLogger()
    root_logger.addFilter(AppLogFilter())
    logger = logging.getLogger(__name__)
    logger.format = logging.Formatter(config.logger_format)
    logger.setLevel(config.log_level)


def _make_redis_conn(config: Type[Config]) -> redis.Redis:
    redis_conn_poll = redis.ConnectionPool(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db,
        password=config.redis_password,
        socket_connect_timeout=10,
    )
    redis_conn = redis.StrictRedis(connection_pool=redis_conn_poll)

    return redis_conn
