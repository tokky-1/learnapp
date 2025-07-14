from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

#SQLALCHEMY_DB_URL =os.getenv("SQLALCHEMY_DB_URL")
SQLALCHEMY_DB_URL = "postgresql://neondb_owner:npg_w1U4YQJitMKc@ep-restless-art-aem19nqy-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require"
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
