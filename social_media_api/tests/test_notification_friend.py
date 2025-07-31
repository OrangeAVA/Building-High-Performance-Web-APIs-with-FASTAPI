import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_user(username, email, password):
    client.post("/signup", json={"username": username, "email": email, "password": password})
    response = client.post("/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_notification():
    token = create_user("notifier", "notifier@example.com", "notify123")
    response = client.post("/notifications?message=Hello", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Notification sent"

    response = client.get("/notifications", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_friendship():
    token1 = create_user("user1", "user1@example.com", "pass1")
    token2 = create_user("user2", "user2@example.com", "pass2")

    user2_id = client.get("/users/me", headers={"Authorization": f"Bearer {token2}"}).json()["id"]

    response = client.post(f"/friend-request?friend_id={user2_id}", headers={"Authorization": f"Bearer {token1}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Friend request sent"

    request_id = client.get("/friend-requests", headers={"Authorization": f"Bearer {token2}"}).json()[0]["id"]

    response = client.post(f"/accept-friend-request?request_id={request_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Friend request accepted"
