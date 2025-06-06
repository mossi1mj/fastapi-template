"""
Pydantic schemas define how data is sent and received via API.

Use separate schemas for:
- reading data (response)
- creating/updating data (request)

Adjust fields and validation according to your API needs.
"""

from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., example="Sample Item")  # Required name field
    description: Optional[str] = Field(None, example="A nice item")  # Optional description
    price: float = Field(..., gt=0, example=9.99)  # Price must be positive float

class ItemCreate(ItemBase):
    pass  # Add extra fields or validation if needed when creating

class ItemRead(ItemBase):
    id: int

    class Config:
        orm_mode = True  # Needed for ORM model compatibility in responses
