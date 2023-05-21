from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# db_url = "postgresql://username:password@localhost/dbname"
db_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


__all__ = ["engine", "Session"]
