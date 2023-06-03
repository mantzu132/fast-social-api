from fastapi.testclient import TestClient
from app import schema
from app.main import app
from .database import test_db, override_get_db
import pytest

# ----------------- TEST THINGS
client = TestClient(app)


def test_create_user(test_db, override_get_db):
    test_user_data = {"email": "test@user.com", "password": "testpassword"}
    response = client.post("users/", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    user_out = schema.UserOut.parse_obj(data)

    assert user_out.email == test_user_data["email"]
    assert user_out.id is not None


def test_user_login_success(test_db, override_get_db):
    # create a user
    test_user_data = {"email": "test@user.com", "password": "testpassword"}
    client.post("users/", json=test_user_data)

    # now try to login with this user
    login_data = {"username": "test@user.com", "password": "testpassword"}
    response = client.post("/login", data=login_data)

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.parametrize(
    "username,password,status_code,detail",
    [
        ("test@user.com", "wrongpassword", 404, "Invalid Credentials"),
        ("wronguser@user.com", "testpassword", 404, "Invalid Credentials"),
        (None, "testpassword", 422, None),
        ("test@user.com", None, 422, None),
    ],
)
def test_user_login_fail(
    username, password, status_code, detail, test_db, override_get_db
):
    # create a user
    test_user_data = {"email": "test@user.com", "password": "testpassword"}
    client.post("/users/", json=test_user_data)

    # now try to login with this user
    login_data = {"username": username, "password": password}
    response = client.post("/login", data=login_data)

    assert response.status_code == status_code

    if detail is not None:
        assert response.json() == {"detail": detail}
