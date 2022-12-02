import pytest

from src.models.product import Product


@pytest.fixture(autouse=True)
def create_dummy_product(tmpdir):
    from .conf_test_db import override_get_db
    database = next(override_get_db())
    new_product = Product(name='Ice', uuid='some_uuid', amount=10)
    database.add(new_product)
    database.commit()

    yield

    database.query(Product).filter(Product.uuid == 'some_uuid').delete()
    database.commit()
