from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.db.database import get_db
from src.schemas import product as schemas
from src.endpoints import service

product_router = APIRouter(
    tags=['Products'],
    prefix='/products'
)


@product_router.get('/filter', status_code=status.HTTP_200_OK, response_model=list[schemas.Product])
async def filter_product(
        q: str,
        filter_param: str = 'search',
        skip: int = 0,
        limit: int = 10,
        database: Session = Depends(get_db)
) -> list[schemas.Product]:
    return await service.filter_product(
        q=q,
        filter_param=filter_param,
        skip=skip,
        limit=limit,
        database=database
    )


@product_router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.Product])
async def get_products(
        skip: int = 0,
        limit: int = 10,
        database: Session = Depends(get_db)
) -> list[schemas.Product]:
    return await service.get_all(
        database,
        skip=skip,
        limit=limit,
    )


@product_router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_product(
        product: schemas.CreateProduct,
        database: Session = Depends(get_db)
) -> schemas.Product:
    return await service.create_product(product, database)


@product_router.delete('/{product_uuid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_uuid: str,
        database: Session = Depends(get_db)
):
    deleted = await service.delete_product(product_uuid, database)
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found!")


@product_router.put('/{product_uuid}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Product)
async def put_product(
        product_uuid: str,
        product: schemas.PutProduct,
        database: Session = Depends(get_db)
):
    if service.exists(product_uuid, database):
        content = await service.update_product(product, database)
        content = jsonable_encoder(schemas.Product(**content.__dict__))
        return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)
    else:
        content = await service.create_product(product, database)
        content = jsonable_encoder(schemas.Product(**content.__dict__))
        return JSONResponse(content=content.json(), status_code=status.HTTP_201_CREATED)
