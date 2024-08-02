from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date


class UserBase(BaseModel):
    user: str
    permission: Literal['usuario', 'administrador']
    name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserId(UserBase):
    id: int


class User(UserId):
    updated_at: date
    created_at: date


class UsersList(BaseModel):
    users: list[User]


class UserUpdate(BaseModel):
    password: Optional[str] = None
    permission: Optional[Literal['usuario', 'administrador']] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
