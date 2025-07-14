from sqlalchemy import text
from database import engine

def db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"Successfully connected to database: {db_name}")
            
            version = connection.execute(text("SELECT VERSION()")).scalar()
            print(f"MySQL Server Version: {version}")
    except Exception as e:
        print(f"Failed to connect to database: {str(e)}")

if __name__ == "__main__":
    db_connection()
    