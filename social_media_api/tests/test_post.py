import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    client.post("/signup", json={
        "username": "poster",
        "email": "poster@example.com",
        "password": "posterpass"
    })
    response = client.post("/login", json={
        "email": "poster@example.com",
        "password": "posterpass"
    })
    return response.json()["access_token"]


def test_create_post():
    token = get_token()
    response = client.post(
        "/posts",
        json={"content": "Test post content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Post created successfully"


def test_get_posts():
    token = get_token()
    response = client.get("/posts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
