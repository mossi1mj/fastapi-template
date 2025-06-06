"""
User schemas for API input/output.

Separate request (create/update) and response schemas help validation and security.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr  # Validates email format
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # Plain password for creating user

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
