from fastapi.testclient import TestClient
from app import schema
from app.main import app
from .database import test_db, override_get_db


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
