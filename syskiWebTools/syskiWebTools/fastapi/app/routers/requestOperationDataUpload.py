from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from databases import Database
from sqlalchemy import Table, Column, String, Float, MetaData, insert
import pandas as pd

DATABASE_URL = "postgresql://postgres:6929Mari@localhost/malseDb"
database = Database(DATABASE_URL)
metadata = MetaData()

app = FastAPI()

operation_manual_input = Table(
    "operations_manual_input", metadata,
    Column('seq_no', String, primary_key=True),
    Column('issue_consideration_status', String(15)),
    Column('estimated_mtg_last2wk_time', Float),
    Column('other_work_last2wk_time', Float),
    Column('remarks', String)
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/uploadOperationData")
async def upload_operation_data(file: UploadFile = File(...)):
    try:
        # Read the CSV file directly from the uploaded file's file-like object
        dataframe = pd.read_csv(file.file)
        
        # Iterate over the rows of the DataFrame
        for row in dataframe.iterrows():
            query = insert(operation_manual_input).values(
                seq_no=row['seq_no'],
                issue_consideration_status=row['issue_consideration_status'],
                estimated_mtg_last2wk_time=row['estimated_mtg_last2wk_time'],
                other_work_last2wk_time=row['other_work_last2wk_time'],
                remarks=row['remarks']
            ).on_conflict_do_update(
                index_elements=['seq_no'],  # Ensure this is the column name that acts as a unique identifier
                set_=dict(
                    issue_consideration_status=row['issue_consideration_status'],
                    estimated_mtg_last2wk_time=row['estimated_mtg_last2wk_time'],
                    other_work_last2wk_time=row['other_work_last2wk_time'],
                    remarks=row['remarks']
                )
            )
            # Execute the query
            await database.execute(query)
        
        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)