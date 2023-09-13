import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db_config import commit_rollback
from .crud.user_crud import get_user
from ..db.schemas.user_schema import UserSchema


router = fastapi.APIRouter()

async_db: AsyncSession = Depends(commit_rollback)


@router.get("/user/{user_id}", response_model=UserSchema, tags=["Users"])
async def get_user(user_id: int):
    res = await get_user(db=async_db, user_id=user_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found"
        )
    return res
