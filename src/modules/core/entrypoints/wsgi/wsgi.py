import logging
import falcon
import redis
from typing import Type, Optional
# from depot.manager import DepotManager
from sqlalchemy.orm import Session
from config import Config
from src import app_globals

from src.modules.core.entrypoints.wsgi.middleware import (
    SADBSessionMiddleware,
    EncodeMiddleware,
    LoggingMiddleware,
    RedisMiddleware,
    MessageBusMiddleware,
    ConfigMiddleware,
    # AuthMiddleware, DoesNotAuthMiddleware,
    # DepotMiddleware,
    CORSMiddleware,
)


from falcon_cache.middleware import CacheMiddleware
from falcon_cache.cache import APICache


from src.modules.core.models.meta import session_factory
from src.modules.core.mb_events.factory import make_message_bus

from src.modules.core.entrypoints.wsgi.errors.base import (
    validation_error_handler,
    no_result_found_handler,
)

from sqlalchemy.exc import NoResultFound
from marshmallow import ValidationError
from message_bus import MessageBusABC
import venusian


class AppLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = ''
        return True


def make_app(
        config: Type[Config] = Config,
        message_bus: Optional[MessageBusABC] = None,
        # depot: DepotManager = None,
) -> falcon.App:
    _init_environment(config)

    # Uncomment this if you will use file depot
    # if not depot:
    #     depot = _init_file_storage(config)

    db_session = _make_db_session(config)
    redis_ = _make_redis_conn(config)

    if not message_bus:
        message_bus = make_message_bus(config)

    middlewares = []

    if config.is_cors_enable:
        middlewares.append(
            CORSMiddleware(allow_origins=config.allow_origins, allow_credentials=config.allow_credentials)
        )

    app_globals.api_cache = APICache(redis=redis_)
    app_globals.api_cache.enabled = config.is_cache_enabled

    middlewares.extend([
        ConfigMiddleware(config),
        # DepotMiddleware(depot),
        RedisMiddleware(redis_),
        CacheMiddleware(cache=app_globals.api_cache),
        # AuthMiddleware(db_session, config),
        EncodeMiddleware(),
        LoggingMiddleware(config),
        SADBSessionMiddleware(db_session),
        MessageBusMiddleware(message_bus),
        # DoesNotAuthMiddleware(),
    ])

    app = falcon.App(
        middleware=middlewares,
    )

    app.add_error_handler(ValidationError, validation_error_handler)
    app.add_error_handler(NoResultFound, no_result_found_handler)

    # todo: add models scan from moduels here
    # venusian.Scanner().scan(models)

    # Provide api scan here
    from src.modules.core.entrypoints.wsgi import api as core_api
    from src.modules.sync_api_module.entrypoints.wsgi import api as sync_api

    scanner = venusian.Scanner(api=app)
    scanner.scan(core_api)
    scanner.scan(sync_api)

    return app


# def _init_file_storage(config: Type[Config]):
#     return DepotManager.configure(
#         "default",
#         {'depot.storage_path': config.file_storage}
#     )


def _init_environment(config: Type[Config]):
    root_logger = logging.getLogger()
    root_logger.addFilter(AppLogFilter())
    logger = logging.getLogger(__name__)
    logger.format = logging.Formatter(config.logger_format)

    logger.setLevel(config.log_level)

    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def _make_db_session(config: Type[Config]) -> Session:
    session = session_factory(config)()

    return session


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
