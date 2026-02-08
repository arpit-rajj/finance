# import psycopg2 
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os
from dotenv import load_dotenv
load_dotenv()
url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOSTNAME"),
    database=os.getenv("DATABASE_NAME"),
    port=int(os.getenv("DATABASE_PORT", 5432)),
)
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(url_object)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres',
#                             password='arpitraj@020415', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)
