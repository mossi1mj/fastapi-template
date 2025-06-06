"""
Database setup using SQLAlchemy for SQL databases (PostgreSQL, SQLite, etc.).

This is the standard approach for SQL databases.

If you want to use NoSQL databases (MongoDB, DynamoDB), 
see the bottom of this file for recommended packages and example code snippets.

Update the DATABASE_URL with your actual env variable from .env file.

"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ===========================
# Configure your database URL here.
# Examples:
# SQLite (dev):
# DATABASE_URL = "sqlite:///./test.db"
#
# PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# ===========================

# Load .env file variables into environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

# Dependency to get DB session in FastAPI routes
def get_db():
    """
    FastAPI dependency that provides a database session
    and closes it after request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===========================
# NoSQL Recommendations
# ===========================

"""
# For MongoDB (NoSQL) — use Motor (async) or MongoEngine (sync)

# pip install motor
# import motor.motor_asyncio
# client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
# db = client.your_database

# For DynamoDB (AWS NoSQL) — use boto3 or PynamoDB

# pip install boto3 pynamodb
# import boto3
# dynamodb = boto3.resource('dynamodb', region_name='your-region')
# table = dynamodb.Table('your-table-name')

# OR with PynamoDB (ORM-like)

# from pynamodb.models import Model
# from pynamodb.attributes import UnicodeAttribute

# class MyModel(Model):
#     class Meta:
#         table_name = "your-table"
#         region = 'your-region'
#     id = UnicodeAttribute(hash_key=True)
#     attribute = UnicodeAttribute()
"""
