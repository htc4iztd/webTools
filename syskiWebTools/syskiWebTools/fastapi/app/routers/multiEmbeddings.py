from dotenv import load_dotenv
import os
import uuid
from fastapi import APIRouter
import chromadb
import numpy as np
from langchain_community.vectorstores import Chroma
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from PIL import Image as _PILImage

load_dotenv()
path = os.getenv("IMAGE_OUTPUT_DIR")

router = APIRouter()

def make_retriever():
  # Create chroma
  vectorstore = Chroma(
      collection_name="mm_rag_clip_photos", embedding_function=OpenCLIPEmbeddings()
  )
  
  # Get image URIs with .jpg extension only
  image_uris = sorted(
      [
          os.path.join(path, image_name)
          for image_name in os.listdir(path)
          if image_name.endswith(".jpg")
      ]
  )
  
  # Add images
  vectorstore.add_images(uris=image_uris)
  
  # Add documents
  vectorstore.add_texts(texts=texts)
  
  # Make retriever
  retriever = vectorstore.as_retriever()
  
  return retriever