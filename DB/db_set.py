from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (example: SQLite, but you can use PostgreSQL, MySQL, etc.)
SQLALCHEMY_DATABASE_URL = "sqlite+aiomysql://user:password@localhost/dbname"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
