from src.modules.core.entrypoints.wsgi.middleware.db_session import SADBSessionMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.encode import EncodeMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.logging import LoggingMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.redis import RedisMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.message_bus import MessageBusMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.config_middleware import ConfigMiddleware  # noqa
# from src.modules.core.entrypoints.wsgi.middleware.auth_middleware import AuthMiddleware, DoesNotAuthMiddleware  # noqa
# from src.modules.core.entrypoints.wsgi.middleware.depot_middleware import DepotMiddleware  # noqa
from src.modules.core.entrypoints.wsgi.middleware.cors_middleware import CORSMiddleware  # noqa
