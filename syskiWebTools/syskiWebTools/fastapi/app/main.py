import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.responses import JSONResponse
from models.models import CategorizedElements, OperationUploadData
from routers import dataLoad, multiPrompts, multiEmb, getFileList, requestGetOperationTable, requestOperationDataUpload
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

DATABASE_URL = "postgresql://syskiuser:syskipassword@127.0.0.1:5432/syskidatabase"
database = Database(DATABASE_URL)

app = FastAPI()
logging.basicConfig(level=logging.INFO)

origins = [
    "http://localhost:3000",  # Next.jsの開発サーバーのオリジン
]

# CORSMiddlewareを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"greeting": "Hello World"}

@app.post("/dataLoad")
async def data_load(file: UploadFile = File(...), collection_name: str = Form(...)):
    logging.info('START: /dataLoad')
    logging.info('Upload file name is: %s', file.filename)
    
    save_directory = os.getenv("PDF_SAVE_DIRECTORY")
    os.makedirs(save_directory, exist_ok=True)
    
    file_path = os.path.join(save_directory, file.filename)
    logging.info(file_path)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    categorized_elements = dataLoad.data_load_main(file_path)
    emb_result = multiEmb.create_vectorstore(categorized_elements, collection_name)

    logging.info('END: /dataLoad')

    if emb_result == "0":
        dataLoadResult = "データの登録が完了しました。\n登録した各要素は以下の通りです\n" + str(categorized_elements)
    else:
        dataLoadResult = emb_result
    return dataLoadResult

@app.post("/multiPrompt")
async def multi_prompt(seq: str = Form(...), user_input: str = Form(...)):
    logging.info('START: /multi_prompt')
    promptResult = multiPrompts.multi_prompt(seq, user_input)
    logging.info('END: /multi_prompt')
    return promptResult

@app.post("/getFileList")
def get_file_list(server_address: str = Form(...), directory_path: str = Form(...)):
    fileList = getFileList.get_file_list(server_address, directory_path)
    return fileList

@app.post("/callFunctionCalling")
def call_function_calling(
    address: str = Body(...),
    amount: int = Body(...),
    recipient: str = Body(...)
):
    logging.info(f"Received request - address: {address}, amount: {amount}, recipient: {recipient}")

    result = functionCalling.main(address, amount, recipient)
    return result

@app.post("/callSmartContract")
def call_smart_contract(
    address: str = Body(...),
    amount: int = Body(...),
    recipient: str = Body(...)
):
    result = requestSmartContract.main(address, amount, recipient)
    return result

@app.get("/getJoinedTable")
async def get_joined_table():
    result = await requestGetOperationTable.main()
    if isinstance(result, str):
        return JSONResponse(status_code=400, content={"message": result})
    return JSONResponse(status_code=200, content={"data": result, "message": "Data uploaded successfully"})

@app.post("/uploadOperationData")
async def upload_operation_data(request: OperationUploadData):
    result = await requestOperationDataUpload.main(request)
    return result
