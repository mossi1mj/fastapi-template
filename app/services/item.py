# app/services/item.py

"""
Business logic layer for items.

Contains CRUD operations interacting with the database models.

Use this service inside your routes/controllers to keep code clean.
"""

from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def get_item(db: Session, item_id: int):
    """
    Fetch a single item by its ID from the DB.
    """
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetch multiple items with optional pagination.
    """
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate):
    """
    Create a new item record in the DB.
    """
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Add update, delete, or other business logic as needed
