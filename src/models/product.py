from sqlalchemy import Column, Integer, String

from src.db.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    uuid = Column(String(255), unique=True)
    amount = Column(Integer)

    def __init__(self, name, uuid, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.uuid = uuid
        self.amount = amount

