from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserInCreate(UserIn):
    pass


class UserInUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
