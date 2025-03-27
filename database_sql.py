# database_sql.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this connection string as needed.
# For peer authentication, ensure the PostgreSQL role "myuser" exists and matches your OS username or adjust pg_hba.conf.
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:password@localhost/mydatabase"

# Create the engine for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

# Define a database model for an item
class SQLItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    in_stock = Column(Boolean, default=True)

# Create the database tables
Base.metadata.create_all(bind=engine)
