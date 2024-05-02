from src.modules.core.entrypoints.wsgi.middleware.db_session import SADBSessionMiddleware
from src.modules.core.entrypoints.wsgi.middleware.encode import EncodeMiddleware
from src.modules.core.entrypoints.wsgi.middleware.logging import LoggingMiddleware
from src.modules.core.entrypoints.wsgi.middleware.redis import RedisMiddleware
from src.modules.core.entrypoints.wsgi.middleware.message_bus import MessageBusMiddleware
from src.modules.core.entrypoints.wsgi.middleware.config_middleware import ConfigMiddleware
# from src.modules.core.entrypoints.wsgi.middleware.auth_middleware import AuthMiddleware, DoesNotAuthMiddleware
# from src.modules.core.entrypoints.wsgi.middleware.depot_middleware import DepotMiddleware
from src.modules.core.entrypoints.wsgi.middleware.cors_middleware import CORSMiddleware
