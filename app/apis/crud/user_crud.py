from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ....app.db.models.user_model import User
from ....app.db.schemas.user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPwdUpdateSchema,
)


async def get_user(db: AsyncSession, user_id: int):
    query = select(User).filter(User.id == user_id).first()
    result = await db.execute(query)
    return result
