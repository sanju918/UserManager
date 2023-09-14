from pydantic import BaseModel, EmailStr, constr, SecretStr
from datetime import datetime


class UserBaseSchema(BaseModel):
    email: EmailStr
    role: int
    is_active: bool


class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8)


class UserUpdateSchema(UserBaseSchema):
    ...


class UserPwdUpdateSchema(BaseModel):
    email: EmailStr
    current_password: SecretStr
    new_password: constr(min_length=8)


class UserSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
