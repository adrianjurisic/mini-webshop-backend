from enum import Enum
from fastapi import FastAPI, HTTPException, Query, status, Body
from models import OrderBase, Product, Order, OrderItem, Customer, ProductBase
from typing import List, Optional
from database import load_products, get_product_by_id, update_product, save_product, delete_product
from database import save_order, load_orders, get_order_by_id, update_order_status
from uuid import uuid4
from datetime import datetime
from mailer import send_order_email
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Mini Webshop radi"}


@app.get("/products", response_model=List[Product])
def get_products():
    return load_products()

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductBase):
    products = load_products()
    new_id = max((p.id for p in products), default=0) + 1
    new_product = Product(id=new_id, **product.dict())
    save_product(new_product)
    return new_product

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

@app.post("/orders", response_model=Order)
def create_order(order_data: OrderBase):
    orders = load_orders()
    new_id = max((o.id for o in orders), default=0) + 1
    new_order = Order(id=new_id, **order_data.dict())
    save_order(new_order)
    send_order_email(new_order)
    return new_order

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
