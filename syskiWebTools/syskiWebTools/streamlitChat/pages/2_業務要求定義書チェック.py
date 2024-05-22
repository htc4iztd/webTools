import streamlit as st
import numpy as np
import pandas as pd
import httpx
import asyncio
from dotenv import load_dotenv
import base64
import requests
import openai

load_dotenv()

# OpenAI APIキーの設定
openai.api_type = "azure"
openai.api_version = "turbo-2024-04-09"
openai.api_key = '8b1f726c620b4e4c8450b8abc56c4e86'

''' 
OpenAI APIではモデルに対して明確な役割分担を示し、応答の一貫性を促すことができる。具体的には、system,user,assistantの３つのロール設定によって実現可能
  system:
  user:
  assistant:
'''
message_text = [{"role":"system", "content":"You are an AI assistant that helps KDDI's Information system department."},
                {"role":"user", "content":""},
                {"role":"assistant", "content":""}]

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

st.set_page_config(
    page_title="業務要求定義書チェックアプリ",
)

st.title("ドキュメントチェック") 
st.markdown(
    """
    業務要求定義書の誤字脱字や日本語表現のチェックを行い、指摘をしてくれる機能です。
    """
)

ope_no = st.selectbox("①チェックするドキュメントの案件種別を選択してください", ("","au案件", "BBC案件")) 

upload_file = st.file_uploader("②チェックするドキュメントをアップロードしてください。",type=["txt", "pdf", "png", "jpg", "jpeg", "csv", "xlsx", "pptx", "docx"])

if st.button("チェック開始", on_click=on_button_click):
    pass
