import streamlit as st
import numpy as np
import pandas as pd
import httpx
import asyncio
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

def encode_file_to_base64(upload_file):
    file_content = upload_file.getValue()
    return base64.b64encode(file_content).decode("utf-8")

async def doc_load(upload_file):
    encoded_file = encode_file_to_base64(upload_file)
    
    data = {
        "file_name" : upload_file.name,
        "file_content": encoded_file
    }
    
    async with httpx.AsyncClient() as client:
        responseDocLoad = await client.post(os.getenv("URL_DATA_LOADER",data))
        if responseDocLoad.status_code == 200:
            result_container.json(responseDocLoad.json())
        else:
            result_container.error("APIからのレスポンスにエラーがありました。")
        return responseDocLoad

def exec_check(ope_no,loader_result):
    data = {
        "ope_no" : ope_no,
        "loader_result" : loader_result
    }
    responseCheck = requests.post(os.getenv("URL_RISK_CHECK",data))
    if responseCheck.status_code == 200:
        result_container.json(responseCheck.json())
    else:
        result_container.error("APIからのレスポンスにエラーがありました。")

def run_async_function(ope_no, upload_file):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loader_result = loop.run_until_complete(doc_load(upload_file))
    loop.close()
    exec_check(ope_no, loader_result)

def on_button_click(ope_no, upload_file):
    result_container.empty()
    load_result = run_async_function(ope_no, upload_file)
    exec_check(ope_no,load_result)

#######################################################

st.set_page_config(
    page_title="リリース推進業務アプリ",
)


st.title("案件チェック系業務") # タイトル
st.markdown(
    """
    業務要求定義書をインプットに、各案件のシステムリスクを自動チェックする機能です。
    """
)

ope_no = st.multiselect("チェック方式", ("システムリスクチェック", "Sample1")) # 複数選択可能なセレクトボックス

upload_file = st.file_uploader("業務要求定義書",type=["txt", "pdf", "png", "jpg", "jpeg", "csv", "xlsx", "pptx", "docx"])

result_container = st.empty()

if st.button("リスクチェック実施", on_click=on_button_click):
    pass