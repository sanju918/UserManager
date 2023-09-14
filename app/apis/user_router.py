import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from ..db.db_config import get_async_db
from ..db.schemas.user_schema import UserSchema, UserCreateSchema, UserPwdUpdateSchema

from .crud.user_crud import (
    get_user,
    get_users,
    create_user,
    get_user_by_email,
    update_password,
)

router = fastapi.APIRouter()


@router.get("/user/{user_id}", response_model=UserSchema, tags=["Users"])
async def read_user(user_id: int, async_db: AsyncSession = Depends(get_async_db)):
    res = await get_user(db=async_db, user_id=user_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found"
        )
    return res


@router.get("/users", response_model=List[UserSchema], tags=["Users"])
async def read_users(async_db: AsyncSession = Depends(get_async_db)):
    res = await get_users(db=async_db)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found"
        )
    return res


@router.post("/users", response_model=UserSchema, tags=["Users"])
async def create_new_user(
    user: UserCreateSchema, async_db: AsyncSession = Depends(get_async_db)
):
    db_user = await get_user_by_email(db=async_db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Provided Email is not available to use.",
        )
    res = await create_user(db=async_db, user=user)

    return res


@router.post("/forgot-password", tags=["Users"])
async def forgot_password(
    password: str,
    request_body: UserPwdUpdateSchema,
    async_db: AsyncSession = Depends(get_async_db),
):
    res = await update_password(db=async_db, user=request_body, old_pass=password)
    return res


@router.post("/users/{email}", tags=["Users"], response_model=UserSchema)
async def read_user_by_email(
    email: str, async_db: AsyncSession = Depends(get_async_db)
):
    return await get_user_by_email(email=email, db=async_db)
