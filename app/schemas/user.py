"""
User schemas for API input/output.

Separate request (create/update) and response schemas help validation and security.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    uid: str  # Firebase UID
    email: EmailStr
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None

    # Add these optional Plaid fields here with default None
    plaid_user_token: Optional[str] = None
    access_token: Optional[str] = None
    item_id: Optional[str] = None

class UserResponse(BaseModel):
    id: int  # FastAPI-generated DB ID
    uid: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    plaid_user_token: Optional[str] = None
    access_token: Optional[str] = None
    item_id: Optional[str] = None

    class Config:
        orm_mode = True
