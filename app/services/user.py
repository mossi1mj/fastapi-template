"""
User business logic.

Handle user-specific CRUD and any special operations like password hashing here.

Remember: never store plain passwords! Hash them before saving.
"""

"""
User business logic.

Handle user-specific CRUD operations and any special logic (e.g., password hashing here).

⚠️ Reminder: NEVER store plain text passwords. Always hash them using bcrypt or a similar library.
"""
import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)

def get_user_by_uid(db: Session, uid: str):
    """
    Retrieve user by Firebase UID.
    """
    logger.info(f"Looking up user with Firebase UID: {uid}")
    return db.query(User).filter(User.uid == uid).first()

def create_user(db: Session, user_data: UserCreate):
    """
    Create user with optional Plaid fields.
    Initially, Plaid fields will be None.
    """
    logger.info(f"Creating user with UID: {user_data.uid} and email: {user_data.email}")
    new_user = User(
        uid=user_data.uid,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        created_at=user_data.created_at or None,
        plaid_user_token=user_data.plaid_user_token,
        access_token=user_data.access_token,
        item_id=user_data.item_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created with DB ID: {new_user.id}")
    return new_user

