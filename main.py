from fastapi import FastAPI, HTTPException, status, Body
from models import Product
from typing import List
from database import load_products, get_product_by_id, update_product, save_product, delete_product


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

