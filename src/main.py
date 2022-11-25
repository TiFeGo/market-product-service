from fastapi import FastAPI
from src.endpoints.products import product_router

app = FastAPI(
    title='Ecommerce API',
    version='0.0.1'
)

app.include_router(product_router)
