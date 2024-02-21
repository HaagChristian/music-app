from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from musicApp.src.settings.settings import SQLALCHEMY_DATABASE_URI

# TODO: adapt db uri
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=1, max_overflow=4, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


