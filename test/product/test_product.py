import pytest
import json
from httpx import AsyncClient
from faker import Faker

from test.conf_test_db import app


@pytest.mark.asyncio
async def test_all_products():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/")
    assert response.status_code == 200
    context = json.loads(response.content.decode())
    assert context is not None
    assert type(context) == list
    assert len(context) == 1


@pytest.mark.asyncio
async def test_create_product():
    data = {
        "name": "tomato",
        "amount": 10
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products/", json=data)
    assert response.status_code == 201
    context = json.loads(response.content.decode())
    assert context['name'] == 'tomato' and context['amount'] == 10


@pytest.mark.asyncio
async def test_update_product():
    data = {
        "name": "Ice",
        "uuid": "some_uuid",
        "amount": 10
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/products/{data['uuid']}", json=data)
    assert response.status_code == 202
    context = json.loads(response.content.decode())
    assert context['name'] == 'Ice' and context['amount'] == 20 and context['uuid'] == 'some_uuid'


@pytest.mark.asyncio
async def test_update_with_create_product():
    data = {
        "name": "carrot",
        "uuid": "some_uuid2",
        "amount": 5
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/products/{data['uuid']}", json=data)
    assert response.status_code == 201
    context = json.loads(response.content.decode())
    assert context['name'] == 'carrot' and context['amount'] == 5 and context['uuid'] != 'some_uuid'


@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/products/some_uuid")
        assert response.status_code == 204
        response = await ac.delete("/products/some_uuid")
        assert response.status_code == 404
