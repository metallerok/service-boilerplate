from sqlalchemy.util import partial
from src.lib.api_resource import resource

PREFIX = "/api/v1"

api_resource = partial(resource, prefix=PREFIX)
