from enum import Enum
from uuid import UUID

from ninja import Schema
from pydantic import Field


class SuccessResponse(Schema):
    success: bool


class ErrorResponse(Schema):
    error: str = "error message"


class UserSchema(Schema):
    username: str = Field(max_length=225)


class UserOut(UserSchema):
    id: UUID = "id"


class UserIn(UserSchema):
    password: str = "password"


class NotFoundResponse(Schema):
    message: str = "Not Found!"


class FriendStatus(Enum):
    FRIENDS = "Friends"
    REQUEST = "Incoming request"
    OUT_REQUEST = "Outgoing request"
    NOTHING = "Nothing"


class FriendStatusResponse(Schema):
    status: str


class NotFoundException(Exception):
    def __init__(self, name: str, id: UUID):
        self.name = name
        self.id = id


class AlreadyExistException(Exception):
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id
