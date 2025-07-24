from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional
from models import Product, Order
from fastapi.encoders import jsonable_encoder


def load_products() -> List[Product]:
    path = Path("data/products.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return [Product(**item) for item in data]

def save_product(new_product: Product) -> bool:
    path = Path("data/products.json")
    with path.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        if any(item["id"] == new_product.id for item in data):
            return False 
        from fastapi.encoders import jsonable_encoder
        data.append(jsonable_encoder(new_product))
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()
    return True

def get_product_by_id(product_id: int) -> Product | None:
    path = Path("data/products.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            if item["id"] == product_id:
                return Product(**item)
    return None

def update_product(product_id: int, updated: Product) -> bool:
    path = Path("data/products.json")
    with path.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        for i, item in enumerate(data):
            if item["id"] == product_id:
                data[i] = jsonable_encoder(updated)
                f.seek(0)
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.truncate()
                return True
    return False

def delete_product(product_id: int) -> bool:
    path = Path("data/products.json")
    with path.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        new_data = [item for item in data if item["id"] != product_id]
        if len(new_data) == len(data):
            return False
        f.seek(0)
        json.dump(new_data, f, indent=2, ensure_ascii=False)
        f.truncate()
        return True



ORDERS_PATH = Path("data/orders.json")

def load_orders() -> List[Order]:
    if not ORDERS_PATH.exists():
        return []
    with ORDERS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return [Order(**item) for item in data]

def save_order(order: Order) -> None:
    orders = load_orders()
    orders.append(order)
    with ORDERS_PATH.open("w", encoding="utf-8") as f:
        json.dump([jsonable_encoder(o) for o in orders], f, indent=2, ensure_ascii=False)

def get_order_by_id(order_id: int) -> Optional[Order]:
    return next((o for o in load_orders() if o.id == order_id), None)

def update_order_status(order_id: int, new_status: str) -> bool:
    orders = load_orders()
    found = False
    for o in orders:
        if o.id == order_id:
            o.status = new_status
            o.obrada = datetime.now()
            found = True
    if found:
        with ORDERS_PATH.open("w", encoding="utf-8") as f:
            json.dump([jsonable_encoder(o) for o in orders], f, indent=2, ensure_ascii=False)
    return found
