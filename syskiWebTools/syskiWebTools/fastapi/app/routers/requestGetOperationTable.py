from fastapi import APIRouter
from fastapi.responses import JSONResponse
from databases import Database
import sqlalchemy

DATABASE_URL = "postgresql://postgres:6929Mari@localhost/malseDb"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

router = APIRouter()

view = sqlalchemy.Table(
    "operations", metadata, 
    autoload_with=database,
    autoload=True
)

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()

async def main():
    try:
        query = view.select()
        results = await database.fetch_all(query)
        return JSONResponse(status_code=200, content={"data": results,"message": "Data uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"data": results,"message": str(e)})