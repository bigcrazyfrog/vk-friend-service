from ninja.params import Body

from app.internal.domain.entities.auth_entities import Tokens
from app.internal.domain.entities.user_entities import ErrorResponse, NotFoundException, SuccessResponse, UserIn
from app.internal.domain.services.auth_service import AuthService


class AuthHandlers:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def register_user(self, request, user_data: UserIn = Body(...)) -> tuple[int, SuccessResponse]:
        success = self._auth_service.register_user(user_data=user_data)
        return 201, SuccessResponse(success=success)

    def login(self, request, username: str, password: str) -> tuple[int, ErrorResponse] | Tokens:
        if not self._auth_service.is_correct_password(username=username, password=password):
            return 400, ErrorResponse(error="Incorrect password")

        user = self._auth_service.get_user_by_username(username=username)

        return self._auth_service.generate_tokens(user.id)

    def update_tokens(self, request, token: str) -> Tokens:
        if not self._auth_service.token_exists(token):
            raise NotFoundException(name="Token", id=token)
        #
        if self._auth_service.is_revoked_token(token):
            self._auth_service.revoke_all_tokens(token)
            raise NotFoundException(name="Token", id=token)

        user_id = self._auth_service.get_user_id(token)
        self._auth_service.revoke_token(token)

        return self._auth_service.generate_tokens(user_id)
