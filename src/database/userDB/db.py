from functools import wraps

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette.requests import Request

from musicApp.src.settings.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=1, max_overflow=4, echo=False)
# echo=True for debugging (print SQL queries to console)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
        # because of using a generator, a rollback is executed by default
        # because of that, it is not necessary to call db.rollback() in the code
    finally:
        db.close()


def commit_on_signup(func):
    @wraps(func)
    def wrapper(*args, request: Request = Depends(get_db), db: Session = Depends(get_db), **kwargs):
        response = func(*args, request=request, db=db, **kwargs)
        db.commit()
        return response

    return wrapper
