from fastapi import FastAPI
from models import Product
from database import load_products

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Mini webshop backend radi!"}

@app.get("/products", response_model=list[Product])
def get_products():
    return load_products()
