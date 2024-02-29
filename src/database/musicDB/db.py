from functools import wraps

from fastapi import Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.settings.settings import SQLALCHEMY_DATABASE_URI_MUSIC

engine_music = create_engine(SQLALCHEMY_DATABASE_URI_MUSIC, pool_size=1, max_overflow=4, echo=False)

SessionLocal_Music = sessionmaker(autocommit=False, autoflush=False, bind=engine_music)

Base = declarative_base()


def get_db_music():
    db = SessionLocal_Music()
    try:
        yield db
        # because of using a generator, a rollback is executed by default
        # because of that, it is not necessary to call db.rollback() in the code
    finally:
        db.close()


def commit_with_rollback_backup(func):
    @wraps(func)
    def wrapper(*args, request: Request = Depends(get_db_music), db: Session = Depends(get_db_music), **kwargs):
        response = func(*args, request=request, db=db, **kwargs)
        db.commit()
        return response

    return wrapper
