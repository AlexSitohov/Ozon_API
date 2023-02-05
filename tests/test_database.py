import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_config import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/test_ozon"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_registration(client):
    response = client.post('/users',
                           json=
                           {
                               "username": "merc",
                               "first_name": "alexander",
                               "last_name": "merc",
                               "password": "123",
                               "email": "password",
                               "phone": "89891238888",
                               "city": "moscow",
                               "balance": 10_000
                           })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('first_name') == 'alexander'
    assert response.json().get('username') == 'merc'
    assert response.json().get('phone') == "89891238888"


access_token = ''


def test_login(client):
    response = client.post('/login',
                           headers={"accept": "application/json",
                                    "Content-Type": "application/x-www-form-urlencoded"}
                           ,
                           data={
                               "username": "merc",
                               "password": "123"
                           })
    assert response.status_code == 200
    assert response.json().get("token_type") == "bearer"
    global access_token
    access_token = response.json().get("access_token")


@pytest.mark.parametrize("title, price, qty", [
    ("tea", 100, 100),
    ("phone", 5000, 100),
    ("t-shirt", 3000, 100)
])
def test_post_products(client, title, price, qty):
    response = client.post('/products',
                           headers={"Authorization": f"bearer {access_token}"}
                           ,
                           json={
                               "title": title,
                               "price": price,
                               "qty": qty
                           })
    assert response.status_code == status.HTTP_201_CREATED


def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0].get("title") == "tea"
    assert response.json()[1].get("title") == "phone"
    assert response.json()[2].get("title") == "t-shirt"


def test_post_orders(client):
    response = client.post('/orders',
                           headers={"Authorization": f"bearer {access_token}"}
                           ,
                           json={
                               "products_id": [
                                   1, 2, 3
                               ]
                           })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("customer_id") == 1
    assert response.json().get("summa") == 8100
    assert response.json().get("status") == "Оплачено и скоро будет отправлен"
    assert response.json().get("products")[0].get("title") == "tea"
    assert response.json().get("products")[1].get("title") == "phone"
    assert response.json().get("products")[2].get("title") == "t-shirt"


def test_get_my_orders(client):
    response = client.get("/orders/my-orders", headers={"Authorization": f"bearer {access_token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0].get("products")[0].get("title") == "tea"
    assert response.json()[0].get("products")[1].get("title") == "phone"
    assert response.json()[0].get("products")[2].get("title") == "t-shirt"
