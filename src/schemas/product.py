from pydantic import BaseModel
from typing import Optional


class BaseProduct(BaseModel):
    name: str
    amount: Optional[int]


class CreateProduct(BaseProduct):
    ...


class PutProduct(BaseProduct):
    uuid: str


class Product(BaseProduct):
    id: int
    uuid: str

    class Config:
        orm_mode = True
