from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import HttpBearer

from app.internal.db.repositories.auth_repository import AuthRepository
from app.internal.db.repositories.user_repositories import UserRepository
from app.internal.domain.entities.user_entities import AlreadyExistException, NotFoundException
from app.internal.domain.services.auth_service import AuthService
from app.internal.domain.services.user_services import UserService
from app.internal.presentation.handlers.auth_handlers import AuthHandlers
from app.internal.presentation.handlers.user_handlers import UserHandlers
from app.internal.presentation.routers.auth_routers import add_auth_router
from app.internal.presentation.routers.user_routers import add_users_router


class HTTPJWTAuth(HttpBearer):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self._auth_service = auth_service

    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not self._auth_service.check_access_token(token):
            return None

        user = self._auth_service.get_user_id(token)
        if user is None:
            return None

        request.user = user
        return token


def get_api():
    user_repo = UserRepository()
    user_service = UserService(user_repo=user_repo)
    user_handlers = UserHandlers(user_service=user_service)

    auth_repo = AuthRepository()
    auth_service = AuthService(auth_repo=auth_repo)
    auth_handlers = AuthHandlers(auth_service=auth_service)

    api = NinjaAPI(
        title='FRIENDS.BACKEND',
        version='1.0.1',
        auth=HTTPJWTAuth(auth_service=auth_service),
    )

    add_auth_router(api, auth_handlers)
    add_users_router(api, user_handlers)

    return api


user_api = get_api()


@user_api.exception_handler(NotFoundException)
def not_found_exception_handler(request, exc):
    return user_api.create_response(
        request,
        {"message": f"{exc.name} with id {exc.id} not found"},
        status=404,
    )


@user_api.exception_handler(AlreadyExistException)
def already_exist_exception_handler(request, exc):
    return user_api.create_response(
        request,
        {"message": f"{exc.name} {exc.id} is already exist"},
        status=400,
    )
