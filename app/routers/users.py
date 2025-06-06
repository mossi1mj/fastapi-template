# app/routers/users.py

"""
User-related API endpoints.

Demonstrates typical user operations and DB session dependency.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserRead
from app.services import user as user_service
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of users with pagination.
    """
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Example check to prevent duplicate email registration
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_service.create_user(db, user)
    return new_user
