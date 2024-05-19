from fastapi import APIRouter
from fastapi.responses import JSONResponse
from databases import Database
import sqlalchemy
import logging

DATABASE_URL = "postgresql://syskiuser:syskipassword@127.0.0.1:5432/syskidatabase"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

router = APIRouter()

# SQLAlchemyエンジンの作成
engine = sqlalchemy.create_engine(DATABASE_URL)

# テーブルの定義
view = sqlalchemy.Table(
    "operations", metadata,
    autoload_with=engine  # エンジンを使用
)

@router.get("/getJoinedTable")
async def get_joined_table():
    try:
        query = view.select()
        if not database.is_connected:
            logging.error("DatabaseBackend is not connect. Trying to connect...")
            await database.connect()
        results = await database.fetch_all(query)
        return JSONResponse(status_code=200, content={"data": results})
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return JSONResponse(status_code=400, content={"message": str(e)})