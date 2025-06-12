"""
User model representing users table.

Define your user attributes and constraints here.

Replace or extend fields to fit your app's user data needs.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Internal DB ID – FastAPI/SQLAlchemy-generated

    uid = Column(String, unique=True, index=True, nullable=False)
    # Firebase UID – from frontend auth

    email = Column(String, unique=True, index=True, nullable=False)
    # Firebase email – from auth

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    # From Firebase displayName, split into first/last

    created_at = Column(DateTime, default=datetime.utcnow)
    # Firebase user creation time or server timestamp

    # Plaid fields (nullable, will be updated post-auth)
    plaid_user_token = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    item_id = Column(String, nullable=True)