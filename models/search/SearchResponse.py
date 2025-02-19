from pydantic import BaseModel
from typing import List


class SearchResponse(BaseModel):
    total: int
    objectIDs: List[int]