import streamlit as st
import requests
import time
from datetime import datetime

def main():

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # セッションIDの初期化（ページリフレッシュまで固定）
    if "sess_id" not in st.session_state:
        st.session_state.sess_id = str(time.time_ns()) ## session idとして現在時刻(nano秒単位まで)使用
    sess_id = st.session_state.sess_id

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", "content": "あなたはリリース推進チームのリスクチェック業務用AIアシスタントです。リスクチェックを行いたい四半期案件とリスクチェックの観点を教えますので、あなたがもっている知識（文章、画像問わず）をもとに回答してください"}]

    seq = st.selectbox('チェック対象の事業案件SEQを入力してください',["2302au_111"])

    user_input = st.text_input("チェックしてほしい観点を入力してください")

    if st.button("リスクチェック開始"):
        api_response = call_multimodal_api(seq, user_input)
        placeholder = st.empty()
        placeholder.markdown(api_response)

def call_multimodal_api(seq, user_input):
    try:
        url = "http://localhost:8000/multiPrompt"
        data={"seq": seq, "user_input": user_input}
        response = requests.post(url, data=data,timeout=100000)
        response.raise_for_status()
        response_text = response.json()
        return response_text
    except requests.RequestException as e:
        return f"API呼び出し中にエラーが発生しました: {e}"

if __name__ == '__main__':
    st.set_page_config(
        page_title="リリース推進チーム　事業案件リスクチェックアプリ",
        page_icon="🧊"
    )

    st.title("LLM Application for リリース推進チーム")

    main()