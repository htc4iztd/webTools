# models.py
from pydantic import BaseModel
from typing import List

class CategorizedElements(BaseModel):
    tables: List[str]
    texts: List[str]
