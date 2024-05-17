from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from databases import Database
from sqlalchemy import Table, Column, String, Float, MetaData, insert
import pandas as pd
import logging

DATABASE_URL = "postgresql://syskiuser:syskipassword@127.0.0.1:5432/syskidatabase"
database = Database(DATABASE_URL)
metadata = MetaData()

operation_manual_input = Table(
    "operations_manual_input", metadata,
    Column('seq_no', String, primary_key=True),
    Column('issue_consideration_status', String(15)),
    Column('estimated_mtg_last2wk_time', Float),
    Column('other_work_last2wk_time', Float),
    Column('remarks', String)
)

router = APIRouter()

@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@router.post("/uploadOperationData")
async def upload_operation_data(file: UploadFile = File(...)):
    try:
        if not database.is_connected:
            logging.error("Database is not connected")
            await database.connect()
        
        dataframe = pd.read_csv(file.file)
        
        for _, row in dataframe.iterrows():
            query = insert(operation_manual_input).values(
                seq_no=row['seq_no'],
                issue_consideration_status=row['issue_consideration_status'],
                estimated_mtg_last2wk_time=row['estimated_mtg_last2wk_time'],
                other_work_last2wk_time=row['other_work_last2wk_time'],
                remarks=row['remarks']
            ).on_conflict_do_update(
                index_elements=['seq_no'],
                set_=dict(
                    issue_consideration_status=row['issue_consideration_status'],
                    estimated_mtg_last2wk_time=row['estimated_mtg_last2wk_time'],
                    other_work_last2wk_time=row['other_work_last2wk_time'],
                    remarks=row['remarks']
                )
            )
            await database.execute(query)
        
        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully"})
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        return JSONResponse(status_code=400, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
