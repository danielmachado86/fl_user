from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base User schema for input validation
    """

    email: EmailStr
    full_name: str
    password: str


class UserCreate(UserBase):
    """
    User schema for creating a new user
    """

    pass


class UserUpdate(UserBase):
    """
    User schema for updating an existing user
    """

    password: Optional[str] = None


class UserInDBBase(UserBase):
    """
    Base User schema with fields from MongoDB
    """

    id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda dt: dt.isoformat(timespec="seconds")}


class UserInDB(UserInDBBase):
    """
    User schema with fields from MongoDB
    """

    hashed_password: str


class UserOut(BaseModel):
    """
    User schema for output response
    """

    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda dt: dt.isoformat(timespec="seconds")}


class UserPublic(UserInDBBase):
    """
    Public User schema without sensitive fields
    """

    pass
