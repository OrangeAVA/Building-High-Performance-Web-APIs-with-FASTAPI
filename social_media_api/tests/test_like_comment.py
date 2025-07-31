import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    client.post("/signup", json={
        "username": "likecommenter",
        "email": "likecomment@example.com",
        "password": "likepass"
    })
    response = client.post("/login", json={
        "email": "likecomment@example.com",
        "password": "likepass"
    })
    return response.json()["access_token"]


def test_like_post():
    token = get_token()
    # Create a post first
    post_response = client.post(
        "/posts",
        json={"content": "Likeable content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = client.get("/posts", headers={"Authorization": f"Bearer {token}"}).json()[0]["id"]

    response = client.post(f"/like?post_id={post_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Post liked"


def test_comment_post():
    token = get_token()
    post_id = client.get("/posts", headers={"Authorization": f"Bearer {token}"}).json()[0]["id"]
    response = client.post(
        f"/comment?post_id={post_id}&comment=Nice+Post",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Comment added"
