# app/routers/users.py

"""
User-related API endpoints.

Demonstrates typical user operations and DB session dependency.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import create_user, get_user_by_uid

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    POST /users/
    Creates a new user.
    Accepts Firebase info (uid, email, names).
    Plaid fields (access_token, item_id) are optional and null initially.
    """
    logger.info(f"POST /users - Attempting to register user: {user_data.email}")
    existing_user = get_user_by_uid(db, user_data.uid)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user_data)

@router.get("/{uid}", response_model=UserResponse)
def fetch_user(uid: str, db: Session = Depends(get_db)):
    """
    GET /users/{uid}
    Fetch user by Firebase UID.
    Plaid fields may be null if not linked yet.
    """
    logger.info(f"GET /users/{uid} - Fetching user")
    user = get_user_by_uid(db, uid)
    if not user:
        logger.error(f"User not found with UID: {uid}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User found: {user.email}")
    return user
