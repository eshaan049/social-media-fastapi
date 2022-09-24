from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os
from .config import settings

# pwd = quote_plus(os.getenv("PASSWORD_DB").encode(encoding="utf-8"))
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)# responsible for SQLAlchemy to connect with postgres or DB
# if we use SQlite DB then we add more parameters like: create_engine(SQ:AL..., connect_args={'check_same_thread':False})

# to talk to SQL DB we need make use of session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():# this is similar to conn.close() where we perform SQL and then close the connection in the end
    db = SessionLocal()# commit we should do in main.py functions
    try:
        yield db
    finally:
        db.close()