from sqlalchemy import insert

from src import schemas
from src.database import database, engine
from src.schemas import Base


async def fill_database(data):
    await database.connect()  # Ожидание установки соединения
    try:
        Base.metadata.create_all(bind=engine)

        async with database.transaction():
            for table, values in data.items():
                table_model = getattr(schemas, table)
                query = insert(table_model).values(values)
                await database.execute(query)
    finally:
        await database.disconnect()  # Разрыв соединения
