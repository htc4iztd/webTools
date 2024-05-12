from fastapi import APIRouter
from databases import Database
import sqlalchemy

DATABASE_URL = "postgresql://postgres:6929Mari@localhost/malseDb"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

router = APIRouter()

view = sqlalchemy.Table(
    "operation_manual_input", metadata, 
    autoload_with=database,
    autoload=True
)

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()

async def main():
    query = view.select()
    results = await database.fetch_all(query)
    return {"data": results}