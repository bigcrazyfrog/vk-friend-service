from typing import Optional
from uuid import UUID

from app.internal.db.models.token_model import RefreshToken
from app.internal.db.models.user_model import User
from app.internal.domain.entities.user_entities import AlreadyExistException, NotFoundException, UserIn, UserOut
from app.internal.domain.services.auth_service import IAuthRepository


class AuthRepository(IAuthRepository):
    def register_user(self, user_data: UserIn) -> bool:
        if User.objects.filter(username=user_data.username).exists():
            raise AlreadyExistException(name="Username", id=user_data.username)

        User.objects.create(username=user_data.username, password=user_data.password)
        return True

    def get_user_by_username(self, username: str) -> Optional[UserOut]:
        user: Optional[User] = User.objects.filter(username=username).first()
        if user is None:
            raise NotFoundException(name="User", id=username)

        return UserOut.from_orm(user)

    def is_correct_password(self, username: str, password: str) -> bool:
        return User.objects.filter(username=username, password=password).exists()

    def token_exists(self, token: str) -> bool:
        return RefreshToken.objects.filter(jti=token).exists()

    def create_token(self, refresh_token, user_id: UUID):
        user = User.objects.filter(id=user_id).first()
        RefreshToken.objects.create(jti=refresh_token, user=user)

    def get_token(self, token: str) -> Optional[RefreshToken]:
        return RefreshToken.objects.filter(jti=token).first()

    def revoke_token(self, token: str) -> None:
        RefreshToken.objects.filter(jti=token).update(revoked=True)

    def revoke_all_tokens(self, user_id: str) -> None:
        RefreshToken.objects.filter(user__id=user_id).update(revoked=True)
