from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

SQLALCHEMY_DB_URL =os.getenv("SQLALCHEMY_DB_URL")
engine = create_engine(SQLALCHEMY_DB_URL)
#print(SQLALCHEMY_DB_URL)
sessionlocal = sessionmaker(bind = engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
        
# statment 
