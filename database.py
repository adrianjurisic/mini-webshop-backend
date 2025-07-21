import json
from typing import List
from models import Product

DATA_FILE = "data/products.json"

def load_products() -> List[Product]:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Product(**item) for item in data]

def save_products(products: List[Product]):
    with open(DATA_FILE, "w") as f:
        json.dump([product.dict() for product in products], f, indent=4, default=str)
