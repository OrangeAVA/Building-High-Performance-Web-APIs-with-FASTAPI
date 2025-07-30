import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order_without_login():
    response = client.post("/orders")
    assert response.status_code in [401, 403]

def test_get_cart_for_nonexistent_user():
    response = client.get("/cart/999")
    assert response.status_code == 200
    assert response.json() == []
