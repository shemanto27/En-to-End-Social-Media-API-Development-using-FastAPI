from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

POSTGRE_URL = settings.DB_URL

engine = create_engine(POSTGRE_URL) #establish connection

SessionLocal = sessionmaker(autoflush=False,expire_on_commit=False,bind=engine) # session to talk to db


Base = declarative_base() #all models that will create table will be extending this base class 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
