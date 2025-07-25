from typing import List, Optional, Literal
from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    quantity: int
    created_at: datetime

class Product(ProductBase):
    id: int


class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Customer(BaseModel):
    ime: str
    prezime: str
    adresa: str
    telefon: str
    email: Optional[str] = None

class OrderBase(BaseModel):
    kupac: Customer
    stavke: List[OrderItem]
    status: Literal["Prihvaćeno", "Odbijeno", "Završeno"]
    kreirano: datetime
    obrada: Optional[datetime] = None

class Order(OrderBase):
    id: int

