from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=1, max_overflow=4, echo=False)
# echo=True for debugging (print SQL queries to console)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
