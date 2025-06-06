"""
SQLAlchemy ORM models define your database structure.

Each class represents a table in your database.
The attributes define columns with types and constraints.

Replace or extend these models according to your actual data.
"""

from sqlalchemy import Column, Integer, String, Float
from app.database import Base  # Base is declarative_base()

class Item(Base):
    __tablename__ = "items"  # Table name in your DB

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    name = Column(String, unique=True, index=True, nullable=False)  # Item name, unique and required
    description = Column(String, nullable=True)  # Optional description column
    price = Column(Float, nullable=False)  # Price field, must be provided

    # Add more fields here based on your requirements