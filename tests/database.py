from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import model
import pytest
from app.database import get_db


db_test_url = "postgresql://postgres:masyvus1@localhost/fastapi_test_database"


engine = create_engine(db_test_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# These fixtures will be called before each test that needs it.
# test_db will create the tables in our db, and then close/drop the database after the test is done.
@pytest.fixture(scope="function")
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
