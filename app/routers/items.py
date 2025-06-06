# app/routers/items.py

"""
API endpoints (routes) for items.

Uses FastAPI APIRouter for modular routing.

Injects DB session dependency from app.database.get_db().
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.item import ItemCreate, ItemRead
from app.services import item as item_service
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ItemRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of items with optional pagination.
    """
    items = item_service.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    """
    # Optionally, check if item with same name exists here and raise 400 if so
    db_item = item_service.create_item(db, item)
    return db_item
