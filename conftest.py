import pytest_asyncio
import pytest
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.modules.core.models.meta import Base
from src.modules.core import models
# from src.lib.hashing import TokenEncoder
from config import TestConfig
from src.modules.core.entrypoints.wsgi.wsgi import make_app
from src.modules.core.entrypoints.asgi.asgi import make_app as make_async_app
from src import app_globals
from message_bus.message_bus import MessageBusABC
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from tests.helpers.headers import Headers

# from depot.manager import DepotManager
from falcon import testing
# from uuid import uuid4
import venusian


@pytest_asyncio.fixture(scope="module")
async def async_db_engine_fx():
    engine = create_async_engine(TestConfig.async_db_uri)

    venusian.Scanner().scan(models)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def async_db_session_fx(async_db_engine_fx):
    engine = async_db_engine_fx

    async_sessionmaker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    yield async_sessionmaker


@pytest.fixture(scope="module")
def db_engine_fx():
    venusian.Scanner().scan(models)
    engine = create_engine(TestConfig.db_uri)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine


@pytest.fixture(scope="module")
def db_session_fx(db_engine_fx):
    session = sessionmaker(
        db_engine_fx, expire_on_commit=False
    )()

    yield session

    session.close()


@pytest.fixture()
def redis_conn_fx():
    redis_conn_poll = redis.ConnectionPool(
        host=TestConfig.redis_host,
        port=TestConfig.redis_port,
        db=TestConfig.redis_db,
        password=TestConfig.redis_password,
        socket_connect_timeout=10,
    )
    redis_conn = redis.StrictRedis(connection_pool=redis_conn_poll)

    yield redis_conn

    # redis_conn.flushdb()


@pytest.fixture()
def api_async_fx():
    # setup

    yield api_factory_async_(config=TestConfig)

    # teardown


@pytest.fixture()
def api_factory_async_fx():
    return api_factory_async_


def api_factory_async_(
        config=TestConfig,
        message_bus: MessageBusABC = None,
        # depot_: DepotManager = None
):

    # if not depot_:
    #     # clear depot middleware before creating client
    #     # between setup/teardown
    #     # because DepotManager it's singletone
    #     DepotManager._depots = {}

    app = make_async_app(config, message_bus)
    app_globals.api_cache.enabled = False
    client = testing.TestClient(app)

    return client


@pytest.fixture(scope="module")
def api_fx(db_engine_fx):
    # setup

    yield api_factory_(config=TestConfig)

    # teardown


@pytest.fixture()
def api_factory_fx(db_engine_fx):
    return api_factory_


def api_factory_(
        config=TestConfig,
        message_bus: MessageBusABC = None,
        # depot_: DepotManager = None
):
    # if not depot_:
    #     # clear depot middleware before creating client
    #     # between setup/teardown
    #     # because DepotManager it's singletone
    #     DepotManager._depots = {}

    app = make_app(config, message_bus)
    app_globals.api_cache.enabled = False
    client = testing.TestClient(app)

    return client


@pytest.fixture(scope="function")
def headers_fx() -> Headers:
    headers = Headers()

    yield headers


# @pytest.fixture()
# def depot_fx(config=TestConfig):
#     # clear depot middleware before creating client
#     # between setup/teardown
#     # because DepotManager it's singletone
#     DepotManager._depots = {}
#
#     depot = DepotManager.configure(
#         "default",
#         {
#             'depot.storage_path': config.file_storage,
#             'depot.backend': 'depot.io.memory.MemoryFileStorage'
#         }
#     )
#
#     yield depot
#
#     DepotManager._depots = {}