from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
engine = create_engine(URL, future=True)
local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def create_all_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = local_session()
        yield db
    finally:
        db.close()

