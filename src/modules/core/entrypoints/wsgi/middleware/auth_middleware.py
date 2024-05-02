import falcon
from typing import Type, Optional
from config import Config
from sqlalchemy.orm import Session
from src.repositories.users import SAUsersRepository, UsersRepositoryABC
from src.entrypoints.web.errors.base import HTTPUnauthorized
from src.lib.jwt import JWTToken
from src.lib.hashing import PasswordEncoder
from src.services.auth import UserAuthenticator
import base64

from src.models.user import User


class AuthMiddleware:
    def __init__(self, db_session: Session, config: Type[Config]):
        self._db_session = db_session
        self._config = config

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

        if req.auth is None:
            req.context["current_user"] = None
            req.context["current_user_id"] = None
            return

        auth = req.auth.split() if req.auth \
            and len(req.auth.split()) == 2 else None

        if auth is None:
            raise HTTPUnauthorized

        users_repo = SAUsersRepository(self._db_session)

        if auth[0] == "Bearer":
            current_user = self._bearer_auth(token=auth[1], users_repo=users_repo)
        elif auth[0] == "Basic":
            current_user = self._basic_auth(encoded_credentials=auth[1], users_repo=users_repo)
        else:
            raise HTTPUnauthorized

        req.context["current_user"] = current_user
        req.context["current_user_id"] = current_user.id

    def _bearer_auth(self, token: str, users_repo: UsersRepositoryABC) -> Optional[User]:
        token = JWTToken(token, self._config.jwt_secret)
        if not token.is_valid():
            raise HTTPUnauthorized(description={
                "error_message": "invalid token"
            })

        current_user = users_repo.get(token["object_id"])

        if current_user and current_user.credential_version != token.payload["credential_version"]:
            raise HTTPUnauthorized

        return current_user

    @classmethod
    def _basic_auth(cls, encoded_credentials: str, users_repo: UsersRepositoryABC) -> Optional[User]:
        email, password = base64.b64decode(encoded_credentials).decode().split(":", 1)

        authenticator = UserAuthenticator(
            users_repo=users_repo,
            password_encoder=PasswordEncoder(),
        )

        current_user = authenticator.authenticate(email, password)

        if not current_user:
            raise HTTPUnauthorized

        return current_user


class DoesNotAuthMiddleware:
    def process_response(self, req, resp, _, __):
        if resp.status == falcon.HTTP_401:
            if req.headers.get("X-DISALLOW-AUTH-HEADER") == "1":
                return

            if req.relative_uri.startswith("/caldav") or (req.relative_uri == "/"):
                resp.append_header("WWW-Authenticate", 'Basic realm="Qvik caldav"')
            else:
                resp.append_header("WWW-Authenticate", 'Bearer realm="QVIK API"')
