from src import schemas
from src.schemas import Base
from sqlalchemy import insert
from src.database import engine, database

async def fill_database(data):
    Base.metadata.create_all(bind=engine)

    async with database.transaction():
        for table, values in data.items():
            table_model = getattr(schemas, table)
            query = insert(table_model).values(values)
            await database.execute(query)