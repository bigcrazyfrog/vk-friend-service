from typing import List, Optional
from uuid import UUID

from app.internal.db.models.user_model import User
from app.internal.domain.entities.user_entities import FriendStatus, NotFoundException, UserIn, UserOut
from app.internal.domain.services.user_services import IUserRepository


class UserRepository(IUserRepository):
    def get_user_by_id(self, id: UUID) -> User:
        user: Optional[User] = User.objects.filter(id=id).first()
        if user is None:
            raise NotFoundException(name="User", id=id)

        return user

    def subscribe(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        from_user = self.get_user_by_id(id=from_user_id)
        to_user = self.get_user_by_id(id=to_user_id)

        if from_user.subscribers.filter(id=to_user_id).exists():
            from_user.subscribers.remove(to_user)
            from_user.friends.add(to_user)
            from_user.save()
            return True

        to_user.subscribers.add(from_user)
        to_user.save()
        return True

    def accept_request(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        from_user = self.get_user_by_id(id=from_user_id)
        to_user = self.get_user_by_id(id=to_user_id)

        if not to_user.subscribers.filter(id=from_user_id).exists():
            raise NotFoundException(name="Responce from user", id=from_user_id)

        to_user.subscribers.remove(from_user)
        to_user.friends.add(from_user)
        to_user.save()
        return True

    def reject_request(self, from_user_id: UUID, to_user_id: UUID) -> bool:
        from_user = self.get_user_by_id(id=from_user_id)
        to_user = self.get_user_by_id(id=to_user_id)

        if not to_user.subscribers.filter(id=from_user_id).exists():
            raise NotFoundException(name="Responce from user", id=from_user_id)

        to_user.subscribers.remove(from_user)
        to_user.save()
        return True

    def get_subscribers(self, user_id: UUID) -> List[UserOut]:
        user = self.get_user_by_id(id=user_id)

        subscribers = user.subscribers.values("id", "username")
        return list(subscribers)

    def get_friend_out_requests(self, user_id: UUID) -> List[UserOut]:
        user = self.get_user_by_id(id=user_id)

        out_requests = user.users.values("id", "username")
        return list(out_requests)

    def get_friends(self, user_id: UUID) -> List[UserOut]:
        user = self.get_user_by_id(id=user_id)

        out_requests = user.friends.values("id", "username")
        return list(out_requests)

    def remove_friend(self, user_id, friend_id):
        user = self.get_user_by_id(id=user_id)
        friend = self.get_user_by_id(id=friend_id)

        if not user.friends.filter(id=friend_id).exists():
            raise NotFoundException(name="Friend", id=friend_id)

        user.friends.remove(friend)
        user.subscribers.add(friend)
        user.save()
        return True

    def get_status(self, user_id: UUID, other_user_id: UUID) -> FriendStatus:
        user = self.get_user_by_id(id=user_id)
        other_user = self.get_user_by_id(id=other_user_id)

        if user.friends.filter(id=other_user_id).exists():
            return FriendStatus.FRIENDS

        if user.subscribers.filter(id=other_user_id).exists():
            return FriendStatus.REQUEST

        if other_user.subscribers.filter(id=user_id).exists():
            return FriendStatus.OUT_REQUEST

        return FriendStatus.NOTHING
