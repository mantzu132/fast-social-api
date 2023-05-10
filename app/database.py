from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

# db_url = "postgresql://username:password@localhost/dbname"
db_url = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

__all__ = ["engine", "Session"]
