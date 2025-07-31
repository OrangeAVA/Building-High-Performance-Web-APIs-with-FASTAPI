import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_add_product_unauthorized():
    product_data = {
        "name": "Test Product",
        "description": "Sample",
        "price": 100,
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code in [401, 403]
