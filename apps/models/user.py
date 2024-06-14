from __future__ import annotations

from sqlalchemy import String, Boolean, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseModel

from typing import AsyncIterator
from datetime import datetime


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )

    email: Mapped[str] = mapped_column(
        "email", String(length=100), nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column(
        "username", String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(
        "password", String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(
        "first_name", String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(
        "last_name", String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        "is_verified", Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False)

    @classmethod
    # type: ignore
    async def get_all(cls, session: AsyncSession, include_users: bool) -> AsyncIterator[User]:
        stmt = select(cls)
        if include_users:
            stmt = stmt.options(selectinload(cls.profile))
        stream = await session.stream_scalars(stmt)
        async for row in stream:
            yield row

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int, include_users: bool = False) -> User:
        stmt = select(cls).where(cls.id == id)
        if include_users:
            stmt = stmt.options(selectinload(cls.profile))
        return await session.scalar(stmt)

    @classmethod
    async def create(cls, session: AsyncSession, email: str, username: str, password: str, first_name: str, last_name: str) -> User:
        user = User(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.flush()
        profile = Profile(
            user_id=user.id
        )
        session.add(profile)
        await session.flush()
        new = await cls.get_by_id(session, user.id, include_users=False)
        if not new:
            raise RuntimeError()
        return new


class Profile(BaseModel):
    __tablename__ = 'profiles'

    avatar: Mapped[str] = mapped_column(
        "avatar", String(255), nullable=False, default="default.jpg")
    bio: Mapped[str] = mapped_column("bio", String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="profile")
