from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy Base class
Base = declarative_base()


# Create an SQLite database connection
DATABASE_URL = "sqlite:///./test.db"

# Create the database tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
