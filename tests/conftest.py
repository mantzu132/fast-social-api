from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import model
import pytest
from app.database import get_db
from fastapi.testclient import TestClient
from app import schema
from app.routers import post, user

# --------------------- DB STUFF
db_test_url = "postgresql://postgres:masyvus1@localhost/fastapi_test_database"


engine = create_engine(db_test_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ----------------


# These fixtures will be called before each test that needs it.


# test_db will create the tables in our db, and then close/drop the database after the test is done.
@pytest.fixture
def test_db():
    model.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db  # this is where the testing happens
    db.close()
    model.Base.metadata.drop_all(bind=engine)


# Another fixture to override the get_db dependency
@pytest.fixture
def override_get_db():
    def _get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[
        get_db
    ] = _get_db_override  # override the original get_db with the new function


# initialize the client so that we can send requests
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(test_db, override_get_db):
    user_in = schema.UserCreate(email="test@example.com", password="test_password")
    db_user = user.create_user(db=test_db, user=user_in)
    return db_user


# create user , login and extract JWT token.
@pytest.fixture()
def jwt_token(client, test_db, override_get_db, test_user):
    login_data = {"username": test_user.email, "password": "test_password"}
    response = client.post("/login", data=login_data)
    return response.json()["access_token"]


@pytest.fixture
def test_posts(test_db, test_user: schema.UserCreate):
    post_1 = schema.CreatePost(title="test post 1", content="This is test post 1")
    post_2 = schema.CreatePost(title="test post 2", content="This is test post 2")
    post_3 = schema.CreatePost(title="test post 3", content="This is test post 3")

    created_post_1 = post.create_post(db=test_db, post=post_1, current_user=test_user)
    created_post_2 = post.create_post(db=test_db, post=post_2, current_user=test_user)
    created_post_3 = post.create_post(db=test_db, post=post_3, current_user=test_user)

    return [created_post_1, created_post_2, created_post_3]
