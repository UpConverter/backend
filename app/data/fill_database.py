from .. import schemas
from ..database import SessionLocal, engine

def fill_database(data):
    schemas.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    for table, values in data.items():
        for item in values:
            db_item = getattr(schemas, table)(**item)
            db.add(db_item)

    db.commit()
    db.close()