from typing import List
from uuid import UUID

from app.internal.domain.entities.user_entities import FriendStatus, UserIn, UserOut


class IUserRepository:
    def get_user_by_id(self, id: UUID) -> UserOut:
        ...

    def add_user(self, user_data: UserIn) -> bool:
        ...

    def update_fields(self, id: str, fields: dict) -> None:
        ...


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def subscribe(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        return self._user_repo.subscribe(from_user_id=from_user_id, to_user_id=to_user_id)

    def get_subscribers(self, user_id: UUID) -> List[UserOut]:
        return self._user_repo.get_subscribers(user_id=user_id)

    def get_friend_out_requests(self, user_id: UUID) -> List[UserOut]:
        return self._user_repo.get_friend_out_requests(user_id=user_id)

    def get_friends(self, user_id: UUID) -> List[UserOut]:
        return self._user_repo.get_friends(user_id=user_id)

    def accept_request(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        return self._user_repo.accept_request(from_user_id=from_user_id, to_user_id=to_user_id)

    def reject_request(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        return self._user_repo.reject_request(from_user_id=from_user_id, to_user_id=to_user_id)

    def remove_friend(self, user_id, friend_id):
        return self._user_repo.remove_friend(user_id=user_id, friend_id=friend_id)

    def get_status(self, user_id: UUID, other_user_id: UUID) -> FriendStatus:
        return self._user_repo.get_status(user_id=user_id, other_user_id=other_user_id)
