from enum import Enum
from fastapi import FastAPI, HTTPException, Query, status, Body
from models import Product, Order, OrderItem, Customer
from typing import List, Optional
from database import load_products, get_product_by_id, update_product, save_product, delete_product
from database import save_order, load_orders, get_order_by_id, update_order_status
from uuid import uuid4
from datetime import datetime
from mailer import send_order_email


app = FastAPI()

@app.get("/products", response_model=List[Product])
def get_products():
    return load_products()

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def add_product(product: Product = Body(...)):
    success = save_product(product)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Proizvod sa ID-jem {product.id} vec postoji."
        )
    return product

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Proizvod nije pronadjen")
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, updated_product: Product):
    if not update_product(product_id, updated_product):
        raise HTTPException(status_code=404, detail="Proizvod nije pronadjen")
    return updated_product

@app.delete("/products/{product_id}", status_code=204)
def delete_product_endpoint(product_id: int):
    if not delete_product(product_id):
        raise HTTPException(status_code=404, detail="Proizvod nije pronadjen")
    return



@app.post("/orders", response_model=Order, status_code=201)
def create_order(order_data: Order):
    existing = load_orders()
    new_id = max([o.id for o in existing], default=0) + 1
    order_data.id = new_id
    order_data.kreirano = datetime.now()
    save_order(order_data)
    send_order_email(order_data)
    return order_data

class OrderStatus(str, Enum):
    prihvaceno = "Prihvaćeno"
    odbijeno = "Odbijeno"
    zavrseno = "Završeno"

@app.get("/orders", response_model=List[Order])
def get_all_orders(
    status: Optional[OrderStatus] = Query(None),
    sort: Optional[str] = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    orders = load_orders()

    if status:
        orders = [o for o in orders if o.status == status.value]

    reverse = sort == "desc"
    orders.sort(key=lambda x: x.kreirano, reverse=reverse)

    return orders[offset:offset + limit]


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Narudžba nije pronađena")
    return order

@app.patch("/orders/{order_id}")
def update_status(order_id: int, status: str = Body(..., embed=True)):
    if status not in ["Prihvaćeno", "Odbijeno", "Završeno"]:
        raise HTTPException(status_code=400, detail="Nevažeći status")
    success = update_order_status(order_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Narudžba nije pronađena")
    return {"message": f"Status promijenjen u '{status}'"}
