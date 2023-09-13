from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
import bcrypt

from app.db.models.user_model import User
from app.db.db_config import get_async_db

from app.db.schemas.user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPwdUpdateSchema,
)


async def get_user(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession):
    query = select(User).execution_options(populate_existing=True)
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreateSchema):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        password=hashed_password.decode("utf-8"),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


# async def create_user(db: AsyncSession, user: UserCreateSchema):
#     db_user = User(**user.dict())
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#
#     return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# Function to verify a user's password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
