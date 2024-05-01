from dotenv import load_dotenv
import os
from fastapi import APIRouter
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_experimental.open_clip import OpenCLIPEmbeddings
import logging

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from .multiFormatFileProcess import split_image_text_types
import openai
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

load_dotenv()
persistPath = os.getenv("PERSIST_PATH")
BASE_DIR = Path(__file__).parent
router = APIRouter()

def prompt_func(data_dict):
    # Joining the context texts into a single string
    formatted_texts = "\n".join(data_dict["context"]["texts"])
    messages = []

    # Adding image(s) to the messages if present
    if data_dict["context"]["images"]:
        image_message = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{data_dict['context']['images'][0]}"
            },
        }
        messages.append(image_message)

    # Adding the text message for analysis
    text_message = {
        "type": "text",
        "text": (
            "You are the business&system analyst in the company.\n"
            "Prompts provide you some documents contains images and texts.\n"
            "Documents means as requirements specifications, or system designs.\n"
            "You must consider prompts taking into account the contexts(images,texts,keywords) in the documents.\n"
            "And, you must response in Japanese.\n"
            f"User-provided keywords: {data_dict['question']}\n\n"
            "Text and / or tables:\n"
            f"{formatted_texts}"
        ),
    }
    messages.append(text_message)

    return [HumanMessage(content=messages)]

def multi_prompt(seq,user_input):

  # Make retriever
  logging.info('START: Make retriever')
  logging.info(seq)
  logging.info(user_input)

  client = chromadb.PersistentClient(path=persistPath)

  db = Chroma(
    collection_name=seq,
    embedding_function=OpenCLIPEmbeddings(),
    client=client,
    persist_directory=persistPath,
  )

  retriever = db.as_retriever()

  logging.info('END: Make retriever')
  logging.info('INFO: retriever is : %s' ,retriever)  

  logging.info('START: Get models')
  model = ChatOpenAI(temperature=0, model="gpt-4-vision-preview", max_tokens=1024)
  logging.info('END: Get models')

  # RAG pipeline
  logging.info('START: Create RAG Pipeline')
  chain = (
      {
          "context": retriever | RunnableLambda(split_image_text_types),
          "question": RunnablePassthrough(),
      }
      | RunnableLambda(prompt_func)
      | model
      | StrOutputParser()
  )
  logging.info('END: Create RAG Pipeline')
  
  logging.info('START: Invoke Chain')
  result = chain.invoke(user_input)
  
  return result