from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    quantity: int
    created_at: datetime
