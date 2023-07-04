from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

database = Database(
    DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)
