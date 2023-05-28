from typing import List, Tuple
from uuid import UUID

from django.http import HttpRequest, JsonResponse
from ninja.params import Body, Path

from app.internal.domain.entities.user_entities import (
    ErrorResponse,
    FriendStatus,
    FriendStatusResponse,
    SuccessResponse,
    UserIn,
    UserOut,
)
from app.internal.domain.services.user_services import UserService


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def subscribe(self, request, to_user_id: UUID) -> SuccessResponse:
        success = self._user_service.subscribe(from_user_id=request.user, to_user_id=to_user_id)
        return SuccessResponse(success=success)

    def accept_request(self, request, to_user_id: UUID) -> SuccessResponse:
        success = self._user_service.accept_request(from_user_id=request.user, to_user_id=to_user_id)
        return SuccessResponse(success=success)

    def reject_request(self, request, to_user_id: UUID) -> SuccessResponse:
        success = self._user_service.reject_request(from_user_id=request.user, to_user_id=to_user_id)
        return SuccessResponse(success=success)

    def get_subscribers(self, request) -> List[UserOut]:
        return self._user_service.get_subscribers(user_id=request.user)

    def get_friend_out_requests(self, request) -> List[UserOut]:
        return self._user_service.get_friend_out_requests(user_id=request.user)

    def get_friends(self, request) -> List[UserOut]:
        return self._user_service.get_friends(user_id=request.user)

    def remove_friend(self, request, friend_id):
        success = self._user_service.remove_friend(user_id=request.user, friend_id=friend_id)
        return SuccessResponse(success=success)

    def get_status(self, request, other_user_id: UUID) -> FriendStatusResponse:
        status = self._user_service.get_status(user_id=request.user, other_user_id=other_user_id)
        return FriendStatusResponse(status=status.value)
