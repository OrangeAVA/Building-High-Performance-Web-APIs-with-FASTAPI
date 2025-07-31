import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_signup():
    response = client.post("/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_login():
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
