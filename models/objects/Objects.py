from pydantic import BaseModel
from typing import List

class Objects(BaseModel):
    """Модель получения списка объектов"""
    
    total: int
    objectIDs: List[int] #| List[None]
