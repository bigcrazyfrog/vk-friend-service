from typing import List

from django.http import JsonResponse
from ninja import NinjaAPI, Router

from app.internal.domain.entities.user_entities import (
    ErrorResponse,
    FriendStatusResponse,
    NotFoundResponse,
    SuccessResponse,
    UserOut,
)
from app.internal.presentation.handlers.user_handlers import UserHandlers


def get_users_router(user_handlers: UserHandlers):
    router = Router(tags=['friends'])

    router.add_api_operation(
        '',
        ['GET'],
        user_handlers.get_friends,
        response={200: List[UserOut], 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/requests',
        ['GET'],
        user_handlers.get_subscribers,
        response={200: List[UserOut], 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/out_requests',
        ['GET'],
        user_handlers.get_friend_out_requests,
        response={200: List[UserOut], 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/status',
        ['GET'],
        user_handlers.get_status,
        response={200: FriendStatusResponse, 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/subscribe',
        ['POST'],
        user_handlers.subscribe,
        response={200: SuccessResponse, 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/accept',
        ['POST'],
        user_handlers.accept_request,
        response={200: SuccessResponse, 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/reject',
        ['POST'],
        user_handlers.reject_request,
        response={200: SuccessResponse, 404: NotFoundResponse},
    )

    router.add_api_operation(
        '/remove',
        ['POST'],
        user_handlers.remove_friend,
        response={200: SuccessResponse, 404: NotFoundResponse},
    )

    return router


def add_users_router(api: NinjaAPI, user_handlers: UserHandlers):
    users_handler = get_users_router(user_handlers)
    api.add_router('/friends', users_handler)
