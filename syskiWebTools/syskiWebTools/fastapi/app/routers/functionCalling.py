from fastapi import APIRouter, HTTPException
import httpx
from langchain import hub
from langchain_core.tools import tool, StructuredTool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

router = APIRouter()

@tool
def callSmartContract(address: str, amount: int, recipient: str):
    """スマートコントラクトを呼び出し、指定された金額をETHで送金する。"""
    # httpx.Clientのインスタンス化
    with httpx.Client() as client:
        # リクエストボディの準備
        data = {
            "address": address,
            "amount": amount,
            "recipient": recipient
        }

        # POSTリクエストの実行
        response = client.post(
            "http://localhost:8000/callSmartContract",
            json=data
        )

        # レスポンスのJSONデータを返す
        return response.json()



def main(address: str, amount: int, recipient: str):
    tools = [callSmartContract]
    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    try:
        # スマートコントラクトの実行
        result = agent_executor.invoke({"input": f"イベントが発生した。渡された情報を基にスマートコントラクトを呼び出して。結果はMarkdown形式で回答して。引数は、address: {address}, amount: {amount}, recipient: {recipient}"})
        
        # 実行結果のチェックとメッセージの準備
        return result["output"]

    except Exception as e:
        # エラー発生時のメッセージ
        return {f"エラーが発生しました: {str(e)}"}