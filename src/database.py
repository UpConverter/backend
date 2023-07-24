from databases import Database
from sqlalchemy import MetaData, create_engine

from src.config import settings
from src.constants import DB_NAMING_CONVENTION
from src.schemas import Base

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

database = Database(DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)

Base.metadata.create_all(bind=engine)