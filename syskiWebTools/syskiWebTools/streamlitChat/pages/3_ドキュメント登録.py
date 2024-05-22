import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
dataLoadUrl = os.getenv("URL_DATA_LOADER")
getFilesUrl = os.getenv("URL_GET_FILES")

def main():
    # ドキュメント登録機能
    st.subheader("ベクターストアへのドキュメント登録機能")
    uploaded_file = st.file_uploader("ドキュメントをアップロードしてください", type=['pdf', 'docx', 'txt'])
    collection_name = st.selectbox('格納先のコレクションを選択してください', ['2302au_111'])
    if st.button("ドキュメント登録"):
        if uploaded_file is not None and collection_name:
            api_response = call_document_upload_api(uploaded_file, collection_name)
            st.text(api_response)
        else:
            st.error("ドキュメントと格納先を選択してください。")

    # セパレーター
    st.markdown("---")

    # サーバファイルシステムアクセス機能
    st.subheader("サーバ上のファイルシステム閲覧・ダウンロード機能")
    host_name = st.text_input("ホスト名を入力してください")
    directory_path = st.text_input("ディレクトリパスを入力してください")

    if st.button("ファイルリスト取得"):
        if host_name and directory_path:
            files_list = get_files_list(host_name, directory_path)
            if files_list:
                st.write("ファイルリスト:")
                for file in files_list:
                    if '.' not in file['name']:
                        # ディレクトリの場合
                        st.markdown(f"[{file['name']}]({file['path']})")
                    else:
                        # ファイルの場合
                        download_url = create_download_link(host_name, file['path'])
                        st.markdown(f"[{file['name']}]({download_url})")
            else:
                st.error("ファイルリストを取得できませんでした。")
        else:
            st.error("サーバアドレスとディレクトリパスを入力してください。")

# API呼び出し関数
def call_document_upload_api(uploaded_file, collection_name):
    url = "http://127.0.0.1:8000/dataLoad"
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    data = {'collection_name': collection_name}
    response = requests.post(url, files=files, data=data)
    return response.text

# GitHubリポジトリのファイルリストを取得するサンプル関数
# 実際には、サーバのAPIを呼び出してファイルリストを取得する
def get_files_list(server_address, directory_path):
    url = "http://localhost:8000/getFileList"
    response = requests.post(url, server_address, directory_path)
    return response

# ファイルダウンロード関数
def create_download_link(server_address, directory_path, file_name):
    return f"{server_address}/{directory_path}/{file_name}"

if __name__ == '__main__':
    st.set_page_config(
        page_title="リリース推進チーム　事業案件リスクチェックアプリ",
        page_icon="🧊"
    )

    st.title("LLM Application for リリース推進チーム")

    main()
