import uuid
import typing
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.product import Product
from src.schemas import product as schemas


async def filter_product(
        q: str,
        *,
        filter_param: str = 'search',
        skip: int = 0,
        limit: int = 10,
        database: Session,
) -> list[Product]:
    products = database.query(Product).filter(Product.name.contains(q)).offset(skip).limit(limit).all()
    return products


async def get_all(
        database: Session,
        *,
        skip: int = 0,
        limit: int = 10,
) -> list[Product]:
    return database.query(Product).offset(skip).limit(limit).all()


async def create_product(
        product: Union[schemas.CreateProduct, schemas.PutProduct],
        database: Session
) -> Product:
    new_product = Product(
        name=product.name,
        uuid=str(uuid.uuid4()),
        amount=product.amount
    )
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


async def delete_product(
        product_uuid: str,
        database: Session
) -> int:
    deleted = database.query(Product).filter(product_uuid == Product.uuid).delete()
    database.commit()
    return deleted


async def update_product(
        product: schemas.PutProduct,
        database: Session,
) -> Product:
    database.query(Product).filter(product.uuid == Product.uuid).update(
        {Product.amount: Product.amount + product.amount})
    database.commit()
    return database.query(Product).filter(product.uuid == Product.uuid).first()


async def exists(product_uuid: str, database: Session) -> bool:
    return database.query(Product).filter(Product.uuid == product_uuid).first() is not None
