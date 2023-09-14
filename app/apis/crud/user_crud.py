from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update
import bcrypt
from fastapi import Depends, HTTPException, status

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
    hashed_password = encode_pwd(user.password)
    # hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
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


async def update_password(db: AsyncSession, user: UserPwdUpdateSchema, old_pass: str):
    res_user = await get_user_by_email(db, user.email)

    if not verify_password(old_pass, res_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    encoded_pwd = encode_pwd(user.new_password)
    print("Encoded PWD: ", encoded_pwd)
    query = (
        sql_update(User)
        .where(User.email == res_user.email)
        .values(password=encoded_pwd.decode("utf-8"))
    )
    res = await db.execute(query)
    print(res)
    return {"details": "password updated successfully"}


# Function to verify a user's password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def encode_pwd(plain_password):
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
