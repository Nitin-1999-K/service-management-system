from fastapi import Path, Body
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    user_type: int
    full_name: str
    email: str
    mobile_number: str
    supervisor_id: str | None = None


class UserCreate(UserBase):
    password: str


class UpdateUserBase(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    mobile_number: str | None = None


class HeadUpdateUser(UpdateUserBase):
    pass


class AdminUpdateUser(UpdateUserBase):
    supervisor_id: str | None = None


class UserResponse(UserBase):
    id: str
    created_datetime: datetime