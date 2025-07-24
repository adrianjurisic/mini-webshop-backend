from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    quantity: int
    created_at: datetime

class Customer(BaseModel):
    ime: str
    prezime: str
    telefon: str
    email: Optional[str] = None

class OrderItem(BaseModel):
    naziv: str
    cijena: float
    kolicina: int

class Order(BaseModel):
    kupac: Customer
    stavke: List[OrderItem]
