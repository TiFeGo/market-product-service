from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.endpoints.products import product_router
from src.core import tracing_tools

app = FastAPI(
    title='Ecommerce API',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
    tracing_tools.init_tracer()


app.include_router(product_router)
