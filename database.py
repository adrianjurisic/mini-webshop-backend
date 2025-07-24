import json
from pathlib import Path
from typing import List
from models import Product
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

