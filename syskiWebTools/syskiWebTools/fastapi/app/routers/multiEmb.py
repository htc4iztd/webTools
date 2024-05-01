from dotenv import load_dotenv
import os
import uuid

from fastapi import APIRouter
import chromadb
import numpy as np
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from models.models import CategorizedElements
import logging
import openai
from PIL import Image as _PILImage

load_dotenv()
router = APIRouter()
openai.api_key = os.getenv("OPENAI_API_KEY")
persistPath = os.getenv("PERSIST_PATH")
logging.basicConfig(level=logging.INFO)

path = os.getenv("IMAGE_OUTPUT_DIR")

def create_vectorstore(categorized_elements: CategorizedElements, collection_name):
  # Create Vectorstore
  logging.info('START: Create Vectorstore')
  logging.info('INFO: categorized_elements: %s',categorized_elements)

  client = chromadb.PersistentClient(path=persistPath)

  db = Chroma(
    collection_name=collection_name,
    embedding_function=OpenCLIPEmbeddings(),
    client=client,
    persist_directory=persistPath,
  )

  # Add images
  logging.info('START: Add images')

  # Get image URIs with .jpg extension only
  image_uris = sorted(
      [
          os.path.join(path, image_name)
          for image_name in os.listdir(path)
          if image_name.endswith(".jpg")
      ]
  )
  print(image_uris)

  if not image_uris:
    logging.info("画像が見つかりませんでした。")
  else:
    try:
        db.add_images(uris=image_uris)
    except Exception as e:
        embResult = f"1: エラーが発生しました: {e}"
        logging.error('ERROR: Add images')
        return embResult
  logging.info('END: Add images')
  
  logging.info('START: Add documents')
  if not categorized_elements['texts']:
    logging.info("文章が見つかりませんでした。")
  else:
    try:
      db.add_texts(texts=categorized_elements['texts'])
    except Exception as e:
      embResult = f"1: エラーが発生しました: {e}"
      logging.error('ERROR: Add documents')
      return embResult
    logging.info('END: Add documents')
    embResult = f"0: 正常に登録できました。作成したコレクション名: {collection_name}"
  
  logging.info('END: Create Vecotorstore')
  return embResult

## Comment out during ver1.0 development
# def addVectorRecord(categorized_elements: CategorizedElements):
#   # Create Vectorstore
#   logging.info('START: Create Vectorstore')
#   logging.info('INFO: categorized_elements: %s',categorized_elements)
# 
#   client = chromadb.Client(Settings(
#     chroma_db_impl="duckdb+parquet",
#     persist_directory="chromadb_data"
#   ))
# 
#   vectorstore = client.create_collection(name="mm_rag_clip_photos", embedding_function=OpenCLIPEmbeddings())
# 
#   # Add images
#   logging.info('START: Add images')
#   vectorstore.add_images(uris=path)
#   logging.info('END: Add images')
#   
#   
#   logging.info('START: Add documents')
#   vectorstore.add_texts(texts=categorized_elements.texts)
#   logging.info('END: Add documents')
# 
#   logging.info('INFO: vectorstore: %s' ,vectorstore)
# 
#   client.persist()
#   
#   logging.info('END: Create Vecotorstore')