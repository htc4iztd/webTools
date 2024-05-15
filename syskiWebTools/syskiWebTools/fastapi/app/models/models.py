# models.py
from pydantic import BaseModel
from typing import List

class CategorizedElements(BaseModel):
    tables: List[str]
    texts: List[str]

class OperationUploadData(BaseModel):
    request: List[str]

class OperationUpdateData(BaseModel):
    request: List[str]
