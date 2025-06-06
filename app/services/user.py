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

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.authentication import hash_password  # bcrypt-based utility

def get_user(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user from the database by their ID.

    Args:
        db (Session): SQLAlchemy database session
        user_id (int): User's unique ID

    Returns:
        User | None: The user if found, else None
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user from the database by their email.

    Args:
        db (Session): SQLAlchemy database session
        email (str): User's email address

    Returns:
        User | None: The user if found, else None
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session
        user (UserCreate): Pydantic schema containing user creation data

    Returns:
        User: The newly created user
    """
    hashed_pw = hash_password(user.password)  # Hash password before saving

    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh instance to return it with the ID and timestamps
    return db_user

