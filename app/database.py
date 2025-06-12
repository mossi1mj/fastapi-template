import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")
logger.info(f"Connecting to database at {DATABASE_URL}")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()

# Import models after Base is declared to avoid circular imports

def initialize_database(models: list):
    """
    Initialize the database: create tables if they don't exist.

    Args:
        models (list): List of SQLAlchemy model classes to check/create.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    for model in models:
        table_name = model.__tablename__
        if table_name not in tables:
            logger.info(f"Creating '{table_name}' table...")
            Base.metadata.create_all(bind=engine, tables=[model.__table__])
            logger.info(f"'{table_name}' table created.")
        else:
            logger.info(f"'{table_name}' table already exists — skipping creation.")

# FastAPI dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()