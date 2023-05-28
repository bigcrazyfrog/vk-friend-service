from ninja import NinjaAPI, Router

from app.internal.domain.entities.auth_entities import Tokens
from app.internal.domain.entities.user_entities import ErrorResponse, SuccessResponse
from app.internal.presentation.handlers.auth_handlers import AuthHandlers


def get_users_router(auth_handlers: AuthHandlers):
    router = Router(tags=['auth'])

    router.add_api_operation(
        '/login',
        ['POST'],
        auth_handlers.login,
        response={200: Tokens, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/auth',
        ['POST'],
        auth_handlers.register_user,
        response={201: SuccessResponse, 400: ErrorResponse},
        auth=None,
    )

    router.add_api_operation(
        '/update_tokens',
        ['POST'],
        auth_handlers.update_tokens,
        response={200: Tokens, 400: ErrorResponse},
        auth=None,
    )

    return router


def add_auth_router(api: NinjaAPI, auth_handlers: AuthHandlers):
    auth_handler = get_users_router(auth_handlers)
    api.add_router('', auth_handler)
