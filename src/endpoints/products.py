from fastapi import APIRouter, Depends, status, Response, HTTPException

product_router = APIRouter(
    tags=['Products'],
    prefix='/products'
)


@product_router.get('/', status_code=status.HTTP_200_OK)
async def filter_product(q: str, filter_param: str = search, skip: int = 0, limit: int = 10):
    ...


@product_router.get('/', status_code=status.HTTP_200_OK)
async def get_product(skip: int = 0, limit: int = 10):
    ...


@product_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(product: CreateProduct):
    ...


@product_router.delete('/{product_uuid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_uuid: str):
    ...


@product_router.put('/{product_uuid}')
async def put_product(product_uuid: str, status_code=status.HTTP_200_OK):
    ...
