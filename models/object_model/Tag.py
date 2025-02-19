from pydantic import BaseModel, HttpUrl
from typing import Optional, Union


class Tag(BaseModel):
    term: str
    AAT_URL: Optional[Union[HttpUrl, str]]
    Wikidata_URL: Optional[Union[HttpUrl, str]]
