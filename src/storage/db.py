import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.storage.models import Base

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Check .env file")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """Yield a SQLAlchemy session"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created")
    