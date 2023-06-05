from app import schema
import pytest


def test_get_all_posts(jwt_token, test_db, client, test_posts, override_get_db):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/posts/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_get_post(jwt_token, test_db, client, test_posts, override_get_db):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/posts/1", headers=headers)

    assert response.status_code == 200


def test_delete_post(jwt_token, test_db, client, test_posts, override_get_db):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.delete(f"/posts/{test_posts[1].id}", headers=headers)

    assert response.status_code == 200

    response = client.get("/posts/", headers=headers)
    remaining_posts = response.json()

    for post in remaining_posts:
        assert post["post"]["id"] != test_posts[1].id


def test_unauthorized_delete_post(test_db, client, test_posts, override_get_db):
    headers = {"Authorization": "Bearer IncorrectToken"}
    response = client.delete(f"/posts/{test_posts[1].id}", headers=headers)

    assert response.status_code == 401
