from typing import List, Optional, Literal
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

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Customer(BaseModel):
    ime: str
    prezime: str
    adresa: str
    telefon: str
    email: Optional[str] = None

class Order(BaseModel):
    id: int
    kupac: Customer
    stavke: List[OrderItem]
    status: Literal["Prihvaćeno", "Odbijeno", "Završeno"] = "Prihvaćeno"
    kreirano: datetime
    obrada: Optional[datetime] = None
