import hashlib
from datetime import datetime
from uuid import UUID

import jwt

from app.internal.domain.entities.auth_entities import Tokens
from app.internal.domain.entities.user_entities import UserIn, UserOut
from config.settings import (
    JWT_ACCESS_SECRET,
    JWT_ACCESS_TOKEN_LIFETIME,
    JWT_REFRESH_SECRET,
    JWT_REFRESH_TOKEN_LIFETIME,
    SALT,
)


class IAuthRepository:
    def register_user(self, user_data: UserIn) -> bool:
        ...


class AuthService:
    def __init__(self, auth_repo: IAuthRepository):
        self._auth_repo = auth_repo

    def register_user(self, user_data: UserIn) -> bool:
        user_data.password = self.hash_password(password=user_data.password)
        return self._auth_repo.register_user(user_data=user_data)

    def get_user_by_username(self, username: str) -> UserOut:
        return self._auth_repo.get_user_by_username(username=username)

    def hash_password(self, password: str) -> str:
        return hashlib.sha512(password.encode() + SALT.encode()).hexdigest()

    def is_correct_password(self, username: str, password: str) -> bool:
        hash_password = self.hash_password(password)
        return self._auth_repo.is_correct_password(username=username, password=hash_password)

    def token_exists(self, token: str) -> bool:
        return self._auth_repo.token_exists(token=token)

    def is_revoked_token(self, token: str) -> bool:
        refresh_token = self._auth_repo.get_token(token=token)
        if refresh_token.revoked:
            return True

        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        date = datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date < datetime.now()

    def check_access_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return False

        date = datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date > datetime.now()

    def get_user_id(self, token: str) -> UUID | None:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        return UUID(payload["id"])

    def revoke_token(self, token: str) -> None:
        self._auth_repo.revoke_token(token=token)

    def revoke_all_tokens(self, token: str) -> None:
        user_id = self.get_user_id(token=token)
        self._auth_repo.revoke_all_tokens(user_id=user_id)

    def generate_tokens(self, user_id: UUID) -> Tokens:
        access_token = self._generate_access_token(user_id)
        refresh_token = self._generate_refresh_token(user_id)

        self._auth_repo.create_token(refresh_token=refresh_token, user_id=user_id)

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def _generate_access_token(self, user_id: UUID):
        date = str(datetime.now() + JWT_ACCESS_TOKEN_LIFETIME)
        return jwt.encode({"id": str(user_id), "admin": False, "date": date}, JWT_ACCESS_SECRET, algorithm="HS256")

    def _generate_refresh_token(self, user_id: UUID):
        date = str(datetime.now() + JWT_REFRESH_TOKEN_LIFETIME)
        return jwt.encode({"id": str(user_id), "date": date}, JWT_REFRESH_SECRET, algorithm="HS256")
