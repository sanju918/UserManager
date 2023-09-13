import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db_config import get_async_db
from .crud.user_crud import get_user
from ..db.schemas.user_schema import UserSchema

router = fastapi.APIRouter()


@router.get("/user/{user_id}", response_model=UserSchema, tags=["Users"])
async def read_user(user_id: int, async_db: AsyncSession = Depends(get_async_db)):
    res = await get_user(db=async_db, user_id=user_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found"
        )
    return res
