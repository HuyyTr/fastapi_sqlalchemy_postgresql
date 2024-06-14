from core.security import hash_password
from models.user import User, Profile
from schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from db.postgresql import AsyncSession

from typing import Union, List, Type


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def get_by_id(self, user_id: int) -> UserSchema:
        async with self.async_session.begin() as session:
            user = await User.get_by_id(session, user_id)
            return UserSchema.model_validate(user)

    async def create(self, data: UserCreateSchema) -> UserSchema:
        async with self.async_session.begin() as session:
            data.password = hash_password(data.password)
            new_user = await User.create(
                session, **data.model_dump(exclude_unset=True))
            return UserSchema.model_validate(new_user)

    def update(self, user_id: int, data: UserUpdateSchema) -> User:
        pass

    def delete(self, user_id: int):
        pass

    def get_current_user(self, ) -> User:
        pass

    def authenticate(self, username, password) -> User:
        pass
