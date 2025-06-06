"""
User model representing users table.

Define your user attributes and constraints here.

Replace or extend fields to fit your app's user data needs.
"""

from sqlalchemy import Column, Integer, String
from app.database import Base # Base is declarative_base()

class User(Base):
    __tablename__ = "users" # Table name in your DB

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)  # Store hashed passwords only!

    # Add additional fields like is_active, created_at, etc.
